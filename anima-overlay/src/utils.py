import os
import shutil
import ctypes
import sys
import json
from ctypes import wintypes
from typing import Optional


def get_app_data_dir() -> str:
    """Restituisce il percorso della cartella dati dell'app in %APPDATA%."""
    base_dir = os.getenv('APPDATA') or os.path.expanduser('~')
    app_data_dir = os.path.join(base_dir, 'AuraLayer')

    # Crea la cartella se non esiste
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)

    return app_data_dir


def atomic_write_json(file_path: str, data: dict, indent: int = 2) -> bool:
    """
    Scrive dati JSON in modo atomico (file temporaneo + os.replace)
    per prevenire corruzioni o file troncati a 0 byte in caso di crash o spegnimento improvviso.
    """
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    tmp_path = f"{file_path}.tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, file_path)
        return True
    except Exception as e:
        print(f"Error atomic writing {file_path}: {e}")
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        return False


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


# Handle globale per mantenere in vita il mutex dell'istanza singola
_instance_mutex = None


def check_single_instance() -> bool:
    """
    Verifica se un'altra istanza dell'app è già in esecuzione usando mutex.
    Restituisce True se questa è l'unica istanza, False se ne esiste già una.
    """
    global _instance_mutex

    mutex_name = "AuraLayer_SingleInstance_Mutex"

    kernel32 = ctypes.windll.kernel32
    CreateMutexW = kernel32.CreateMutexW
    CreateMutexW.argtypes = [wintypes.LPCWSTR, wintypes.BOOL, wintypes.LPCWSTR]
    CreateMutexW.restype = wintypes.HANDLE

    GetLastError = kernel32.GetLastError
    GetLastError.argtypes = []
    GetLastError.restype = wintypes.DWORD

    CloseHandle = kernel32.CloseHandle
    CloseHandle.argtypes = [wintypes.HANDLE]
    CloseHandle.restype = wintypes.BOOL

    _instance_mutex = CreateMutexW(None, False, mutex_name)

    if GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        if _instance_mutex:
            CloseHandle(_instance_mutex)
            _instance_mutex = None
        return False

    return True


def resource_path(relative_path: str) -> str:
    """
    Restituisce il percorso assoluto di una risorsa, funzionante sia in sviluppo che in PyInstaller.
    Per PyInstaller, le risorse sono in _MEIPASS.
    In sviluppo cerca sia nella root del progetto sia nella sottocartella src/.
    """
    if getattr(sys, 'frozen', False):
        # Eseguito come PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Eseguito in sviluppo
        base_path = os.path.dirname(os.path.dirname(__file__))

    direct_path = os.path.join(base_path, relative_path)
    if not os.path.exists(direct_path):
        src_path = os.path.join(base_path, "src", relative_path)
        if os.path.exists(src_path):
            return src_path

    return direct_path


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('rcMonitor', wintypes.RECT),
        ('rcWork', wintypes.RECT),
        ('dwFlags', wintypes.DWORD)
    ]


# Inizializzazione 64-bit sicura delle Win32 API per user32
_user32 = ctypes.windll.user32

_user32.GetForegroundWindow.argtypes = []
_user32.GetForegroundWindow.restype = wintypes.HWND

_user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
_user32.GetClassNameW.restype = ctypes.c_int

_user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
_user32.GetWindowRect.restype = wintypes.BOOL

_user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
_user32.MonitorFromWindow.restype = wintypes.HMONITOR

_user32.GetMonitorInfoW.argtypes = [wintypes.HMONITOR, ctypes.POINTER(MONITORINFO)]
_user32.GetMonitorInfoW.restype = wintypes.BOOL

_user32.IsWindowVisible.argtypes = [wintypes.HWND]
_user32.IsWindowVisible.restype = wintypes.BOOL


def is_fullscreen_active(exclude_hwnds: Optional[list] = None) -> bool:
    """
    Rileva se una finestra in primo piano occupa l'intero schermo (es. gioco o video fullscreen).
    Restituisce True se un'applicazione a tutto schermo è attiva, altrimenti False.
    Completamente sicuro per architetture Windows 64-bit e 32-bit.
    """
    try:
        hwnd = _user32.GetForegroundWindow()
        if not hwnd:
            return False

        if exclude_hwnds and hwnd in exclude_hwnds:
            return False

        # Ignora desktop di Windows e barra delle applicazioni
        cls_buf = ctypes.create_unicode_buffer(256)
        _user32.GetClassNameW(hwnd, cls_buf, 256)
        cls_name = cls_buf.value
        if cls_name in ['Progman', 'WorkerW', 'Shell_TrayWnd', 'Shell_SecondaryTrayWnd']:
            return False

        rect = wintypes.RECT()
        if not _user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return False

        # MONITOR_DEFAULTTONEAREST = 2
        hmon = _user32.MonitorFromWindow(hwnd, 2)
        if not hmon:
            return False

        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)
        if not _user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
            return False

        m = mi.rcMonitor
        # Verifica se la finestra copre interamente l'area fisica del monitor
        if rect.left <= m.left and rect.top <= m.top and rect.right >= m.right and rect.bottom >= m.bottom:
            if _user32.IsWindowVisible(hwnd):
                return True

        return False
    except Exception:
        return False
