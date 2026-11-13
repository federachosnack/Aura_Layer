import random
import time
from PyQt6.QtCore import QTimer, QObject, pyqtSignal, QPoint, QVariantAnimation, QEasingCurve
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
    """
    Comportamento: Sbircia dai bordi (Peek-a-boo).
    Il compagno vive nascosto appena fuori dallo schermo e fa capolino
    scivolando fluidamente all'interno per fare compagnia, per poi rientrare dopo un tempo piacevole.
    """

    position_signal = pyqtSignal(int, int)  # x, y
    show_signal = pyqtSignal()
    hide_signal = pyqtSignal()

    def __init__(self, window_width: int, window_height: int):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.running = False
        self.is_dragging = False
        self.is_sliding_in = False
        self.is_sliding_out = False

        # Tempi configurabili (in secondi)
        self.min_interval = 20   # Minimo tempo nascosto tra una sbirciata e l'altra
        self.max_interval = 45   # Massimo tempo nascosto tra una sbirciata e l'altra
        self.min_show_time = 14  # Minimo tempo di permanenza visibile
        self.max_show_time = 22  # Massimo tempo di permanenza visibile

        # Coordinate per le posizioni
        self.current_visible_pos = QPoint(0, 0)
        self.current_hidden_pos = QPoint(0, 0)

        # Timer per nascondere
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)

        # Timer per il prossimo spawn
        self.spawn_timer = QTimer(self)
        self.spawn_timer.setSingleShot(True)
        self.spawn_timer.timeout.connect(self.spawn)

        # Animazione di scorrimento (slide-in / slide-out)
        self.slide_anim = QVariantAnimation(self)
        self.slide_anim.valueChanged.connect(self._on_slide_step)
        self.slide_anim.finished.connect(self._on_slide_finished)

    def set_window_size(self, width: int, height: int):
        """Aggiorna dimensioni finestra."""
        self.window_width = width
        self.window_height = height

    def start_behavior(self):
        """Avvia il comportamento con prima sbirciata rapida."""
        self.running = True
        self.is_dragging = False
        # Prima sbirciata rapida dopo 800ms per mostrare subito il compagno all'avvio
        self.spawn_timer.start(800)

    def stop_behavior(self):
        """Ferma il comportamento e le animazioni."""
        self.running = False
        self.slide_anim.stop()
        self.hide_timer.stop()
        self.spawn_timer.stop()

    def resume_behavior(self):
        """Riprende il comportamento dopo una pausa o evento hide/show."""
        if not self.running:
            self.running = True
            if not self.is_dragging:
                if not self.spawn_timer.isActive() and not self.hide_timer.isActive() and self.slide_anim.state() != QVariantAnimation.State.Running:
                    self.spawn_timer.start(800)

    def set_dragging(self, is_dragging: bool, x: int = 0, y: int = 0):
        """Gestisce il drag dell'utente, sospendendo o riprendendo le animazioni."""
        self.is_dragging = is_dragging
        if is_dragging:
            self.slide_anim.stop()
            self.hide_timer.stop()
            self.spawn_timer.stop()
            self.is_sliding_in = False
            self.is_sliding_out = False
        else:
            # L'utente ha rilasciato il personaggio sullo schermo
            self.current_visible_pos = QPoint(x, y)
            self.current_hidden_pos = self._calc_nearest_hidden_pos(x, y)
            # Rimane visibile dove l'utente l'ha lasciato per 15s prima di rientrare
            if self.running:
                self.hide_timer.start(15000)

    def update_position(self, x: int, y: int):
        """Aggiorna posizione durante il trascinamento."""
        self.current_visible_pos = QPoint(x, y)

    def spawn(self):
        """Fa sbirciare il personaggio scivolando da un bordo casuale dello schermo."""
        if not self.running or self.is_dragging:
            return

        screen = get_current_screen()
        if not screen:
            screen = QApplication.primaryScreen()
        if not screen:
            return

        screen_geometry = screen.geometry()
        left = screen_geometry.x()
        top = screen_geometry.y()
        right = left + screen_geometry.width()
        bottom = top + screen_geometry.height()

        max_x = max(left, right - self.window_width)
        max_y = max(top, bottom - self.window_height)

        # Margine di sicurezza per i punti casuali lungo i bordi
        pad_x = min(60, (max_x - left) // 4) if max_x > left else 0
        pad_y = min(60, (max_y - top) // 4) if max_y > top else 0

        # Scegli un lato casuale: 0=Bottom, 1=Right, 2=Left, 3=Top
        side = random.randint(0, 3)

        if side == 0:  # Bottom: sbuca dal bordo inferiore (sopra la barra)
            rand_x = random.randint(left + pad_x, max_x - pad_x) if max_x - pad_x > left + pad_x else left
            start_pos = QPoint(rand_x, bottom)
            end_pos = QPoint(rand_x, max_y)
        elif side == 1:  # Right: sbuca dal bordo destro
            rand_y = random.randint(top + pad_y, max_y - pad_y) if max_y - pad_y > top + pad_y else top
            start_pos = QPoint(right, rand_y)
            end_pos = QPoint(max_x, rand_y)
        elif side == 2:  # Left: sbuca dal bordo sinistro
            rand_y = random.randint(top + pad_y, max_y - pad_y) if max_y - pad_y > top + pad_y else top
            start_pos = QPoint(left - self.window_width, rand_y)
            end_pos = QPoint(left, rand_y)
        else:  # Top: sbuca dal bordo superiore
            rand_x = random.randint(left + pad_x, max_x - pad_x) if max_x - pad_x > left + pad_x else left
            start_pos = QPoint(rand_x, top - self.window_height)
            end_pos = QPoint(rand_x, top)

        self.current_hidden_pos = start_pos
        self.current_visible_pos = end_pos

        # Posiziona fuori schermo e mostra finestra
        self.position_signal.emit(start_pos.x(), start_pos.y())
        self.show_signal.emit()

        # Avvia animazione slide-in morbida (650 ms con OutCubic)
        self.is_sliding_in = True
        self.is_sliding_out = False
        self.slide_anim.stop()
        self.slide_anim.setDuration(650)
        self.slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.slide_anim.setStartValue(start_pos)
        self.slide_anim.setEndValue(end_pos)
        self.slide_anim.start()

    def hide(self):
        """Fa rientrare dolcemente il personaggio nel bordo dello schermo (slide-out)."""
        if not self.running or self.is_dragging:
            return

        self.is_sliding_in = False
        self.is_sliding_out = True
        self.slide_anim.stop()
        self.slide_anim.setDuration(500)
        self.slide_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self.slide_anim.setStartValue(self.current_visible_pos)
        self.slide_anim.setEndValue(self.current_hidden_pos)
        self.slide_anim.start()

    def _on_slide_step(self, val):
        """Callback interpolazione animazione."""
        if isinstance(val, QPoint):
            self.position_signal.emit(val.x(), val.y())

    def _on_slide_finished(self):
        """Callback al completamento dello slide."""
        if self.is_sliding_in:
            self.is_sliding_in = False
            # Assicura posizione esatta finale
            self.position_signal.emit(self.current_visible_pos.x(), self.current_visible_pos.y())
            # Avvia il tempo di permanenza visibile (14 - 22 secondi)
            show_time = random.randint(self.min_show_time, self.max_show_time) * 1000
            self.hide_timer.start(show_time)
        elif self.is_sliding_out:
            self.is_sliding_out = False
            # Nasconde completamente la finestra finché non torna
            self.hide_signal.emit()
            # Programma la prossima sbirciata (20 - 45 secondi)
            delay = random.randint(self.min_interval, self.max_interval) * 1000
            self.spawn_timer.start(delay)

    def _calc_nearest_hidden_pos(self, x: int, y: int) -> QPoint:
        """Calcola la posizione nascosta sul bordo più vicino dopo un drag dell'utente."""
        screen = get_screen_for_point(x + self.window_width // 2, y + self.window_height // 2)
        if not screen:
            screen = QApplication.primaryScreen()
        if not screen:
            return QPoint(x, y + self.window_height)

        geom = screen.geometry()
        d_left = x - geom.x()
        d_right = (geom.x() + geom.width()) - (x + self.window_width)
        d_top = y - geom.y()
        d_bottom = (geom.y() + geom.height()) - (y + self.window_height)

        min_dist = min(d_left, d_right, d_top, d_bottom)
        if min_dist == d_bottom:
            return QPoint(x, geom.y() + geom.height())
        elif min_dist == d_right:
            return QPoint(geom.x() + geom.width(), y)
        elif min_dist == d_left:
            return QPoint(geom.x() - self.window_width, y)
        else:
            return QPoint(x, geom.y() - self.window_height)

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

    def resume_behavior(self):
        """Riprende il comportamento senza reimpostare la posizione."""
        if not self.running:
            self.running = True
            if not self.move_timer.isActive() and not self.is_falling:
                self.move_timer.start(16)

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
            if self.running and not self.is_dragging and not self.move_timer.isActive():
                self.move_timer.start(16)
        else:
            self.is_falling = True
            self.fall_velocity = 0.0  # Reset velocità
            self.move_timer.stop()  # Sospendi move_timer durante la caduta (evita 2 timer a 60 FPS contemporanei)
            self.fall_timer.start(16)  # 60 FPS

    def fall_step(self):
        """Esegue un passo della caduta con accelerazione."""
        if not self.is_falling:
            return

        screen = get_screen_for_point(self.current_x + self.window_width // 2, self.current_y + self.window_height // 2)
        if not screen:
            self.is_falling = False
            self.fall_timer.stop()
            if self.running and not self.is_dragging and not self.move_timer.isActive():
                self.move_timer.start(16)
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
            if self.running and not self.is_dragging and not self.move_timer.isActive():
                self.move_timer.start(16)  # Riprende la passeggiata orizzontale a terra

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

        # Configurazione fisica calibrata per lancio naturale e morbido
        self.gravity = 0.55  # Accelerazione gravità morbida
        self.bounce_factor = 0.45  # Rimbalzo elastico dolce e naturale
        self.friction = 0.94  # Attrito orizzontale graduale
        self.max_toss_speed = 16.0  # Velocità massima di lancio per evitare effetto proiettile
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.current_x = 0.0
        self.current_y = 0.0
        self._drag_history = []  # Buffer recente di (x, y, timestamp) per calcolare il vero vettore di lancio
        self._idle_frames = 0  # Contatore frame di quiete per standby automatico (0% CPU)

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
        self._idle_frames = 0

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
        self._idle_frames = 0
        self.physics_timer.stop()

    def resume_behavior(self):
        """Riprende la simulazione fisica se il personaggio non è già a riposo sul suolo."""
        if not self.running:
            self.running = True
            screen = get_screen_for_point(int(self.current_x) + self.window_width // 2, int(self.current_y) + self.window_height // 2)
            if screen:
                geom = screen.geometry()
                floor_y = geom.bottom() - self.window_height
                if self.current_y < floor_y - 2 or abs(self.velocity_x) > 0.1 or abs(self.velocity_y) > 0.1:
                    self._idle_frames = 0
                    if not self.physics_timer.isActive():
                        self.physics_timer.start(16)

    def physics_step(self):
        """Esegue un passo della simulazione fisica con standby intelligente a riposo (0% CPU)."""
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
            # Rimbalzo con smorzamento dolce
            self.velocity_y = -self.velocity_y * self.bounce_factor

            # Se la velocità di rimbalzo è minima, fermala a zero
            if abs(self.velocity_y) < 0.8:
                self.velocity_y = 0.0

        # Collisione con i bordi laterali (rimbalzo naturale dalle pareti)
        if self.current_x <= min_x:
            self.current_x = min_x
            self.velocity_x = -self.velocity_x * self.bounce_factor
        elif self.current_x >= max_x:
            self.current_x = max_x
            self.velocity_x = -self.velocity_x * self.bounce_factor

        # Applica attrito orizzontale
        self.velocity_x *= self.friction
        if abs(self.velocity_x) < 0.08:
            self.velocity_x = 0.0

        self.position_signal.emit(int(self.current_x), int(self.current_y))

        # Ottimizzazione Risorse (Sleep-on-Idle):
        # Quando il personaggio è fermo a terra, dopo 10 frame consecutivi spegniamo il timer
        # per ridurre a 0.0% l'utilizzo della CPU a riposo.
        if abs(self.current_y - bottom_y) < 1.0 and abs(self.velocity_y) < 0.01 and abs(self.velocity_x) < 0.01:
            self._idle_frames += 1
            if self._idle_frames >= 10:
                self.physics_timer.stop()
        else:
            self._idle_frames = 0

    def set_dragging(self, is_dragging):
        """Gestisce l'inizio o il rilascio del trascinamento, calcolando l'inerzia del lancio."""
        self.is_dragging = is_dragging
        now = time.time()
        if is_dragging:
            self.velocity_x = 0.0
            self.velocity_y = 0.0
            self._drag_history = []
            self._idle_frames = 0
        else:
            # Calcola la velocità del lancio analizzando i punti recenti negli ultimi 80ms
            recent_points = [p for p in self._drag_history if (now - p[2]) <= 0.08]
            if len(recent_points) >= 2:
                points_to_use = recent_points[-3:]
                p_first = points_to_use[0]
                p_last = points_to_use[-1]
                dt = p_last[2] - p_first[2]
                time_since_last = now - p_last[2]

                # Se l'utente si è fermato prima di rilasciare (mano ferma > 50ms), posa piano senza lancio
                if time_since_last > 0.05 or dt <= 0.010:
                    self.velocity_x = 0.0
                    self.velocity_y = 0.0
                else:
                    raw_vx = (p_last[0] - p_first[0]) / (dt * 60)
                    raw_vy = (p_last[1] - p_first[1]) / (dt * 60)

                    # Se il movimento è troppo debole, non innescare il lancio
                    if abs(raw_vx) < 1.2 and abs(raw_vy) < 1.2:
                        self.velocity_x = 0.0
                        self.velocity_y = 0.0
                    else:
                        # Applica moltiplicatore naturale e cap massimo morbido di sicurezza
                        self.velocity_x = max(-self.max_toss_speed, min(self.max_toss_speed, raw_vx * 0.70))
                        self.velocity_y = max(-self.max_toss_speed, min(self.max_toss_speed, raw_vy * 0.70))
            else:
                self.velocity_x = 0.0
                self.velocity_y = 0.0

            # Se posato a terra delicatamente con velocità quasi nulla, adagia senza rimbalzi
            screen = get_screen_for_point(self.current_x + self.window_width // 2, self.current_y + self.window_height // 2)
            if screen:
                bottom_y = screen.geometry().y() + screen.geometry().height() - self.window_height
                if abs(self.current_y - bottom_y) < 8 and abs(self.velocity_y) < 1.5 and abs(self.velocity_x) < 1.0:
                    self.current_y = bottom_y
                    self.velocity_y = 0.0
                    self.velocity_x = 0.0

            # Risveglia il timer di fisica se fermo in sleep
            self._idle_frames = 0
            if self.running and not self.physics_timer.isActive():
                self.physics_timer.start(16)

    def update_position(self, x, y):
        """Aggiorna la posizione durante il trascinamento e memorizza la traiettoria recente per il lancio."""
        now = time.time()
        new_x, new_y = self._clamp_to_screen(x, y)
        self.current_x = new_x
        self.current_y = new_y
        self._drag_history.append((float(new_x), float(new_y), now))
        if len(self._drag_history) > 6:
            self._drag_history.pop(0)

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
