import sys
import os
from typing import Dict
from PyQt6.QtWidgets import QApplication, QMenu
from PyQt6.QtCore import Qt, QTimer, QCoreApplication, QPoint
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtGui import QAction, QIcon, QGuiApplication
from src.overlay_window import OverlayWindow
from src.animation_player import AnimationPlayer
from src.audio_manager import AudioManager
from src.behaviors import RandomEdgeBehavior, FreeWalkBehavior, GravityBehavior, get_current_screen
from src.character import CharacterManager
from src.tray_manager import TrayManager
from src.config_manager import ConfigManager
from src.launcher import LauncherWindow, make_icon
from src.utils import migrate_from_local_if_needed, check_single_instance, resource_path, is_fullscreen_active, install_global_exception_handler
from src.translations import init_translations


class ActiveCharacter:
    """Represents an active character with its window and behavior. / Rappresenta un personaggio attivo con la sua finestra e comportamento."""

    def __init__(self, character, app, config_manager=None, translations=None, overlay_app=None):
        self.character = character
        self.app = app
        self.config_manager = config_manager
        self.translations = translations
        self.overlay_app = overlay_app
        self.window = OverlayWindow()
        self.player = AnimationPlayer(self.window)
        self.behavior = None
        self.audio_manager = AudioManager()

        try:
            # Collega il menu contestuale con tasto destro del mouse sul desktop
            self.window.right_clicked.connect(self.show_context_menu)

            # Collega visibilità della finestra all'animazione per azzerare cicli CPU quando nascosta
            self.window.window_hidden.connect(self.player.stop_animation)
            self.window.window_shown.connect(self.player.start_animation)

            # Calculate scaling once / Calcola scaling una volta sola
            scale_factor = (character.scale or 100) / 100
            scaled_width = int(character.width * scale_factor)
            scaled_height = int(character.height * scale_factor)

            # Load animation / Carica animazione
            try:
                self.player.load_animation(character.get_animation_path())
                self.player.set_size(scaled_width, scaled_height)
                # Imposta FPS: se character.fps è specificato usa quello; altrimenti usa None per rispettare le durate native dei frame GIF
                fps_to_use = character.fps
                if self.config_manager:
                    global_fps_limit = self.config_manager.get_global_setting("global_fps_limit", 0)
                    if global_fps_limit > 0:
                        fps_to_use = min(fps_to_use, global_fps_limit) if fps_to_use is not None else global_fps_limit
                self.player.set_fps(fps_to_use)
                self.player.start_animation()
                self.player.show()
            except Exception as e:
                print(f"Error loading animation for {character.name}: {e}")

            # Configure window with scaling / Configura finestra con scaling
            self.window.resize(scaled_width, scaled_height)

            # Apply click-through mode / Applica click-through mode
            self.window.set_click_through(character.locked)

            # Create appropriate behavior with scaled dimensions / Crea comportamento appropriato con dimensioni scalate
            self.setup_behavior(scaled_width, scaled_height)

            # Play audio if present / Riproduci audio se presente e abilitato
            if character.has_audio() and character.config.get("play_audio_on_startup", True):
                self.audio_manager.play_sound(character.get_audio_path(), character.volume)

            # Applica schermo preferito se assegnato (stile Wallpaper Engine)
            pref_screen_name = character.config.get("preferred_screen")
            if pref_screen_name and pref_screen_name != "auto":
                for s in QGuiApplication.screens():
                    if s.name() == pref_screen_name:
                        curr_s = QGuiApplication.screenAt(self.window.geometry().center())
                        if curr_s != s:
                            self.move_to_screen(s)
                        break
        except Exception:
            self.cleanup()
            raise

    def _teardown_behavior(self):
        """Pulisce e distrugge il comportamento attivo disconnettendo i segnali dalla finestra."""
        if self.behavior:
            try:
                self.behavior.stop_behavior()
            except Exception:
                pass
            self.behavior = None

        # Disconnetti tutti i vecchi listener dei segnali di trascinamento della finestra
        for signal in (self.window.drag_started, self.window.position_changed, self.window.drag_ended):
            try:
                signal.disconnect()
            except (TypeError, RuntimeError):
                pass

    def setup_behavior(self, width, height):
        """Configure character behavior / Configura il comportamento del personaggio."""
        self._teardown_behavior()
        self.window.allow_offscreen = (self.character.behavior == "random_edge")
        self.window.safe_overflow = (self.character.behavior == "static")

        # Se non è statico e non è random_edge, assicura che il personaggio sia entro i limiti rigidi dello schermo
        if not self.window.safe_overflow and not self.window.allow_offscreen:
            clamped = self.window.clamp_to_screen(self.window.pos())
            if self.window.pos() != clamped:
                self.window.move(clamped)
        if self.character.behavior == "free_walk":
            self.behavior = FreeWalkBehavior(width, height)
            self.behavior.position_signal.connect(self.window.move)
            self.window.drag_started.connect(lambda: self.behavior.set_dragging(True))
            self.window.position_changed.connect(self.behavior.update_position)
            self.window.drag_ended.connect(self._on_free_walk_drag_ended)
            self.behavior.start_behavior()
        elif self.character.behavior == "random_edge":
            self.window.allow_offscreen = True
            self.behavior = RandomEdgeBehavior(width, height)
            self.behavior.position_signal.connect(self.window.move)
            self.behavior.show_signal.connect(self.window.show)
            self.behavior.hide_signal.connect(self.window.hide)
            self.window.drag_started.connect(lambda: self.behavior.set_dragging(True))
            self.window.position_changed.connect(self.behavior.update_position)
            self.window.drag_ended.connect(lambda x, y: self.behavior.set_dragging(False, x, y))
            self.behavior.start_behavior()
        elif self.character.behavior == "gravity":
            self.behavior = GravityBehavior(width, height)
            self.behavior.position_signal.connect(self.window.move)
            self.window.drag_started.connect(lambda: self.behavior.set_dragging(True))
            self.window.position_changed.connect(self.behavior.update_position)
            self.window.drag_ended.connect(self._on_gravity_drag_ended)
            self.behavior.start_behavior()
        else:
            # static: posizionamento fisso con salvataggio automatico della posizione al rilascio del drag
            saved_x = self.character.config.get("pos_x")
            saved_y = self.character.config.get("pos_y")
            if saved_x is not None and saved_y is not None:
                self.window.move(int(saved_x), int(saved_y))
            else:
                screen = get_current_screen()
                if screen:
                    geom = screen.geometry()
                    init_x = geom.x() + geom.width() - width - 40
                    init_y = geom.y() + geom.height() - height
                    self.window.move(init_x, init_y)

            def on_static_drag_ended(x, y):
                self.character.update_config(pos_x=x, pos_y=y)
                self.character.save_config()
                self._sync_screen_after_drag()

            self.window.drag_ended.connect(on_static_drag_ended)

    def _sync_screen_after_drag(self):
        """Rileva lo schermo su cui si trova il personaggio al rilascio del drag e sincronizza UI/config."""
        screen = QGuiApplication.screenAt(self.window.geometry().center())
        if not screen:
            screen = QApplication.primaryScreen()
        if screen:
            scr_name = screen.name()
            old_pref = self.character.config.get("preferred_screen")
            if old_pref and old_pref != "auto" and old_pref != scr_name:
                self.character.update_config(preferred_screen=scr_name)
                self.character.save_config()
            if self.overlay_app and self.overlay_app.launcher:
                self.overlay_app.launcher.update_character_screen_ui(self.character.name, scr_name)

    def _on_free_walk_drag_ended(self, x, y):
        """Handle drag end for free walk: stop dragging and fall to ground if in air."""
        if self.behavior and isinstance(self.behavior, FreeWalkBehavior):
            self.behavior.set_dragging(False)
            self.behavior.fall_to_bottom()
        self._sync_screen_after_drag()

    def _on_gravity_drag_ended(self, x, y):
        """Handle drag end for gravity: stop dragging and sync screen."""
        if self.behavior and isinstance(self.behavior, GravityBehavior):
            self.behavior.set_dragging(False)
        self._sync_screen_after_drag()

    def show(self):
        """Show the character / Mostra il personaggio."""
        if self.character.behavior != "random_edge":
            self.window.show()
        if self.behavior:
            if hasattr(self.behavior, "resume_behavior"):
                self.behavior.resume_behavior()
            elif hasattr(self.behavior, "start_behavior"):
                self.behavior.start_behavior()
        if hasattr(self.player, "start_animation") and self.window.isVisible():
            self.player.start_animation()

    def hide(self):
        """Hide the character / Nasconde il personaggio."""
        self.window.hide()
        if self.behavior:
            self.behavior.stop_behavior()
        if hasattr(self.player, "stop_animation"):
            self.player.stop_animation()

    def cleanup(self):
        """Clean up resources / Pulisce le risorse."""
        self._teardown_behavior()
        self.audio_manager.stop()
        self.window.close()

    def show_context_menu(self, pos: QPoint):
        """Apre il menu contestuale rapido in stile Cyber Glass sul desktop."""
        if self.character.locked:
            return

        menu = QMenu(self.window)
        menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        checkmark_path = resource_path("loghi/checkmark.png").replace("\\", "/")

        menu.setStyleSheet(f"""
            QMenu {{
                background-color: rgba(13, 20, 36, 0.96);
                border: 1px solid rgba(99, 102, 241, 0.35);
                border-radius: 12px;
                padding: 6px;
                color: #F1F5F9;
                font-family: 'Segoe UI', system-ui, sans-serif;
                font-size: 13px;
            }}
            QMenu::item {{
                background-color: transparent;
                padding: 7px 22px 7px 12px;
                border-radius: 6px;
                margin: 1px 2px;
                color: #E2E8F0;
            }}
            QMenu::item:selected {{
                background-color: rgba(99, 102, 241, 0.3);
                color: #FFFFFF;
            }}
            QMenu::item:disabled {{
                color: #94A3B8;
                font-weight: 700;
            }}
            QMenu::separator {{
                height: 1px;
                background: rgba(255, 255, 255, 0.1);
                margin: 4px 6px;
            }}
            QMenu::indicator {{
                width: 14px;
                height: 14px;
                margin-left: 4px;
            }}
            QMenu::indicator:checked {{
                image: url("{checkmark_path}");
            }}
        """)

        # 1. Header con il nome del personaggio
        header_action = QAction(f"{self.character.name}", menu)
        header_action.setEnabled(False)
        menu.addAction(header_action)
        menu.addSeparator()

        # 2. Riproduci audio (se presente)
        if self.character.has_audio():
            play_audio_text = self.translations.get("ctx_play_audio", "Riproduci audio") if self.translations else "Riproduci audio"
            audio_action = QAction(make_icon("volume", "#6366F1", 16), play_audio_text, menu)
            audio_action.triggered.connect(lambda: self.audio_manager.play_sound(self.character.get_audio_path(), self.character.volume))
            menu.addAction(audio_action)

        # 3. Sottomenu Cambia Comportamento
        behavior_menu_text = self.translations.get("ctx_behavior", "Comportamento") if self.translations else "Comportamento"
        behavior_menu = menu.addMenu(behavior_menu_text)
        behavior_menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        behavior_menu.setIcon(make_icon("settings", "#818CF8", 16))

        behaviors_list = [
            ("static", self.translations.get("behavior_static", "Statico") if self.translations else "Statico"),
            ("free_walk", self.translations.get("behavior_free_walk", "Cammino Libero") if self.translations else "Cammino Libero"),
            ("gravity", self.translations.get("behavior_gravity", "Gravità") if self.translations else "Gravità"),
            ("random_edge", self.translations.get("behavior_random_edge", "Sbircia dai bordi") if self.translations else "Sbircia dai bordi"),
        ]

        for b_id, b_label in behaviors_list:
            b_action = QAction(b_label, behavior_menu)
            b_action.setCheckable(True)
            b_action.setChecked(self.character.behavior == b_id)
            b_action.triggered.connect(lambda checked, target_b=b_id: self.change_behavior(target_b))
            behavior_menu.addAction(b_action)

        # 4. Sposta su Schermo (mostrato solo se ci sono 2 o più schermi collegati)
        screens = QGuiApplication.screens()
        if len(screens) > 1:
            current_screen = QGuiApplication.screenAt(self.window.geometry().center())
            move_menu_text = self.translations.get("ctx_move_to_screen", "Sposta su Schermo") if self.translations else "Sposta su Schermo"
            screen_menu = menu.addMenu(move_menu_text)
            screen_menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            screen_menu.setIcon(make_icon("monitor", "#06B6D4", 16))

            primary_screen = QApplication.primaryScreen()
            primary_tag = self.translations.get("screen_primary", "Principale") if self.translations else "Principale"

            screen_num_tmpl = self.translations.get("screen_num", "Schermo {i}") if self.translations else "Schermo {i}"
            for i, scr in enumerate(screens, start=1):
                is_current = (scr == current_screen)
                scr_name = scr.name()
                is_primary = (scr == primary_screen)
                tag = f" ({primary_tag})" if is_primary else ""
                screen_prefix = screen_num_tmpl.format(i=i) if "{i}" in screen_num_tmpl else f"Schermo {i}"
                label = f"{screen_prefix}: {scr_name}{tag}"
                scr_action = QAction(label, screen_menu)
                scr_action.setCheckable(True)
                scr_action.setChecked(is_current)
                scr_action.setEnabled(not is_current)
                scr_action.triggered.connect(lambda checked, s=scr: self.move_to_screen(s))
                screen_menu.addAction(scr_action)

        menu.addSeparator()

        # 5. Blocca sul desktop (click-through)
        lock_text = self.translations.get("ctx_lock", "Blocca sul desktop") if self.translations else "Blocca sul desktop"
        lock_action = QAction(make_icon("lock", "#F59E0B", 16), lock_text, menu)
        lock_action.triggered.connect(self.lock_character)
        menu.addAction(lock_action)

        # 5. Modifica nel Launcher
        launcher_text = self.translations.get("ctx_open_launcher", "Modifica nel Launcher") if self.translations else "Modifica nel Launcher"
        open_launcher_action = QAction(make_icon("edit", "#38BDF8", 16), launcher_text, menu)
        open_launcher_action.triggered.connect(self.open_in_launcher)
        menu.addAction(open_launcher_action)

        menu.addSeparator()

        # 6. Rimuovi dal Desktop
        remove_text = self.translations.get("ctx_remove_desktop", "Rimuovi dal desktop") if self.translations else "Rimuovi dal desktop"
        remove_action = QAction(make_icon("trash", "#EF4444", 16), remove_text, menu)
        remove_action.triggered.connect(self.remove_from_desktop)
        menu.addAction(remove_action)

        menu.exec(pos)

    def move_to_screen(self, target_screen):
        """Sposta il personaggio su un altro monitor preservando l'allineamento a terra e relativo."""
        if not target_screen:
            return

        current_screen = QGuiApplication.screenAt(self.window.geometry().center())
        if not current_screen:
            current_screen = QApplication.primaryScreen()

        geom_from = current_screen.geometry() if current_screen else target_screen.geometry()
        geom_to = target_screen.geometry()

        # Calcola posizione relativa orizzontale
        from_width_span = max(1, geom_from.width() - self.window.width())
        rel_x = (self.window.x() - geom_from.x()) / from_width_span
        rel_x = max(0.0, min(1.0, rel_x))

        new_x = int(geom_to.x() + rel_x * (geom_to.width() - self.window.width()))

        # Calcola distanza dal fondo (allineamento pavimento / taskbar)
        bottom_offset = (geom_from.y() + geom_from.height()) - (self.window.y() + self.window.height())
        bottom_offset = max(0, min(geom_to.height() - self.window.height(), bottom_offset))
        new_y = int(geom_to.y() + geom_to.height() - self.window.height() - bottom_offset)

        clamped = self.window.clamp_to_screen(QPoint(new_x, new_y))
        self.window.move(clamped)

        # Aggiorna coordinate nel comportamento attivo se presente
        if self.behavior:
            if hasattr(self.behavior, "current_x"):
                self.behavior.current_x = clamped.x()
            if hasattr(self.behavior, "current_y"):
                self.behavior.current_y = clamped.y()

        # Salva la nuova posizione e preferenza
        self.character.update_config(pos_x=clamped.x(), pos_y=clamped.y(), preferred_screen=target_screen.name())
        self.character.save_config()

        # Sincronizza il launcher se aperto
        if self.overlay_app and self.overlay_app.launcher:
            self.overlay_app.launcher.update_character_screen_ui(self.character.name, target_screen.name())

    def change_behavior(self, new_behavior: str):
        """Cambia il comportamento del personaggio al volo."""
        if self.character.behavior == new_behavior:
            return

        self._teardown_behavior()

        self.character.update_config(behavior=new_behavior)
        self.character.save_config()
        self.character.behavior = new_behavior

        scale_factor = (self.character.scale or 100) / 100
        scaled_width = int(self.character.width * scale_factor)
        scaled_height = int(self.character.height * scale_factor)

        self.setup_behavior(scaled_width, scaled_height)

        # Sincronizza il launcher se aperto
        if self.overlay_app and self.overlay_app.launcher:
            if self.overlay_app.launcher.selected_character == self.character.name:
                self.overlay_app.launcher.on_character_selected(self.character.name)

    def lock_character(self):
        """Attiva il blocco (click-through) e notifica l'utente."""
        self.character.update_config(locked=True)
        self.character.save_config()
        self.character.locked = True
        self.window.set_click_through(True)

        if self.overlay_app:
            if self.overlay_app.launcher:
                self.overlay_app.launcher.on_character_lock(self.character.name, True)
            if self.overlay_app.tray_manager:
                title = self.translations.get("ctx_locked_notification_title", "Personaggio Bloccato") if self.translations else "Personaggio Bloccato"
                template = self.translations.get("ctx_locked_notification_msg", "\"{name}\" è ora trasparente ai clic.\nPuoi sbloccarlo dal Launcher.") if self.translations else "\"{name}\" è ora trasparente ai clic.\nPuoi sbloccarlo dal Launcher."
                self.overlay_app.tray_manager.show_message(title, template.format(name=self.character.name), duration=4000)

    def open_in_launcher(self):
        """Apre il launcher e seleziona subito questo personaggio."""
        if self.overlay_app:
            self.overlay_app.open_launcher()
            if self.overlay_app.launcher:
                self.overlay_app.launcher.on_character_selected(self.character.name)
                self.overlay_app.launcher.raise_()
                self.overlay_app.launcher.activateWindow()

    def remove_from_desktop(self):
        """Disattiva e chiude il personaggio dal desktop."""
        if self.overlay_app:
            self.overlay_app.deactivate_character(self.character.name)
            if self.overlay_app.launcher:
                self.overlay_app.launcher.update_active_characters(list(self.overlay_app.active_characters.keys()))


if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes
    from PyQt6.QtCore import QAbstractNativeEventFilter

    WM_HOTKEY = 0x0312
    MOD_ALT = 0x0001
    MOD_CONTROL = 0x0002
    MOD_NOREPEAT = 0x4000
    VK_H = 0x48
    HOTKEY_ID_TOGGLE_ALL = 1001

    class GlobalHotkeyFilter(QAbstractNativeEventFilter):
        """Filtro eventi nativi Windows per catturare la scorciatoia da tastiera globale Ctrl+Alt+H."""
        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        def nativeEventFilter(self, event_type, message):
            if "windows_generic_MSG" in str(event_type):
                msg = wintypes.MSG.from_address(int(message))
                if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID_TOGGLE_ALL:
                    self.callback()
                    return True, 0
            return False, 0


class AnimaOverlayApp:
    """Main application for Anima Overlay / Applicazione principale per Anima Overlay."""

    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Set application icon for Windows taskbar / Imposta icona dell'applicazione per la barra di Windows
        app_icon = resource_path("loghi/icon.ico")
        if os.path.exists(app_icon):
            self.app.setWindowIcon(QIcon(app_icon))

        # Remove any leftover local server from abnormal shutdown / Rimuovi eventuale server locale residuo da chiusura anomala
        QLocalServer.removeServer("AuraLayerIPC")

        # Create local server for IPC (to receive requests from other instances) / Crea server locale per IPC (per ricevere richieste da altre istanze)
        self.ipc_server = QLocalServer()
        if not self.ipc_server.listen("AuraLayerIPC"):
            print(f"Warning: IPC server not started: {self.ipc_server.errorString()}")
        self.ipc_server.newConnection.connect(self._on_ipc_connection)

        # Migrate data from local folder to APPDATA if needed / Migra dati dalla cartella locale a APPDATA se necessario
        migrate_from_local_if_needed()

        # Initialize managers (now automatically use APPDATA) / Inizializza manager (ora usano automaticamente APPDATA)
        self.character_manager = CharacterManager()
        self.config_manager = ConfigManager()

        # Initialize translation system / Inizializza sistema traduzioni
        try:
            language = self.config_manager.get_global_setting("language", "it")
            self.translations = init_translations(language)
        except Exception as e:
            print(f"Error initializing translations: {e}")
            # Fallback to simple translations without translation system
            self.translations = None

        # Pass translations to tray manager only if available
        if self.translations:
            self.tray_manager = TrayManager(self.translations)
        else:
            self.tray_manager = TrayManager(None)

        # Create launcher passing shared CharacterManager and translations / Crea launcher passando CharacterManager condiviso e traduzioni
        self.launcher = LauncherWindow(self.character_manager, self.config_manager, self.translations)
        self.launcher.character_launched.connect(self.on_launcher_launch)
        self.launcher.character_deactivated.connect(self.on_launcher_deactivate)
        self.launcher.character_removed.connect(self.on_launcher_remove)
        self.launcher.character_renamed.connect(self.on_launcher_rename)
        self.launcher.character_updated.connect(self.on_launcher_update)
        self.launcher.character_lock_changed.connect(self.on_launcher_lock)
        self.launcher.character_screen_changed.connect(self.on_launcher_screen_changed)
        self.launcher.global_fps_changed.connect(self.on_global_fps_changed)
        self.launcher.fullscreen_pause_changed.connect(self.on_fullscreen_pause_changed)
        self.launcher.quit_requested.connect(self.quit_app)

        # Active characters / Personaggi attivi
        self.active_characters: Dict[str, ActiveCharacter] = {}
        self.all_hidden = False  # State for show/hide all toggle / Stato per toggle mostra/nascondi tutti
        self._fullscreen_paused = False

        # Timer per pausa automatica se un'app/gioco va a tutto schermo (fullscreen detection)
        # Avviato solo se abilitato nelle impostazioni per azzerare cicli CPU a vuoto
        self.fullscreen_timer = QTimer()
        self.fullscreen_timer.timeout.connect(self._check_fullscreen)
        if self.config_manager.get_global_setting("fullscreen_pause", False):
            self.fullscreen_timer.start(1500)

        # Connect tray signals / Connetti segnali tray
        self.tray_manager.quit_signal.connect(self.quit_app)
        self.tray_manager.open_launcher_signal.connect(self.open_launcher)
        self.tray_manager.toggle_all_signal.connect(self.toggle_all_characters)
        self.tray_manager.unlock_all_signal.connect(self.unlock_all_characters)

        # Salvagente rimozione schermo (spegnimento o disconnessione cavo monitor)
        self.app.screenRemoved.connect(self.on_screen_removed)

        # Setup hotkey globale Windows (Ctrl+Alt+H per mostrare/nascondere tutti i personaggi)
        self.hotkey_filter = None
        self._setup_global_hotkey()

        # Create tray icon with logo / Crea tray icon con logo
        logo_path = resource_path("loghi/logo_mini.png")
        self.tray_manager.create_tray_icon(logo_path)

        # Load active characters from configuration / Carica personaggi attivi dalla configurazione
        self.load_active_characters()

    def _setup_global_hotkey(self):
        """Registra la scorciatoia da tastiera globale di sistema Ctrl+Alt+H su Windows."""
        if sys.platform != "win32":
            return
        try:
            user32 = ctypes.windll.user32
            user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_uint, ctypes.c_uint]
            user32.RegisterHotKey.restype = wintypes.BOOL
            user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
            user32.UnregisterHotKey.restype = wintypes.BOOL

            self.hotkey_filter = GlobalHotkeyFilter(self.toggle_all_characters)
            self.app.installNativeEventFilter(self.hotkey_filter)

            # Prova registrazione con MOD_NOREPEAT (evita flickering tenendo premuto)
            res = user32.RegisterHotKey(None, HOTKEY_ID_TOGGLE_ALL, MOD_CONTROL | MOD_ALT | MOD_NOREPEAT, VK_H)
            if not res:
                # Fallback senza MOD_NOREPEAT
                res = user32.RegisterHotKey(None, HOTKEY_ID_TOGGLE_ALL, MOD_CONTROL | MOD_ALT, VK_H)
            if res:
                print("Global hotkey Ctrl+Alt+H successfully registered.")
            else:
                print("Warning: Global hotkey Ctrl+Alt+H could not be registered (may be in use by another app).")
        except Exception as e:
            print(f"Error registering global hotkey: {e}")
        
    def load_active_characters(self):
        """Carica e avvia i personaggi che erano attivi all'ultima chiusura con ripristino sicuro auto-healing."""
        active_names = list(self.config_manager.get_active_characters())
        for name in active_names:
            try:
                char = self.character_manager.get_character(name)
                if char:
                    self.activate_character(char)
                else:
                    # Rimuovi solo se il personaggio non esiste più fisicamente sul disco
                    self.config_manager.remove_active_character(name)
            except Exception:
                # Registra l'errore nel crash log senza cancellare la sessione in caso di errore temporaneo
                sys.excepthook(*sys.exc_info())

        if self.launcher:
            self.launcher.update_active_characters(list(self.active_characters.keys()))

    def activate_character(self, character):
        """Activate a character / Attiva un personaggio."""
        if character.name in self.active_characters:
            return

        active_char = ActiveCharacter(character, self.app, self.config_manager, translations=self.translations, overlay_app=self)
        self.active_characters[character.name] = active_char
        if not self.all_hidden and not self._fullscreen_paused:
            active_char.show()
        else:
            active_char.hide()

        # Update configuration / Aggiorna configurazione
        self.config_manager.add_active_character(character.name)

    def restart_character(self, character_name: str):
        """Restart a character (deactivate + reload config + activate) / Riavvia un personaggio (deactivate + reload config + activate)."""
        if character_name in self.active_characters:
            # Deactivate / Disattiva
            self.deactivate_character(character_name)
            # Reload character manager to get updated config / Ricarica character manager per avere config aggiornato
            self.character_manager.load_all_characters()
            # Reactivate / Riattiva
            character = self.character_manager.get_character(character_name)
            if character:
                self.activate_character(character)

    def deactivate_character(self, character_name: str):
        """Deactivate a character / Disattiva un personaggio."""
        if character_name in self.active_characters:
            self.active_characters[character_name].cleanup()
            del self.active_characters[character_name]

            # Update configuration / Aggiorna configurazione
            self.config_manager.remove_active_character(character_name)

    def toggle_all_characters(self):
        """Show/hide all active characters / Mostra/nasconde tutti i personaggi attivi."""
        if not self.active_characters:
            print("No active characters to show. Use launcher to activate them.")
            return

        if self.all_hidden:
            # Show all again / Ri mostra tutti
            for active_char in self.active_characters.values():
                active_char.show()
            self.all_hidden = False
        else:
            # Hide all / Nascondi tutti
            for active_char in self.active_characters.values():
                active_char.hide()
            self.all_hidden = True

    def open_launcher(self):
        """Open the launcher / Apre il launcher."""
        self.launcher.show()
        self.launcher.raise_()
        self.launcher.activateWindow()

    def on_launcher_launch(self, character_name: str):
        """Handle launch from launcher / Gestisce il lancio dal launcher."""
        # Reload character manager to get updated data / Ricarica character manager per avere i dati aggiornati
        self.character_manager.load_all_characters()
        character = self.character_manager.get_character(character_name)
        if character:
            self.activate_character(character)
            # Sincronizza lo stato di tutte le card della griglia e dei pulsanti nel launcher
            self.launcher.update_active_characters(list(self.active_characters.keys()))

    def on_launcher_deactivate(self, character_name: str):
        """Handle deactivation from launcher / Gestisce la disattivazione dal launcher."""
        self.deactivate_character(character_name)
        # Sincronizza lo stato di tutte le card della griglia e dei pulsanti nel launcher
        self.launcher.update_active_characters(list(self.active_characters.keys()))

    def unlock_all_characters(self):
        """Sblocca tutti i personaggi attivi sul desktop (rimuove il click-through)."""
        for active_char in self.active_characters.values():
            if active_char.character.locked:
                active_char.character.update_config(locked=False)
                active_char.character.save_config()
                active_char.character.locked = False
                active_char.window.set_click_through(False)

        if self.launcher and self.launcher.selected_character:
            self.launcher.on_character_selected(self.launcher.selected_character)

        msg = self.translations.get("msg_all_unlocked", "Tutti i personaggi sono stati sbloccati.") if self.translations else "Tutti i personaggi sono stati sbloccati."
        self.tray_manager.show_message("Aura Layer", msg, duration=3000)

    def on_launcher_remove(self, character_name: str):
        """Handle removal from launcher / Gestisce la rimozione dal launcher."""
        if character_name in self.active_characters:
            self.deactivate_character(character_name)
        self.character_manager.load_all_characters()
        self.launcher.update_counters()

    def on_launcher_rename(self, old_name: str, new_name: str):
        """Handle rename from launcher / Gestisce la rinomina dal launcher."""
        if old_name in self.active_characters:
            # Deactivate with old name / Disattiva con vecchio nome
            self.deactivate_character(old_name)
            # Reactivate with new name / Riattiva con nuovo nome
            self.character_manager.load_all_characters()
            character = self.character_manager.get_character(new_name)
            if character:
                self.activate_character(character)
        self.launcher.update_counters()

    def on_launcher_update(self, character_name: str):
        """Handle character update (behavior/FPS change) / Gestisce l'aggiornamento del personaggio (cambio comportamento/FPS)."""
        if character_name in self.active_characters:
            # Restart character with new config / Riavvia il personaggio con il nuovo config
            self.restart_character(character_name)

    def on_launcher_lock(self, character_name: str, locked: bool):
        """Handle lock change without restarting character / Gestisce il cambio lock senza riavviare il personaggio."""
        if character_name in self.active_characters:
            # Apply lock directly to existing window / Applica lock direttamente alla finestra esistente
            self.active_characters[character_name].window.set_click_through(locked)

    def on_launcher_screen_changed(self, character_name: str, screen_name: str):
        """Gestisce il cambio schermo dal Launcher per un personaggio attivo sul desktop."""
        if character_name in self.active_characters:
            active_char = self.active_characters[character_name]
            if screen_name and screen_name != "auto":
                for s in QGuiApplication.screens():
                    if s.name() == screen_name:
                        active_char.move_to_screen(s)
                        break

    def on_screen_removed(self, removed_screen):
        """Salvagente: se uno schermo viene spento o scollegato, riporta i personaggi rimasti isolati."""
        primary = QApplication.primaryScreen()
        if not primary:
            return
        repositioned = False
        valid_screens = QGuiApplication.screens()
        for active_char in self.active_characters.values():
            char_screen = QGuiApplication.screenAt(active_char.window.geometry().center())
            if char_screen is None or char_screen not in valid_screens:
                active_char.move_to_screen(primary)
                repositioned = True

        if repositioned:
            msg = self.translations.get("msg_screen_disconnected", "Uno schermo è stato scollegato. I personaggi sono stati riposizionati sul monitor principale.") if self.translations else "Uno schermo è stato scollegato. I personaggi sono stati riposizionati sul monitor principale."
            self.tray_manager.show_message("Aura Layer", msg, duration=4000)

    def on_global_fps_changed(self, limit: int):
        """Aggiorna il limite FPS in tempo reale per tutti i personaggi attivi."""
        for active_char in self.active_characters.values():
            char_fps = active_char.character.fps
            if char_fps is not None:
                fps_to_use = char_fps
                if limit > 0:
                    fps_to_use = min(fps_to_use, limit)
            else:
                fps_to_use = limit if limit > 0 else None
            active_char.player.set_fps(fps_to_use)

    def on_fullscreen_pause_changed(self, enabled: bool):
        """Attiva o disattiva il timer fullscreen per risparmiare risorse."""
        if enabled:
            if not self.fullscreen_timer.isActive():
                self.fullscreen_timer.start(1500)
        else:
            if self.fullscreen_timer.isActive():
                self.fullscreen_timer.stop()
            if self._fullscreen_paused:
                self._fullscreen_paused = False
                if not self.all_hidden:
                    for active_char in self.active_characters.values():
                        active_char.show()

    def _check_fullscreen(self):
        """Controlla se un'app o gioco è a tutto schermo e gestisce la pausa dei personaggi."""
        enabled = self.config_manager.get_global_setting("fullscreen_pause", False)
        if not enabled:
            if self.fullscreen_timer.isActive():
                self.fullscreen_timer.stop()
            if self._fullscreen_paused:
                self._fullscreen_paused = False
                if not self.all_hidden:
                    for active_char in self.active_characters.values():
                        active_char.show()
            return

        exclude_hwnds = []
        for active_char in self.active_characters.values():
            if active_char.window:
                try:
                    exclude_hwnds.append(int(active_char.window.winId()))
                except Exception:
                    pass
        if self.launcher:
            try:
                exclude_hwnds.append(int(self.launcher.winId()))
            except Exception:
                pass

        is_fs = is_fullscreen_active(exclude_hwnds)
        if is_fs and not self._fullscreen_paused:
            self._fullscreen_paused = True
            for active_char in self.active_characters.values():
                active_char.hide()
        elif not is_fs and self._fullscreen_paused:
            self._fullscreen_paused = False
            if not self.all_hidden:
                for active_char in self.active_characters.values():
                    active_char.show()

    def quit_app(self):
        """Exit the application / Esce dall'applicazione."""
        if hasattr(self, 'fullscreen_timer') and self.fullscreen_timer.isActive():
            self.fullscreen_timer.stop()

        # Clean up all active characters / Pulisci tutti i personaggi attivi
        for active_char in self.active_characters.values():
            active_char.cleanup()

        # Chiudi e rimuovi il server IPC locale per non lasciare pipe aperte
        if hasattr(self, 'ipc_server') and self.ipc_server:
            self.ipc_server.close()
            QLocalServer.removeServer("AuraLayerIPC")

        # Disregistra hotkey globale di sistema
        if sys.platform == "win32" and getattr(self, 'hotkey_filter', None):
            try:
                ctypes.windll.user32.UnregisterHotKey(None, HOTKEY_ID_TOGGLE_ALL)
                self.app.removeNativeEventFilter(self.hotkey_filter)
                self.hotkey_filter = None
            except Exception:
                pass

        self.tray_manager.hide()
        self.app.quit()

    def run(self):
        """Start the application / Avvia l'applicazione."""
        print("Aura Layer started.")
        print(f"Available characters: {', '.join(self.character_manager.get_character_names())}")

        # Check if should start minimized / Controlla se avviare minimizzato
        start_minimized = self.config_manager.get_global_setting("start_minimized", False)
        if not start_minimized:
            # Show launcher at startup (like Wallpaper Engine) / Mostra il launcher all'avvio (come Wallpaper Engine)
            self.open_launcher()
        else:
            print("Starting minimized - use system tray icon to open launcher.")

        print("Use launcher to select and start characters.")

        sys.exit(self.app.exec())

    def _on_ipc_connection(self):
        """Handle IPC connections from other app instances / Gestisce le connessioni IPC da altre istanze dell'app."""
        socket = self.ipc_server.nextPendingConnection()
        if socket.waitForReadyRead(1000):
            data = socket.readAll().data()
            if data == b"show":
                # Request to show launcher / Richiesta di mostrare il launcher
                self.open_launcher()
        socket.disconnectFromServer()


def main():
    """Application entry point / Entry point dell'applicazione."""
    # Installa il gestore globale di crash per registrare eccezioni in crash.log
    install_global_exception_handler()

    # Check if another instance is already running / Verifica se un'altra istanza è già in esecuzione
    if not check_single_instance():
        # Create minimal QCoreApplication to use QLocalSocket / Crea una QCoreApplication minima per usare QLocalSocket
        temp_app = QCoreApplication(sys.argv)

        # Connect to local server of first instance / Connetti al server locale della prima istanza
        socket = QLocalSocket()
        socket.connectToServer("AuraLayerIPC")

        if socket.waitForConnected(1000):
            # Send message to show launcher / Invia messaggio per mostrare il launcher
            socket.write(b"show")
            socket.flush()
            socket.waitForBytesWritten(1000)
            socket.disconnectFromServer()

        sys.exit(0)

    overlay_app = AnimaOverlayApp()
    overlay_app.run()


if __name__ == "__main__":
    main()
