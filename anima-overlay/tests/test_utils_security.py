import unittest
import os
import io
import zipfile
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils import validate_aura_zip, sanitize_filename, atomic_write_json, get_app_logger


class TestUtilsSecurity(unittest.TestCase):

    def test_sanitize_filename(self):
        """Verifica la sanitizzazione dei nomi file per Windows."""
        # 1. Caratteri vietati e directory traversal
        self.assertEqual(sanitize_filename("../../evil.exe"), "evil.exe")
        self.assertEqual(sanitize_filename("folder/sub\\name?.gif"), "name.gif")
        self.assertEqual(sanitize_filename("name*with:invalid|chars.png"), "namewithinvalidchars.png")

        # 2. Nomi di dispositivo riservati di Windows
        self.assertEqual(sanitize_filename("CON"), "character")
        self.assertEqual(sanitize_filename("prn.txt"), "character")
        self.assertEqual(sanitize_filename("aux"), "character")
        self.assertEqual(sanitize_filename("nul"), "character")
        self.assertEqual(sanitize_filename("com1.png"), "character")
        self.assertEqual(sanitize_filename("lpt2"), "character")

        # 3. Stringa vuota o solo spazi
        self.assertEqual(sanitize_filename(""), "character")
        self.assertEqual(sanitize_filename("   "), "character")
        self.assertEqual(sanitize_filename("ValidName"), "ValidName")

    def test_validate_aura_zip_security(self):
        """Verifica che la validazione pacchetto .aura blocchi zip-bomb e path traversal."""
        # 1. Archivio valido
        valid_buf = io.BytesIO()
        with zipfile.ZipFile(valid_buf, "w") as z:
            z.writestr("manifest.json", "{}")
            z.writestr("animation.gif", b"GIF89a")
            z.writestr("..preview.png", b"OK")  # File valido che inizia con due punti ma non è traversal
        valid_buf.seek(0)
        with zipfile.ZipFile(valid_buf, "r") as z:
            ok, code = validate_aura_zip(z)
            self.assertTrue(ok)
            self.assertEqual(code, "")

        # 2. Path traversal classico (../)
        bad_buf = io.BytesIO()
        with zipfile.ZipFile(bad_buf, "w") as z:
            z.writestr("../hack.bat", b"evil")
        bad_buf.seek(0)
        with zipfile.ZipFile(bad_buf, "r") as z:
            ok, code = validate_aura_zip(z)
            self.assertFalse(ok)
            self.assertEqual(code, "ERR_UNSAFE_PATH")

        # 3. Percorso assoluto Linux o Windows (C: o /)
        abs_buf = io.BytesIO()
        with zipfile.ZipFile(abs_buf, "w") as z:
            z.writestr("/root/hack.sh", b"evil")
        abs_buf.seek(0)
        with zipfile.ZipFile(abs_buf, "r") as z:
            ok, code = validate_aura_zip(z)
            self.assertFalse(ok)
            self.assertEqual(code, "ERR_UNSAFE_PATH")

        # 4. Zip bomb per numero di file
        many_buf = io.BytesIO()
        with zipfile.ZipFile(many_buf, "w") as z:
            for i in range(15):
                z.writestr(f"f_{i}.txt", b"x")
        many_buf.seek(0)
        with zipfile.ZipFile(many_buf, "r") as z:
            ok, code = validate_aura_zip(z, max_files=10)
            self.assertFalse(ok)
            self.assertEqual(code, "ERR_TOO_MANY_FILES")

        # 5. Zip bomb per dimensione decompressa
        large_buf = io.BytesIO()
        with zipfile.ZipFile(large_buf, "w") as z:
            z.writestr("huge.dat", b"0" * 5000)
        large_buf.seek(0)
        with zipfile.ZipFile(large_buf, "r") as z:
            ok, code = validate_aura_zip(z, max_uncompressed_bytes=2000)
            self.assertFalse(ok)
            self.assertEqual(code, "ERR_UNCOMPRESSED_SIZE")

    def test_atomic_write_json(self):
        """Verifica la scrittura atomica JSON con fsync e replace."""
        with tempfile.TemporaryDirectory() as td:
            target = os.path.join(td, "test_config.json")
            data = {"version": "1.2.0", "author": "federachosnack"}
            ok = atomic_write_json(target, data)
            self.assertTrue(ok)
            self.assertTrue(os.path.exists(target))
            self.assertFalse(os.path.exists(f"{target}.tmp"))

            # Rilettura
            import json
            with open(target, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            self.assertEqual(loaded, data)

    def test_app_logger(self):
        """Verifica l'inizializzazione del logger centrale dell'applicazione."""
        logger = get_app_logger()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "AuraLayer")
        logger.info("Test log message for unit testing")


if __name__ == "__main__":
    unittest.main()
