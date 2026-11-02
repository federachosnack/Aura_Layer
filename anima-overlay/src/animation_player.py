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
        """Carica un'animazione da file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File non trovato: {path}")
            
        self.animation_path = path
        self.frames = []
        self.durations = []
        self.current_frame = 0
        
        try:
            with Image.open(path) as img:
                for frame in ImageSequence.Iterator(img):
                    # Converti frame in QImage
                    frame = frame.convert("RGBA")
                    data = frame.tobytes("raw", "RGBA")
                    qimage = QImage(data, frame.width, frame.height, QImage.Format.Format_RGBA8888)
                    pixmap = QPixmap.fromImage(qimage)
                    self.frames.append(pixmap)
                    
                    # Ottieni durata del frame (default 100ms se non specificato)
                    duration = frame.info.get("duration", 100)
                    self.durations.append(duration)
                    
        except Exception as e:
            raise RuntimeError(f"Errore nel caricamento dell'animazione: {e}")
            
        if self.frames:
            self.setPixmap(self.frames[0])
            self.setScaledContents(True)
            
    def start_animation(self):
        """Avvia il playback dell'animazione."""
        if self.frames and not self.timer.isActive():
            if self.fps and self.fps > 0:
                interval = max(1, int(1000 / self.fps))
            elif self.durations:
                interval = self.durations[0]
            else:
                interval = 100
            self.timer.start(interval)
            
    def stop_animation(self):
        """Ferma il playback dell'animazione."""
        self.timer.stop()
        
    def next_frame(self):
        """Passa al frame successivo."""
        if not self.frames:
            return

        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.setPixmap(self.frames[self.current_frame])

        # Aggiorna timer con durata del prossimo frame
        if self.fps is not None:
            # Usa FPS personalizzato
            interval = int(1000 / self.fps)
        else:
            # Usa durata nativa del frame
            interval = self.durations[self.current_frame]
        self.timer.setInterval(interval)

    def set_fps(self, fps: int):
        """Imposta il FPS personalizzato (None per durata nativa) e aggiorna immediatamente il timer."""
        self.fps = fps
        if self.timer.isActive() and fps and fps > 0:
            self.timer.setInterval(max(1, int(1000 / fps)))
        
    def set_size(self, width: int, height: int):
        """Imposta le dimensioni del player."""
        self.setFixedSize(width, height)
