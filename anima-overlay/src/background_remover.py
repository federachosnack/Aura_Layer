import os
from typing import Optional
from PIL import Image

# Disabilita JIT di numba per migliorare stabilità in eseguibili compilati
os.environ.setdefault('NUMBA_DISABLE_JIT', '1')

from rembg import remove


class BackgroundRemover:
    """Gestisce la rimozione dello sfondo dalle immagini usando rembg."""

    @staticmethod
    def remove_background(input_path: str, output_path: str) -> bool:
        """Rimuove lo sfondo da un'immagine e salva il risultato."""
        try:
            # Carica l'immagine
            input_image = Image.open(input_path)

            # Rimuovi lo sfondo
            output_image = remove(input_image)

            # Salva il risultato
            output_image.save(output_path)
            return True
        except Exception as e:
            print(f"Error removing background: {e}")
            return False

    @staticmethod
    def is_supported_format(file_path: str) -> bool:
        """Verifica se il formato è supportato."""
        supported_extensions = ['.png', '.jpg', '.jpeg', '.webp', '.gif']
        return os.path.splitext(file_path)[1].lower() in supported_extensions
