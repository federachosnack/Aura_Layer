import random
from PyQt6.QtCore import QTimer, QObject, pyqtSignal, QPoint
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication, QCursor


def get_screen_for_point(x: int, y: int):
    """Restituisce lo schermo che contiene il punto (x, y), oppure il primaryScreen di fallback."""
    screen = QGuiApplication.screenAt(QPoint(int(x), int(y)))
    if screen:
        return screen
    return QApplication.primaryScreen()


def get_current_screen():
    """Restituisce lo schermo dove si trova attualmente il cursore del mouse, o il primaryScreen."""
    screen = QGuiApplication.screenAt(QCursor.pos())
    if screen:
        return screen
    return QApplication.primaryScreen()


class RandomEdgeBehavior(QObject):
    """Comportamento: comparsa random ai bordi dello schermo attivo."""

    position_signal = pyqtSignal(int, int)  # x, y
    show_signal = pyqtSignal()
    hide_signal = pyqtSignal()

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.running = True

        # Configurazione temporale (in secondi)
        self.min_interval = 10  # Minimo tempo tra comparse
        self.max_interval = 30  # Massimo tempo tra comparse
        self.min_show_time = 1  # Minimo tempo di visibilità
        self.max_show_time = 3  # Massimo tempo di visibilità

        # Timer per il loop
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)

        # Timer per il prossimo spawn
        self.spawn_timer = QTimer()
        self.spawn_timer.setSingleShot(True)
        self.spawn_timer.timeout.connect(self.spawn)

    def set_window_size(self, width, height):
        """Aggiorna dimensioni finestra."""
        self.window_width = width
        self.window_height = height

    def start_behavior(self):
        """Avvia il comportamento."""
        self.running = True
        # Primo spawn dopo un intervallo casuale
        delay = random.randint(self.min_interval, self.max_interval) * 1000
        self.spawn_timer.start(delay)

    def stop_behavior(self):
        """Ferma il comportamento."""
        self.running = False
        self.hide_timer.stop()
        self.spawn_timer.stop()

    def spawn(self):
        """Fa apparire il personaggio in una posizione casuale ai bordi dello schermo attivo."""
        if not self.running:
            return

        screen = get_current_screen()
        if not screen:
            return

        screen_geometry = screen.geometry()
        left = screen_geometry.x()
        top = screen_geometry.y()
        max_x = left + screen_geometry.width() - self.window_width
        max_y = top + screen_geometry.height() - self.window_height

        if max_x < left:
            max_x = left
        if max_y < top:
            max_y = top

        # Scegli un lato casuale: 0=top, 1=bottom, 2=left, 3=right
        side = random.randint(0, 3)

        # Calcola posizione casuale sul lato scelto
        if side == 0:  # Top
            x = random.randint(left, max_x)
            y = top
        elif side == 1:  # Bottom
            x = random.randint(left, max_x)
            y = max_y
        elif side == 2:  # Left
            x = left
            y = random.randint(top, max_y)
        else:  # Right
            x = max_x
            y = random.randint(top, max_y)

        # Emetti segnali per mostrare e posizionare
        self.position_signal.emit(x, y)
        self.show_signal.emit()

        # Imposta timer per nascondere dopo tempo casuale
        show_time = random.randint(self.min_show_time, self.max_show_time) * 1000
        self.hide_timer.start(show_time)

    def hide(self):
        """Nasconde il personaggio."""
        if not self.running:
            return

        self.hide_signal.emit()

        # Programma prossimo spawn
        delay = random.randint(self.min_interval, self.max_interval) * 1000
        self.spawn_timer.start(delay)

    def set_timing(self, min_interval, max_interval, min_show, max_show):
        """Configura i tempi di comparsa/scomparsa."""
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.min_show_time = min_show
        self.max_show_time = max_show


class FreeWalkBehavior(QObject):
    """Comportamento: passeggiata libera lungo il bordo inferiore dello schermo (sopra la taskbar)."""

    position_signal = pyqtSignal(int, int)  # x, y

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.running = False
        self.is_dragging = False

        # Configurazione movimento
        self.speed = 2  # Pixel per frame
        self.direction = 1  # 1 = destra, -1 = sinistra
        self.current_x = 0
        self.current_y = 0

        # Timer per il loop di movimento
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_step)

        # Timer per l'animazione di caduta
        self.fall_timer = QTimer()
        self.fall_timer.timeout.connect(self.fall_step)
        self.fall_velocity = 0.0  # Velocità verticale corrente
        self.fall_acceleration = 0.5  # Accelerazione gravità (pixel/frame²)
        self.is_falling = False

    def set_window_size(self, width, height):
        """Aggiorna dimensioni finestra."""
        self.window_width = width
        self.window_height = height

    def start_behavior(self):
        """Avvia il comportamento."""
        self.running = True

        # Posiziona inizialmente al centro del bordo inferiore dello schermo attivo
        screen = get_current_screen()
        if screen:
            screen_geometry = screen.geometry()
            self.current_x = screen_geometry.x() + (screen_geometry.width() - self.window_width) // 2
            self.current_y = screen_geometry.y() + screen_geometry.height() - self.window_height
            self.position_signal.emit(int(self.current_x), int(self.current_y))

        # Avvia il timer di movimento (60 FPS)
        self.move_timer.start(16)  # ~60 FPS

    def stop_behavior(self):
        """Ferma il comportamento."""
        self.running = False
        self.move_timer.stop()
        self.fall_timer.stop()
        self.is_falling = False

    def move_step(self):
        """Esegue un passo del movimento."""
        if not self.running or self.is_dragging or self.is_falling:
            return

        screen = get_screen_for_point(self.current_x + self.window_width // 2, self.current_y + self.window_height // 2)
        if not screen:
            return

        screen_geometry = screen.geometry()
        min_x = screen_geometry.x()
        max_x = screen_geometry.x() + screen_geometry.width() - self.window_width
        target_y = screen_geometry.y() + screen_geometry.height() - self.window_height

        # Mantieni Y perfettamente allineata alla taskbar dello schermo attuale
        if self.current_y != target_y:
            self.current_y = target_y

        # Muovi orizzontalmente
        self.current_x += self.speed * self.direction

        # Cambia direzione ai bordi
        if self.current_x <= min_x:
            self.current_x = min_x
            self.direction = 1
        elif self.current_x >= max_x:
            self.current_x = max_x
            self.direction = -1

        self.position_signal.emit(int(self.current_x), int(self.current_y))

    def set_dragging(self, is_dragging):
        """Imposta se il personaggio è in fase di trascinamento."""
        self.is_dragging = is_dragging
        if is_dragging and self.is_falling:
            self.is_falling = False
            self.fall_timer.stop()
            self.fall_velocity = 0.0

    def update_position(self, x, y):
        """Aggiorna la posizione quando trascinato."""
        self.current_x, self.current_y = self._clamp_to_screen(x, y)

    def _clamp_to_screen(self, x, y):
        """Limita le coordinate all'interno dello schermo corretto (supporta multi-monitor)."""
        screen = get_screen_for_point(x + self.window_width // 2, y + self.window_height // 2)
        if screen:
            screen_geometry = screen.geometry()
            min_x = screen_geometry.x()
            max_x = screen_geometry.x() + screen_geometry.width() - self.window_width
            min_y = screen_geometry.y()
            max_y = screen_geometry.y() + screen_geometry.height() - self.window_height

            x = max(min_x, min(max_x, x))
            y = max(min_y, min(max_y, y))

        return x, y

    def fall_to_bottom(self):
        """Fa cadere il personaggio al bordo inferiore con animazione gravitazionale."""
        screen = get_screen_for_point(self.current_x + self.window_width // 2, self.current_y + self.window_height // 2)
        if not screen:
            return

        screen_geometry = screen.geometry()
        target_y = screen_geometry.y() + screen_geometry.height() - self.window_height

        # Se è oltre il bordo inferiore (es. dentro la taskbar), riposizionalo immediatamente al bordo
        if self.current_y >= target_y:
            self.current_y = target_y
            self.position_signal.emit(int(self.current_x), int(self.current_y))
        else:
            self.is_falling = True
            self.fall_velocity = 0.0  # Reset velocità
            self.fall_timer.start(16)  # 60 FPS

    def fall_step(self):
        """Esegue un passo della caduta con accelerazione."""
        if not self.is_falling:
            return

        screen = get_screen_for_point(self.current_x + self.window_width // 2, self.current_y + self.window_height // 2)
        if not screen:
            self.is_falling = False
            self.fall_timer.stop()
            return

        screen_geometry = screen.geometry()
        min_y = screen_geometry.y()
        target_y = screen_geometry.y() + screen_geometry.height() - self.window_height

        # Se la posizione corrente è fuori dallo schermo in alto, riposiziona
        if self.current_y < min_y:
            self.current_y = min_y

        # Aggiorna velocità con accelerazione
        self.fall_velocity += self.fall_acceleration

        # Muovi verso il basso
        self.current_y += self.fall_velocity

        # Controlla se ha raggiunto o superato il bordo inferiore
        if self.current_y >= target_y:
            self.current_y = target_y
            self.is_falling = False
            self.fall_timer.stop()
            self.fall_velocity = 0.0

        self.position_signal.emit(int(self.current_x), int(self.current_y))

    def set_speed(self, speed):
        """Imposta la velocità di movimento."""
        self.speed = speed


class GravityBehavior(QObject):
    """Comportamento: gravità con rimbalzo al bordo inferiore (taskbar) e collisioni con i bordi laterali."""

    position_signal = pyqtSignal(int, int)  # x, y

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.running = False
        self.is_dragging = False

        # Configurazione fisica
        self.gravity = 0.5  # Accelerazione gravità (pixel/frame²)
        self.bounce_factor = 0.6  # Fattore di rimbalzo (0-1)
        self.friction = 0.98  # Attrito orizzontale
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.current_x = 0.0
        self.current_y = 0.0

        # Timer per il loop di fisica
        self.physics_timer = QTimer()
        self.physics_timer.timeout.connect(self.physics_step)

    def set_window_size(self, width, height):
        """Aggiorna dimensioni finestra."""
        self.window_width = width
        self.window_height = height

    def start_behavior(self):
        """Avvia il comportamento."""
        self.running = True

        # Posiziona inizialmente al centro dello schermo attivo
        screen = get_current_screen()
        if screen:
            screen_geometry = screen.geometry()
            self.current_x = screen_geometry.x() + (screen_geometry.width() - self.window_width) // 2
            self.current_y = screen_geometry.y() + 100  # Inizia dall'alto dello schermo corrente
            self.velocity_x = 0.0
            self.velocity_y = 0.0
            self.position_signal.emit(int(self.current_x), int(self.current_y))

        # Avvia il timer di fisica (60 FPS)
        self.physics_timer.start(16)  # ~60 FPS

    def stop_behavior(self):
        """Ferma il comportamento."""
        self.running = False
        self.physics_timer.stop()

    def physics_step(self):
        """Esegue un passo della simulazione fisica."""
        if not self.running or self.is_dragging:
            return

        screen = get_screen_for_point(self.current_x + self.window_width // 2, self.current_y + self.window_height // 2)
        if not screen:
            return

        screen_geometry = screen.geometry()
        min_x = screen_geometry.x()
        max_x = screen_geometry.x() + screen_geometry.width() - self.window_width
        bottom_y = screen_geometry.y() + screen_geometry.height() - self.window_height

        # Applica gravità
        self.velocity_y += self.gravity

        # Aggiorna posizione
        self.current_x += self.velocity_x
        self.current_y += self.velocity_y

        # Collisione con il bordo inferiore (sopra la taskbar)
        if self.current_y >= bottom_y:
            self.current_y = bottom_y
            # Rimbalzo
            self.velocity_y = -self.velocity_y * self.bounce_factor

            # Se la velocità è molto bassa, ferma il rimbalzo
            if abs(self.velocity_y) < 1.0:
                self.velocity_y = 0.0

        # Collisione con i bordi laterali
        if self.current_x <= min_x:
            self.current_x = min_x
            self.velocity_x = -self.velocity_x * self.bounce_factor
        elif self.current_x >= max_x:
            self.current_x = max_x
            self.velocity_x = -self.velocity_x * self.bounce_factor

        # Applica attrito orizzontale
        self.velocity_x *= self.friction
        if abs(self.velocity_x) < 0.05:
            self.velocity_x = 0.0

        self.position_signal.emit(int(self.current_x), int(self.current_y))

    def set_dragging(self, is_dragging):
        """Imposta se il personaggio è in fase di trascinamento."""
        self.is_dragging = is_dragging
        if is_dragging:
            # Resetta velocità quando inizia il drag
            self.velocity_x = 0.0
            self.velocity_y = 0.0

    def update_position(self, x, y):
        """Aggiorna la posizione quando trascinato."""
        self.current_x, self.current_y = self._clamp_to_screen(x, y)

    def _clamp_to_screen(self, x, y):
        """Limita le coordinate all'interno dello schermo corretto (supporta multi-monitor)."""
        screen = get_screen_for_point(x + self.window_width // 2, y + self.window_height // 2)
        if screen:
            screen_geometry = screen.geometry()
            min_x = screen_geometry.x()
            max_x = screen_geometry.x() + screen_geometry.width() - self.window_width
            min_y = screen_geometry.y()
            max_y = screen_geometry.y() + screen_geometry.height() - self.window_height

            x = max(min_x, min(max_x, x))
            y = max(min_y, min(max_y, y))

        return x, y

    def set_gravity(self, gravity):
        """Imposta l'accelerazione di gravità."""
        self.gravity = gravity

    def set_bounce_factor(self, bounce):
        """Imposta il fattore di rimbalzo."""
        self.bounce_factor = max(0.0, min(1.0, bounce))
