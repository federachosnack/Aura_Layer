from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer
from PIL import Image, ImageSequence
import os


class AnimationPlayer(QLabel):
    """Gestisce il playback di animazioni (GIF, APNG, WEBP)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation_path = None
        self.frames = []
        self.current_frame = 0
        self.durations = []
        self.fps = None  # FPS personalizzato o None per durata nativa
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.looping = True
        
    def load_animation(self, path: str):
        """Carica un'animazione da file arrestando prima eventuali playback attivi."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File non trovato: {path}")

        # Ferma il timer per evitare accessi concorrenti a frames durante il caricamento
        self.stop_animation()

        self.animation_path = path
        self.frames = []
        self.durations = []
        self.current_frame = 0

        MAX_FRAME_DIM = 1000
        MAX_FRAMES = 400
        try:
            with Image.open(path) as img:
                raw_n = getattr(img, "n_frames", 1)
                n_frames = min(MAX_FRAMES, max(1, raw_n))
                # Budget dinamico memoria: ~128 MB per animazione (4 byte/pixel RGBA) per prevenire OOM anche con molteplici personaggi attivi
                side = int((128 * 1024 * 1024 / (n_frames * 4)) ** 0.5)
                max_dim = max(64, min(MAX_FRAME_DIM, side))

                for idx, frame in enumerate(ImageSequence.Iterator(img)):
                    if idx >= MAX_FRAMES:
                        break
                    # Converti frame in RGBA disaccoppiando la copia in memoria prima di ridimensionare
                    frame = frame.convert("RGBA")

                    # Limita dimensioni massime dei frame in base al budget di memoria dinamico
                    if frame.width > max_dim or frame.height > max_dim:
                        frame.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

                    data = frame.tobytes("raw", "RGBA")
                    qimage = QImage(data, frame.width, frame.height, QImage.Format.Format_RGBA8888)
                    pixmap = QPixmap.fromImage(qimage)
                    self.frames.append(pixmap)

                    # Ottieni durata del frame con fallback sicuro (minimo 10ms per evitare 100% CPU lockup)
                    raw_duration = frame.info.get("duration", 100)
                    duration = max(10, int(raw_duration)) if raw_duration else 100
                    self.durations.append(duration)

        except Exception as e:
            raise RuntimeError(f"Errore nel caricamento dell'animazione: {e}")

        if self.frames:
            self.setPixmap(self.frames[0])
            self.setScaledContents(True)

    def start_animation(self):
        """Avvia il playback dell'animazione con intervallo sicuro."""
        if self.frames and not self.timer.isActive():
            if self.fps and self.fps > 0:
                interval = max(10, int(1000 / self.fps))
            elif self.durations:
                interval = max(10, self.durations[0])
            else:
                interval = 100
            self.timer.start(interval)

    def stop_animation(self):
        """Ferma il playback dell'animazione."""
        self.timer.stop()

    def next_frame(self):
        """Passa al frame successivo proteggendo da divisioni per zero e intervalli a 0ms."""
        if not self.frames:
            return

        # Gestione loop
        if not self.looping and self.current_frame >= len(self.frames) - 1:
            self.stop_animation()
            return

        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.setPixmap(self.frames[self.current_frame])

        # Aggiorna timer con durata del prossimo frame (minimo 10ms)
        if self.fps is not None and self.fps > 0:
            interval = max(10, int(1000 / self.fps))
        elif self.durations and self.current_frame < len(self.durations):
            interval = max(10, self.durations[self.current_frame])
        else:
            interval = 100

        self.timer.setInterval(interval)

    def set_fps(self, fps: int):
        """Imposta il FPS personalizzato (None per durata nativa) e aggiorna immediatamente il timer."""
        self.fps = fps
        if self.timer.isActive():
            if fps and fps > 0:
                self.timer.setInterval(max(10, int(1000 / fps)))
            elif self.durations and self.current_frame < len(self.durations):
                self.timer.setInterval(max(10, self.durations[self.current_frame]))
        
    def set_size(self, width: int, height: int):
        """Imposta le dimensioni del player."""
        self.setFixedSize(width, height)
