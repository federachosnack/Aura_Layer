import sys
import os
from typing import Dict, Optional
from PyQt6.QtWidgets import QApplication, QMessageBox, QLabel, QFileDialog
from PyQt6.QtCore import Qt, QTimer, QCoreApplication
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtGui import QPainter, QColor, QFont, QAction, QIcon
from src.overlay_window import OverlayWindow
from src.animation_player import AnimationPlayer
from src.audio_manager import AudioManager
from src.behaviors import RandomEdgeBehavior, FreeWalkBehavior, GravityBehavior
from src.character import CharacterManager
from src.tray_manager import TrayManager
from src.config_manager import ConfigManager
from src.launcher import LauncherWindow
from src.utils import migrate_from_local_if_needed, check_single_instance, resource_path, is_fullscreen_active
from src.translations import init_translations


class ActiveCharacter:
    """Represents an active character with its window and behavior. / Rappresenta un personaggio attivo con la sua finestra e comportamento."""

    def __init__(self, character, app, config_manager=None):
        self.character = character
        self.app = app
        self.config_manager = config_manager
        self.window = OverlayWindow()
        self.player = AnimationPlayer(self.window)
        self.behavior = None
        self.audio_manager = AudioManager()

        # Calculate scaling once / Calcola scaling una volta sola
        scale_factor = (character.scale or 100) / 100
        scaled_width = int(character.width * scale_factor)
        scaled_height = int(character.height * scale_factor)

        # Load animation / Carica animazione
        try:
            self.player.load_animation(character.get_animation_path())
            self.player.set_size(scaled_width, scaled_height)
            # Set custom FPS if present, considering global limit / Imposta FPS personalizzato se presente, considerando il limite globale
            fps_to_use = character.fps if character.fps is not None else 24
            if self.config_manager:
                global_fps_limit = self.config_manager.get_global_setting("global_fps_limit", 0)
                if global_fps_limit > 0:
                    fps_to_use = min(fps_to_use, global_fps_limit)
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

        # Play audio if present / Riproduci audio se presente
        if character.has_audio():
            self.audio_manager.play_sound(character.get_audio_path(), character.volume)

    def setup_behavior(self, width, height):
        """Configure character behavior / Configura il comportamento del personaggio."""
        if self.character.behavior == "free_walk":
            self.behavior = FreeWalkBehavior(width, height)
            self.behavior.position_signal.connect(self.window.move)
            self.window.drag_started.connect(lambda: self.behavior.set_dragging(True))
            self.window.position_changed.connect(self.behavior.update_position)
            self.window.drag_ended.connect(self._on_free_walk_drag_ended)
            self.behavior.start_behavior()
        elif self.character.behavior == "random_edge":
            self.behavior = RandomEdgeBehavior(width, height)
            self.behavior.position_signal.connect(self.window.move)
            self.behavior.show_signal.connect(self.window.show)
            self.behavior.hide_signal.connect(self.window.hide)
            self.behavior.start_behavior()
        elif self.character.behavior == "gravity":
            self.behavior = GravityBehavior(width, height)
            self.behavior.position_signal.connect(self.window.move)
            self.window.drag_started.connect(lambda: self.behavior.set_dragging(True))
            self.window.position_changed.connect(self.behavior.update_position)
            self.window.drag_ended.connect(lambda x, y: self.behavior.set_dragging(False))
            self.behavior.start_behavior()
        else:
            # static: posizionamento fisso con salvataggio automatico della posizione al rilascio del drag
            saved_x = self.character.config.get("pos_x")
            saved_y = self.character.config.get("pos_y")
            if saved_x is not None and saved_y is not None:
                self.window.move(int(saved_x), int(saved_y))
            else:
                from src.behaviors import get_current_screen
                screen = get_current_screen()
                if screen:
                    geom = screen.geometry()
                    init_x = geom.x() + geom.width() - width - 40
                    init_y = geom.y() + geom.height() - height
                    self.window.move(init_x, init_y)

            def on_static_drag_ended(x, y):
                self.character.update_config(pos_x=x, pos_y=y)
                self.character.save_config()

            self.window.drag_ended.connect(on_static_drag_ended)

    def _on_free_walk_drag_ended(self, x, y):
        """Handle drag end for free walk: stop dragging and fall to ground if in air."""
        if self.behavior and isinstance(self.behavior, FreeWalkBehavior):
            self.behavior.set_dragging(False)
            self.behavior.fall_to_bottom()

    def show(self):
        """Show the character / Mostra il personaggio."""
        self.window.show()

    def hide(self):
        """Hide the character / Nasconde il personaggio."""
        self.window.hide()
        if self.behavior:
            self.behavior.stop_behavior()

    def cleanup(self):
        """Clean up resources / Pulisce le risorse."""
        if self.behavior:
            self.behavior.stop_behavior()
        self.audio_manager.stop()
        self.window.close()


class AnimaOverlayApp:
    """Main application for Anima Overlay / Applicazione principale per Anima Overlay."""

    def __init__(self):
        self.app = QApplication(sys.argv)
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
        self.launcher.global_fps_changed.connect(self.on_global_fps_changed)
        self.launcher.quit_requested.connect(self.quit_app)

        # Active characters / Personaggi attivi
        self.active_characters: Dict[str, ActiveCharacter] = {}
        self.all_hidden = False  # State for show/hide all toggle / Stato per toggle mostra/nascondi tutti
        self._fullscreen_paused = False

        # Timer per pausa automatica se un'app/gioco va a tutto schermo (fullscreen detection)
        self.fullscreen_timer = QTimer()
        self.fullscreen_timer.timeout.connect(self._check_fullscreen)
        self.fullscreen_timer.start(1500)

        # Connect tray signals / Connetti segnali tray
        self.tray_manager.quit_signal.connect(self.quit_app)
        self.tray_manager.open_launcher_signal.connect(self.open_launcher)
        self.tray_manager.toggle_all_signal.connect(self.toggle_all_characters)

        # Create tray icon with logo / Crea tray icon con logo
        logo_path = resource_path("loghi/logo_mini.png")
        self.tray_manager.create_tray_icon(logo_path)

        # Load active characters from configuration / Carica personaggi attivi dalla configurazione
        self.load_active_characters()
        
    def load_active_characters(self):
        """Don't load active characters at startup - user must select them from launcher / Non carica personaggi attivi all'avvio - l'utente deve selezionarli dal launcher."""
        pass

    def activate_character(self, character):
        """Activate a character / Attiva un personaggio."""
        if character.name in self.active_characters:
            return

        active_char = ActiveCharacter(character, self.app, self.config_manager)
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
            # Update state in launcher / Aggiorna stato nel launcher
            self.launcher.active_characters.add(character_name)
            self.launcher.update_button_states()
            self.launcher.update_counters()

    def on_launcher_deactivate(self, character_name: str):
        """Handle deactivation from launcher / Gestisce la disattivazione dal launcher."""
        self.deactivate_character(character_name)
        # Update state in launcher / Aggiorna stato nel launcher
        if character_name in self.launcher.active_characters:
            self.launcher.active_characters.remove(character_name)
        self.launcher.update_button_states()
        self.launcher.update_counters()

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

    def on_global_fps_changed(self, limit: int):
        """Aggiorna il limite FPS in tempo reale per tutti i personaggi attivi."""
        for active_char in self.active_characters.values():
            char_fps = active_char.character.fps if active_char.character.fps is not None else 24
            fps_to_use = char_fps
            if limit > 0:
                fps_to_use = min(fps_to_use, limit)
            active_char.player.set_fps(fps_to_use)

    def _check_fullscreen(self):
        """Controlla se un'app o gioco è a tutto schermo e gestisce la pausa dei personaggi."""
        enabled = self.config_manager.get_global_setting("fullscreen_pause", False)
        if not enabled:
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

        self.tray_manager.hide()
        self.app.quit()

    def run(self):
        """Start the application / Avvia l'applicazione."""
        print("Anima Overlay started.")
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
