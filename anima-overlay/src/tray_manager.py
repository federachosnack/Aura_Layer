from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QObject, pyqtSignal
import os


class TrayManager(QObject):
    """Manages system tray icon and context menu / Gestisce l'icona nella system tray e il menu contestuale."""

    # Signals / Segnali
    quit_signal = pyqtSignal()
    open_launcher_signal = pyqtSignal()
    toggle_all_signal = pyqtSignal()  # Show/Hide All / Mostra/Nascondi tutti
    unlock_all_signal = pyqtSignal()  # Unlock all characters / Sblocca tutti i personaggi

    def __init__(self, translations=None, parent=None):
        super().__init__(parent)
        self.tray_icon = None
        self.menu = None
        self.translations = translations
        
    def create_tray_icon(self, icon_path=None):
        """Create system tray icon / Crea l'icona nella system tray."""
        self.tray_icon = QSystemTrayIcon(self)

        # If no custom icon, use default / Se non c'è icona personalizzata, usa quella di default
        if icon_path and os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # Create simple default icon / Crea un'icona di default semplice
            from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(100, 150, 255))
            painter = QPainter(pixmap)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(4, 4, 24, 24)
            painter.end()
            self.tray_icon.setIcon(QIcon(pixmap))

        self.create_menu()
        self.tray_icon.setContextMenu(self.menu)

        # Force icon display / Forza la visualizzazione dell'icona
        self.tray_icon.show()

        # Check if system supports tray icons / Verifica se il sistema supporta le tray icons
        if not self.tray_icon.isSystemTrayAvailable():
            print("WARNING: System tray not available on this system")
        else:
            print("System tray icon created successfully")
        
    def create_menu(self):
        """Create context menu for tray icon / Crea il menu contestuale della tray icon."""
        self.menu = QMenu()

        # Menu item to open launcher / Voce per aprire launcher
        open_launcher_text = self.translations.get("tray_open_launcher", "Apri Launcher") if self.translations else "Apri Launcher"
        open_launcher_action = QAction(open_launcher_text, self.menu)
        open_launcher_action.triggered.connect(self.open_launcher_signal.emit)
        self.menu.addAction(open_launcher_action)

        self.menu.addSeparator()

        # Menu item to show/hide all / Voce per mostrare/nascondere tutti
        toggle_all_text = self.translations.get("tray_toggle_all", "Mostra/Nascondi Tutti") if self.translations else "Mostra/Nascondi Tutti"
        toggle_all_action = QAction(toggle_all_text, self.menu)
        toggle_all_action.triggered.connect(self.toggle_all_signal.emit)
        self.menu.addAction(toggle_all_action)

        # Menu item to unlock all / Voce per sbloccare tutti i personaggi
        unlock_all_text = self.translations.get("tray_unlock_all", "Sblocca tutti i personaggi") if self.translations else "Sblocca tutti i personaggi"
        unlock_all_action = QAction(unlock_all_text, self.menu)
        unlock_all_action.triggered.connect(self.unlock_all_signal.emit)
        self.menu.addAction(unlock_all_action)

        self.menu.addSeparator()

        # Menu item to quit / Voce per uscire
        quit_text = self.translations.get("tray_quit", "Esci") if self.translations else "Esci"
        quit_action = QAction(quit_text, self.menu)
        quit_action.triggered.connect(self.quit_signal.emit)
        self.menu.addAction(quit_action)

    def show_message(self, title: str, message: str, duration=3000):
        """Show balloon notification from tray icon / Mostra una notifica balloon dalla tray icon."""
        if self.tray_icon:
            self.tray_icon.showMessage(title, message, duration)

    def hide(self):
        """Hide tray icon / Nasconde l'icona della tray."""
        if self.tray_icon:
            self.tray_icon.hide()
