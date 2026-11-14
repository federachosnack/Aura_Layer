import json
import os
import shutil
from typing import Dict, Any, List, Optional
from src.utils import get_app_data_dir, atomic_write_json, get_app_logger

logger = get_app_logger()


class ConfigManager:
    """Manages saving and loading application settings / Gestisce il salvataggio e il caricamento delle impostazioni dell'applicazione."""

    def __init__(self, config_file: Optional[str] = None):
        # If no path provided, use default in APPDATA / Se non viene passato un percorso, usa quello di default in APPDATA
        if config_file is None:
            self.config_file = os.path.join(get_app_data_dir(), "config.json")
        else:
            self.config_file = config_file

        self.config = {}
        self.load_config()

    def load_config(self):
        """Load configuration from file / Carica la configurazione dal file con gestione recupero e backup."""
        tmp_file = f"{self.config_file}.tmp"
        loaded = False

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                loaded = True
            except Exception as e:
                logger.error(f"Error loading config from {self.config_file}: {e}")
                # Backup corrupted file for safety / Salva backup del file corrotto per sicurezza
                try:
                    shutil.copy2(self.config_file, f"{self.config_file}.corrupted")
                    logger.warning(f"Corrupted config backed up to {self.config_file}.corrupted")
                except Exception:
                    pass

        # Se non caricato e c'è un file .tmp valido, prova a recuperare da .tmp
        if not loaded and os.path.exists(tmp_file):
            try:
                with open(tmp_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                loaded = True
                logger.info(f"Config successfully recovered from {tmp_file}")
                self.save_config()
            except Exception:
                pass

        if not loaded:
            self.config = self.get_default_config()
            self.save_config()

    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration / Restituisce la configurazione di default."""
        return {
            "active_characters": [],
            "global_settings": {
                "start_minimized": False,
                "minimize_to_tray": True,
                "autostart": False,
                "language": "it"  # Default language: Italian
            }
        }

    def save_config(self):
        """Save configuration atomically to file / Salva la configurazione nel file in modo atomico."""
        atomic_write_json(self.config_file, self.config)

    def get_active_characters(self) -> List[str]:
        """Return list of active characters / Restituisce la lista dei personaggi attivi."""
        return self.config.get("active_characters", [])

    def set_active_characters(self, characters: List[str]):
        """Set list of active characters / Imposta la lista dei personaggi attivi."""
        self.config["active_characters"] = characters
        self.save_config()

    def add_active_character(self, character_name: str):
        """Add character to active list / Aggiunge un personaggio alla lista degli attivi."""
        if character_name not in self.config["active_characters"]:
            self.config["active_characters"].append(character_name)
            self.save_config()

    def remove_active_character(self, character_name: str):
        """Remove character from active list / Rimuove un personaggio dalla lista degli attivi."""
        if character_name in self.config["active_characters"]:
            self.config["active_characters"].remove(character_name)
            self.save_config()

    def get_global_setting(self, key: str, default: Any = None) -> Any:
        """Get a global setting / Ottiene un'impostazione globale."""
        return self.config.get("global_settings", {}).get(key, default)

    def set_global_setting(self, key: str, value: Any):
        """Set a global setting / Imposta un'impostazione globale."""
        if "global_settings" not in self.config:
            self.config["global_settings"] = {}
        self.config["global_settings"][key] = value
        self.save_config()

    def get_all_config(self) -> Dict[str, Any]:
        """Return all configuration / Restituisce tutta la configurazione."""
        return self.config.copy()
