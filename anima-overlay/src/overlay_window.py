from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer
from PyQt6.QtGui import QMouseEvent, QGuiApplication, QCursor
import ctypes
from ctypes import wintypes

# Costanti Win32 per SetWindowPos
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOACTIVATE = 0x0010

# Costanti Win32 per SetWinEventHook
EVENT_SYSTEM_FOREGROUND = 3
WINEVENT_OUTOFCONTEXT = 0x0000

# Costanti Win32 per click-through
GWL_EXSTYLE = -20
WS_EX_TRANSPARENT = 0x00000020
WS_EX_LAYERED = 0x00080000

# Definizione tipo callback per WinEventHook
WinEventProc = ctypes.CFUNCTYPE(
    None,
    wintypes.HWND,  # hWinEventHook
    wintypes.DWORD,  # event
    wintypes.HWND,   # hwnd
    wintypes.LONG,   # idObject
    wintypes.LONG,   # idChild
    wintypes.DWORD,  # idThread
    wintypes.DWORD   # dwmsEventTime
)


class OverlayWindow(QWidget):
    """Finestra overlay trasparente, senza bordi, always-on-top."""
    
    # Segnali per comunicare con i comportamenti
    drag_started = pyqtSignal()
    drag_ended = pyqtSignal(int, int)  # x, y posizione finale
    position_changed = pyqtSignal(int, int)  # x, y durante drag
    
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.drag_position = None
        self.is_click_through = False

        # Riferimento al callback per evitare garbage collection
        self._win_event_callback = None
        self._event_hook = None

        # Timer ridotto a 300ms come fallback
        self.topmost_timer = QTimer()
        self.topmost_timer.timeout.connect(self.force_topmost)
        self.topmost_timer.start(300)

        # Imposta hook per reagire immediatamente ai cambiamenti di focus
        self.setup_foreground_hook()
        
    def setup_window(self):
        """Configura la finestra come overlay trasparente."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

    def force_topmost(self):
        """Riasserisce lo stato topmost usando API Win32 per z-order affidabile."""
        hwnd = int(self.winId())

        # Imposta argtypes per corretto marshalling su 64-bit
        user32 = ctypes.windll.user32
        user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
        user32.SetWindowPos.restype = wintypes.BOOL

        result = user32.SetWindowPos(
            hwnd, HWND_TOPMOST, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
        )

        if not result:
            error_code = ctypes.GetLastError()
            print(f"SetWindowPos fallito, codice errore: {error_code}")

    def setup_foreground_hook(self):
        """Imposta hook WinEvent per reagire ai cambiamenti di finestra in foreground."""
        # Callback che chiama force_topmost quando cambia finestra
        def foreground_callback(hWinEventHook, event, hwnd, idObject, idChild, idThread, dwmsEventTime):
            try:
                if event == EVENT_SYSTEM_FOREGROUND:
                    self.force_topmost()
            except Exception as e:
                # Callback nativo: logga errore ma non propagare eccezione
                print(f"Error in foreground_callback: {e}")

        # Crea e mantiene riferimento al callback
        self._win_event_callback = WinEventProc(foreground_callback)

        # Imposta hook con argtypes corretti
        user32 = ctypes.windll.user32
        user32.SetWinEventHook.argtypes = [wintypes.UINT, wintypes.UINT, wintypes.HMODULE, WinEventProc, wintypes.DWORD, wintypes.DWORD, wintypes.UINT]
        user32.SetWinEventHook.restype = wintypes.HANDLE

        self._event_hook = user32.SetWinEventHook(
            EVENT_SYSTEM_FOREGROUND,
            EVENT_SYSTEM_FOREGROUND,
            0,
            self._win_event_callback,
            0,
            0,
            WINEVENT_OUTOFCONTEXT
        )

        if not self._event_hook:
            print("Warning: Failed to set WinEventHook, using timer only")

    def cleanup_hook(self):
        """Pulisce l'hook quando la finestra viene distrutta."""
        if self._event_hook:
            user32 = ctypes.windll.user32
            user32.UnhookWinEvent.argtypes = [wintypes.HANDLE]
            user32.UnhookWinEvent.restype = wintypes.BOOL
            user32.UnhookWinEvent(self._event_hook)
            self._event_hook = None
        self._win_event_callback = None

    def closeEvent(self, event):
        """Pulisce risorse alla chiusura."""
        self.cleanup_hook()
        super().closeEvent(event)

    def set_click_through(self, enabled: bool):
        """Attiva/disattiva la modalità click-through (mouse trasparente)."""
        hwnd = int(self.winId())
        user32 = ctypes.windll.user32
        user32.GetWindowLongPtrW.restype = ctypes.c_longlong
        user32.GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
        user32.SetWindowLongPtrW.restype = ctypes.c_longlong
        user32.SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_longlong]

        current_style = user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        if enabled:
            new_style = current_style | WS_EX_TRANSPARENT | WS_EX_LAYERED
        else:
            new_style = current_style & ~WS_EX_TRANSPARENT
        user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, new_style)
        self.is_click_through = enabled

    def clamp_to_screen(self, pos: QPoint) -> QPoint:
        """
        Limita la posizione della finestra all'area visibile del monitor (screen.geometry).
        Consente al personaggio di posizionarsi sopra la barra di Windows,
        fermandosi a filo con il bordo inferiore del monitor senza essere tagliato.
        """
        # Se stiamo trascinando col mouse, usiamo lo schermo dove si trova il cursore
        screen = None
        if self.drag_position is not None:
            screen = QGuiApplication.screenAt(QCursor.pos())

        if not screen:
            center_point = QPoint(pos.x() + self.width() // 2, pos.y() + self.height() // 2)
            screen = QGuiApplication.screenAt(center_point)

        if not screen:
            screen = QApplication.primaryScreen()

        if not screen:
            return pos

        geom = screen.geometry()
        min_x = geom.x()
        max_x = geom.x() + geom.width() - self.width()
        min_y = geom.y()
        max_y = geom.y() + geom.height() - self.height()

        if max_x < min_x:
            max_x = min_x
        if max_y < min_y:
            max_y = min_y

        clamped_x = max(min_x, min(max_x, pos.x()))
        clamped_y = max(min_y, min(max_y, pos.y()))
        return QPoint(clamped_x, clamped_y)

    def move(self, *args):
        """Sposta la finestra garantendo che rimanga sempre all'interno del monitor (a filo sul fondo)."""
        if len(args) == 1 and isinstance(args[0], QPoint):
            clamped = self.clamp_to_screen(args[0])
            super().move(clamped)
        elif len(args) == 2:
            clamped = self.clamp_to_screen(QPoint(int(args[0]), int(args[1])))
            super().move(clamped)
        else:
            super().move(*args)

    def showEvent(self, event):
        super().showEvent(event)
        # Assicura che la finestra appena mostrata non sia fuori schermo
        clamped = self.clamp_to_screen(self.pos())
        if self.pos() != clamped:
            super().move(clamped)
        self.force_topmost()

    def mousePressEvent(self, event: QMouseEvent):
        """Gestisce l'inizio del trascinamento."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.drag_started.emit()
            self.force_topmost()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Gestisce il trascinamento della finestra con clamping sul monitor (può andare sopra la barra)."""
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
            current_pos = self.pos()
            self.position_changed.emit(current_pos.x(), current_pos.y())
            self.force_topmost()
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Termina il trascinamento garantendo che sia a filo con i bordi e in primo piano rispetto alla barra."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            clamped_pos = self.clamp_to_screen(self.pos())
            super().move(clamped_pos)
            self.drag_ended.emit(clamped_pos.x(), clamped_pos.y())
            self.force_topmost()
            event.accept()
