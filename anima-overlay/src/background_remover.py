import os
from PIL import Image

# Disabilita JIT di numba per migliorare stabilità in eseguibili compilati
os.environ.setdefault('NUMBA_DISABLE_JIT', '1')


class BackgroundRemover:
    """Gestisce la rimozione dello sfondo dalle immagini usando rembg in modo lazy e sicuro."""

    @staticmethod
    def remove_background(input_path: str, output_path: str) -> bool:
        """Rimuove lo sfondo da un'immagine e salva il risultato."""
        try:
            # Import lazy per evitare di caricare onnxruntime/rembg all'avvio dell'app se non richiesto
            from rembg import remove

            # Carica l'immagine con context manager per rilasciare subito l'handle di file su Windows
            with Image.open(input_path) as input_image:
                output_image = remove(input_image)
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
