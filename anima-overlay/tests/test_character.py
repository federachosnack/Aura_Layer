import unittest
import os
import tempfile
import json
import sys

# Assicura importazione moduli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.character import Character


class TestCharacterModel(unittest.TestCase):

    def test_load_config_sanitization_and_clamping(self):
        """Verifica che Character.load_config converta e limiti in modo sicuro valori corrotti o errati."""
        with tempfile.TemporaryDirectory() as td:
            bad_cfg = {
                "name": "   ",                      # Solo spazi -> deve fallback sul nome cartella
                "animation_file": "anim.gif",
                "behavior": "super_flying_alien",    # Non valido -> deve fallback su static
                "width": "5000",                     # Oltre max 2000 -> deve clampare a 2000
                "height": "-10",                     # Minore di min 10 -> deve clampare a 10
                "scale": "500",                      # Oltre max 200 -> deve clampare a 200
                "fps": "120",                        # Oltre max 60 -> deve clampare a 60
                "volume": "3.5",                     # Oltre max 1.0 -> deve clampare a 1.0
                "speed": "25.0",                     # Oltre max 10.0 -> deve clampare a 10.0
                "locked": "true",                    # Stringa -> True bool
                "draggable": "false",                # Stringa false -> False bool (non bool("false")!)
                "play_audio_on_startup": "False"     # Stringa -> False bool
            }
            with open(os.path.join(td, "config.json"), "w", encoding="utf-8") as f:
                json.dump(bad_cfg, f)

            c = Character(td)
            self.assertEqual(c.name, os.path.basename(td))
            self.assertEqual(c.behavior, "static")
            self.assertEqual(c.width, 2000)
            self.assertEqual(c.height, 10)
            self.assertEqual(c.scale, 200)
            self.assertEqual(c.fps, 60)
            self.assertEqual(c.volume, 1.0)
            self.assertEqual(c.speed, 10.0)
            self.assertTrue(c.locked)
            self.assertFalse(c.draggable)
            self.assertFalse(c.play_audio_on_startup)

    def test_unhashable_behavior_type(self):
        """Verifica che tipi unhashable (liste/dizionari) nel campo behavior non causino TypeError."""
        with tempfile.TemporaryDirectory() as td:
            cfg = {
                "name": "TestHero",
                "behavior": ["static", "free_walk"],
                "width": 150,
                "height": 150
            }
            with open(os.path.join(td, "config.json"), "w", encoding="utf-8") as f:
                json.dump(cfg, f)

            c = Character(td)
            self.assertEqual(c.behavior, "static")

            # Test anche in update_config
            c.update_config(behavior={"nested": "object"})
            self.assertEqual(c.behavior, "static")

    def test_update_config_and_to_dict(self):
        """Verifica aggiornamento config e serializzazione to_dict."""
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "config.json"), "w", encoding="utf-8") as f:
                json.dump({"name": "Ahri"}, f)

            c = Character(td)
            c.update_config(scale=150, fps=45, volume=0.8, behavior="free_walk")
            self.assertEqual(c.scale, 150)
            self.assertEqual(c.fps, 45)
            self.assertEqual(c.volume, 0.8)
            self.assertEqual(c.behavior, "free_walk")

            d = c.to_dict()
            self.assertEqual(d["scale"], 150)
            self.assertEqual(d["fps"], 45)
            self.assertEqual(d["behavior"], "free_walk")


if __name__ == "__main__":
    unittest.main()
