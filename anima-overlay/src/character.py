import json
import os
from typing import Dict, Any, Optional
from src.utils import get_app_data_dir, atomic_write_json


class Character:
    """Rappresenta un personaggio/animazione con la sua configurazione."""
    
    def __init__(self, character_path: str):
        self.character_path = character_path
        self.config = {}
        self.name = ""
        self.animation_file = ""
        self.audio_file = None
        self.behavior = "static"
        self.width = 200
        self.height = 200
        self.draggable = True
        self.speed = 1.0
        self.volume = 0.5
        self.fps = None
        self.scale = None
        self.locked = False
        self.preferred_screen = "auto"
        self.play_audio_on_startup = True

        self.load_config()
        
    def load_config(self):
        """Carica la configurazione dal file JSON del personaggio con gestione recupero da .tmp."""
        config_path = os.path.join(self.character_path, "config.json")
        tmp_path = f"{config_path}.tmp"

        if not os.path.exists(config_path) and os.path.exists(tmp_path):
            try:
                os.replace(tmp_path, config_path)
            except OSError:
                config_path = tmp_path

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # Estrai i campi dalla configurazione con type-coercion e clamping di sicurezza
        self.name = str(self.config.get("name", "Unnamed Character")).strip() or "Unnamed Character"
        self.animation_file = str(self.config.get("animation_file", ""))
        raw_audio = self.config.get("audio_file")
        self.audio_file = str(raw_audio) if raw_audio else None

        valid_behaviors = {"static", "free_walk", "random_edge", "gravity"}
        raw_behavior = self.config.get("behavior", "static")
        self.behavior = raw_behavior if raw_behavior in valid_behaviors else "static"

        try:
            self.width = max(10, min(4000, int(self.config.get("width", 200))))
        except (ValueError, TypeError):
            self.width = 200

        try:
            self.height = max(10, min(4000, int(self.config.get("height", 200))))
        except (ValueError, TypeError):
            self.height = 200

        try:
            self.draggable = bool(self.config.get("draggable", True))
        except Exception:
            self.draggable = True

        try:
            self.speed = max(0.1, min(10.0, float(self.config.get("speed", 1.0))))
        except (ValueError, TypeError):
            self.speed = 1.0

        try:
            self.volume = max(0.0, min(1.0, float(self.config.get("volume", 0.5))))
        except (ValueError, TypeError):
            self.volume = 0.5

        raw_fps = self.config.get("fps", None)
        if raw_fps is not None:
            try:
                self.fps = max(1, min(60, int(raw_fps)))
            except (ValueError, TypeError):
                self.fps = None
        else:
            self.fps = None

        raw_scale = self.config.get("scale", None)
        if raw_scale is not None:
            try:
                self.scale = max(25, min(200, int(raw_scale)))
            except (ValueError, TypeError):
                self.scale = None
        else:
            self.scale = None

        raw_locked = self.config.get("locked", False)
        self.locked = raw_locked in (True, 1, "true", "True")

        self.preferred_screen = str(self.config.get("preferred_screen", "auto"))
        raw_startup_audio = self.config.get("play_audio_on_startup", True)
        self.play_audio_on_startup = raw_startup_audio in (True, 1, "true", "True")
        
    def get_animation_path(self) -> str:
        """Restituisce il percorso completo del file animazione."""
        return os.path.join(self.character_path, self.animation_file)
        
    def get_audio_path(self) -> Optional[str]:
        """Restituisce il percorso completo del file audio, se presente."""
        if self.audio_file:
            return os.path.join(self.character_path, self.audio_file)
        return None

    def update_config(self, **kwargs):
        """Aggiorna i campi della configurazione in memoria validando e sanitizzando i tipi."""
        for key, value in kwargs.items():
            if key == "scale" and value is not None:
                try:
                    value = max(25, min(200, int(value)))
                except (ValueError, TypeError):
                    value = None
            elif key == "fps" and value is not None:
                try:
                    value = max(1, min(60, int(value)))
                except (ValueError, TypeError):
                    value = None
            elif key == "volume" and value is not None:
                try:
                    value = max(0.0, min(1.0, float(value)))
                except (ValueError, TypeError):
                    value = 0.5
            elif key == "behavior" and value is not None:
                valid_behaviors = {"static", "free_walk", "random_edge", "gravity"}
                value = value if value in valid_behaviors else "static"
            elif key == "locked":
                value = value in (True, 1, "true", "True")
            elif key in ("width", "height") and value is not None:
                try:
                    value = max(10, min(4000, int(value)))
                except (ValueError, TypeError):
                    value = 200

            self.config[key] = value
            # Aggiorna anche l'attributo corrispondente se esiste
            if hasattr(self, key):
                setattr(self, key, value)

    def save_config(self):
        """Salva la configurazione corrente nel file JSON in modo atomico."""
        config_path = os.path.join(self.character_path, "config.json")
        atomic_write_json(config_path, self.config)
        
    def has_audio(self) -> bool:
        """Verifica se il personaggio ha un file audio."""
        return self.audio_file is not None and os.path.exists(self.get_audio_path())

    def to_dict(self) -> Dict[str, Any]:
        """Converte il personaggio in dizionario completo per serializzazione."""
        return {
            "path": self.character_path,
            "name": self.name,
            "animation_file": self.animation_file,
            "audio_file": self.audio_file,
            "behavior": self.behavior,
            "width": self.width,
            "height": self.height,
            "draggable": self.draggable,
            "speed": self.speed,
            "volume": self.volume,
            "fps": self.fps,
            "scale": self.scale,
            "locked": self.locked,
            "preferred_screen": self.preferred_screen,
            "play_audio_on_startup": self.play_audio_on_startup
        }


class CharacterManager:
    """Gestisce una collezione di personaggi."""

    def __init__(self, characters_dir: Optional[str] = None):
        # Se non viene passato un percorso, usa quello di default in APPDATA
        if characters_dir is None:
            self.characters_dir = os.path.join(get_app_data_dir(), "characters")
        else:
            self.characters_dir = characters_dir

        self.characters: Dict[str, Character] = {}
        self.load_all_characters()
        
    def load_all_characters(self):
        """Carica tutti i personaggi dalla directory characters."""
        self.characters = {}  # Svuota prima di ripopolare

        if not os.path.exists(self.characters_dir):
            os.makedirs(self.characters_dir)
            return

        for item in os.listdir(self.characters_dir):
            character_path = os.path.join(self.characters_dir, item)
            if os.path.isdir(character_path):
                config_path = os.path.join(character_path, "config.json")
                if os.path.exists(config_path):
                    try:
                        character = Character(character_path)
                        self.characters[item] = character
                    except Exception as e:
                        print(f"Error loading character {item}: {e}")
                        
    def get_character(self, name: str) -> Optional[Character]:
        """Ottiene un personaggio per nome."""
        return self.characters.get(name)
        
    def add_character(self, character_path: str) -> Optional[Character]:
        """Aggiunge un nuovo personaggio."""
        character_name = os.path.basename(character_path)
        try:
            character = Character(character_path)
            self.characters[character_name] = character
            return character
        except Exception as e:
            print(f"Error adding character: {e}")
            return None
            
    def remove_character(self, name: str) -> bool:
        """Rimuove un personaggio."""
        if name in self.characters:
            del self.characters[name]
            return True
        return False
        
    def get_all_characters(self) -> Dict[str, Character]:
        """Restituisce tutti i personaggi."""
        return self.characters
        
    def get_character_names(self) -> list[str]:
        """Restituisce i nomi di tutti i personaggi."""
        return list(self.characters.keys())
