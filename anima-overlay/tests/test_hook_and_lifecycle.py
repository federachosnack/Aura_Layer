import unittest
import os
import sys
import tempfile
from PIL import Image

# Isola APPDATA prima di importare qualsiasi modulo di Aura Layer
if "APPDATA" not in os.environ or "auralayer_test" not in os.environ["APPDATA"]:
    os.environ["APPDATA"] = tempfile.mkdtemp(prefix="auralayer_test_")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtWidgets import QApplication
app = QApplication.instance() or QApplication(sys.argv)

from src.overlay_window import OverlayWindow, _ForegroundHookManager
from src.animation_player import AnimationPlayer


class TestHookAndLifecycle(unittest.TestCase):

    def test_foreground_hook_manager_singleton(self):
        """Verifica che _ForegroundHookManager sia un singleton e mantenga riferimenti deboli."""
        win1 = OverlayWindow()
        win2 = OverlayWindow()

        mgr1 = _ForegroundHookManager._instance
        self.assertIsNotNone(mgr1)
        self.assertIn(win1, mgr1.windows)
        self.assertIn(win2, mgr1.windows)

        # Chiusura di win1 -> deve uscire dal set
        win1.close()
        self.assertNotIn(win1, mgr1.windows)
        self.assertIn(win2, mgr1.windows)

        win2.close()
        self.assertNotIn(win2, mgr1.windows)

    def test_animation_player_budget_and_clamping(self):
        """Verifica che animazioni superiori a 400 frame vengano limitate a 400 salvaguardando la memoria."""
        with tempfile.TemporaryDirectory() as td:
            gif_path = os.path.join(td, "long_animation.gif")
            # Crea un'animazione con 450 frame
            frames = [Image.new("RGBA", (16, 16), (i % 255, 100, 100, 255)) for i in range(450)]
            frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=40, loop=0)

            player = AnimationPlayer()
            player.load_animation(gif_path)

            self.assertEqual(len(player.frames), 400)
            self.assertEqual(len(player.durations), 400)
            self.assertEqual(player.durations[0], 40)
            self.assertFalse(player.frames[0].isNull())


if __name__ == "__main__":
    unittest.main()
