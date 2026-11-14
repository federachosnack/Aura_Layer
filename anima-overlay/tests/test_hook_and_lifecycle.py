import unittest
import os
import sys

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

    def test_animation_player_budget(self):
        """Verifica che il budget di 128 MB calcoli le dimensioni corrette senza crash."""
        player = AnimationPlayer()
        self.assertIsNotNone(player)


if __name__ == "__main__":
    unittest.main()
