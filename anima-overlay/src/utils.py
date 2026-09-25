import os
import shutil
import ctypes
import sys
from ctypes import wintypes
from typing import Optional


def get_app_data_dir() -> str:
    """Restituisce il percorso della cartella dati dell'app in %APPDATA%."""
    app_data_dir = os.path.join(os.getenv('APPDATA'), 'AuraLayer')

    # Crea la cartella se non esiste
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)

    return app_data_dir


def migrate_from_local_if_needed() -> None:
    """Migra i dati dalla cartella locale a %APPDATA% se necessario."""
    app_data_dir = get_app_data_dir()

    # Percorsi locali (vecchia posizione)
    local_characters_dir = "characters"
    local_config_file = "config.json"

    # Percorsi in APPDATA (nuova posizione)
    app_characters_dir = os.path.join(app_data_dir, "characters")
    app_config_file = os.path.join(app_data_dir, "config.json")

    # Migra characters se esiste localmente e non in APPDATA
    if os.path.exists(local_characters_dir) and not os.path.exists(app_characters_dir):
        print("Migrazione cartella characters in corso...")
        try:
            shutil.copytree(local_characters_dir, app_characters_dir)
            print(f"Characters migrati da {local_characters_dir} a {app_characters_dir}")
        except Exception as e:
            print(f"Errore durante la migrazione characters: {e}")

    # Migra config se esiste localmente e non in APPDATA
    if os.path.exists(local_config_file) and not os.path.exists(app_config_file):
        print("Migrazione config.json in corso...")
        try:
            shutil.copy2(local_config_file, app_config_file)
            print(f"Config migrato da {local_config_file} a {app_config_file}")
        except Exception as e:
            print(f"Errore durante la migrazione config: {e}")


def check_single_instance() -> bool:
    """
    Verifica se un'altra istanza dell'app è già in esecuzione usando mutex.
    Restituisce True se questa è l'unica istanza, False se ne esiste già una.
    """
    # Nome univoco per il mutex
    mutex_name = "AuraLayer_SingleInstance_Mutex"

    # Definizione funzioni Win32
    CreateMutexW = ctypes.windll.kernel32.CreateMutexW
    CreateMutexW.argtypes = [wintypes.LPCWSTR, wintypes.BOOL, wintypes.LPCWSTR]
    CreateMutexW.restype = wintypes.HANDLE

    GetLastError = ctypes.windll.kernel32.GetLastError
    GetLastError.argtypes = []
    GetLastError.restype = wintypes.DWORD

    # Tenta di creare il mutex
    mutex = CreateMutexW(None, False, mutex_name)

    if GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        # Il mutex esiste già, quindi c'è un'altra istanza in esecuzione
        return False

    return True


def resource_path(relative_path: str) -> str:
    """
    Restituisce il percorso assoluto di una risorsa, funzionante sia in sviluppo che in PyInstaller.
    Per PyInstaller, le risorse sono in _internal.
    """
    if getattr(sys, 'frozen', False):
        # Eseguito come PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Eseguito in sviluppo
        base_path = os.path.dirname(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)
