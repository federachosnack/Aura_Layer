import unittest
import os
import sys
import tempfile

# Isola APPDATA prima di importare qualsiasi modulo di Aura Layer
if "APPDATA" not in os.environ or "auralayer_test" not in os.environ["APPDATA"]:
    os.environ["APPDATA"] = tempfile.mkdtemp(prefix="auralayer_test_")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.translations import Translations


class TestTranslations(unittest.TestCase):

    def setUp(self):
        self.tr = Translations()

    def test_key_parity(self):
        """Verifica la perfetta simmetria 100% tra le chiavi IT ed EN."""
        it_keys = set(self.tr.TRANSLATIONS["it"].keys())
        en_keys = set(self.tr.TRANSLATIONS["en"].keys())

        missing_in_en = it_keys - en_keys
        missing_in_it = en_keys - it_keys

        self.assertEqual(len(missing_in_en), 0, f"Chiavi presenti in IT ma mancanti in EN: {missing_in_en}")
        self.assertEqual(len(missing_in_it), 0, f"Chiavi presenti in EN ma mancanti in IT: {missing_in_it}")
        self.assertEqual(len(it_keys), len(en_keys))
        self.assertGreaterEqual(len(it_keys), 245)

    def test_security_and_crash_keys_exist(self):
        """Verifica che tutte le chiavi critiche di errore e sicurezza siano definite."""
        critical_keys = [
            "import_too_many_files",
            "import_uncompressed_size",
            "import_unsafe_path",
            "import_invalid_manifest",
            "import_anim_missing",
            "crash_critical_title",
            "crash_critical_msg"
        ]
        for key in critical_keys:
            self.assertIn(key, self.tr.TRANSLATIONS["it"])
            self.assertIn(key, self.tr.TRANSLATIONS["en"])

    def test_language_switch(self):
        """Verifica lo switch tra lingue."""
        self.tr.set_language("it")
        self.assertEqual(self.tr.current_language, "it")
        it_val = self.tr.get("app_title")

        self.tr.set_language("en")
        self.assertEqual(self.tr.current_language, "en")
        en_val = self.tr.get("app_title")

        self.assertIsNotNone(it_val)
        self.assertIsNotNone(en_val)


if __name__ == "__main__":
    unittest.main()
