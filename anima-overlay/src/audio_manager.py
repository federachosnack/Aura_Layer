import os
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QObject, pyqtSignal


class AudioManager(QObject):
    """Gestisce la riproduzione audio per i personaggi."""

    audio_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)
        self.player.playbackStateChanged.connect(self._on_state_changed)

    def play_sound(self, file_path: str, volume: float = 0.5) -> bool:
        """Riproduce un file audio con volume clampato tra 0.0 e 1.0."""
        if not os.path.exists(file_path):
            return False

        clamped_volume = max(0.0, min(1.0, float(volume)))
        self.audio_output.setVolume(clamped_volume)
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.player.play()
        return True

    def stop(self):
        """Ferma la riproduzione."""
        self.player.stop()

    def set_volume(self, volume: float):
        """Imposta il volume (0.0 - 1.0)."""
        self.audio_output.setVolume(max(0.0, min(1.0, float(volume))))

    def get_volume(self) -> float:
        """Restituisce il volume attuale."""
        return self.audio_output.volume()

    def is_playing(self) -> bool:
        """Verifica se sta riproducendo."""
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    def _on_state_changed(self, state):
        """Callback quando cambia lo stato."""
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.audio_finished.emit()
