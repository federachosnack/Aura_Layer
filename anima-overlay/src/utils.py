import os
import shutil
import ctypes
import sys
import json
import re
import zipfile
import traceback
import time
import faulthandler
from pathlib import Path
from datetime import datetime
from ctypes import wintypes
from typing import Optional, Tuple


def sanitize_filename(name: str, default: str = "character") -> str:
    """
    Sanitizza un nome file o cartella per Windows:
    - Prende solo il basename (elimina ../../ e percorsi assoluti).
    - Rimuove caratteri vietati nei filesystem Windows (\\ / : * ? " < > |).
    - Rimuove caratteri di controllo non stampabili.
    - Evita nomi di periferica riservati di Windows (CON, PRN, AUX, NUL, COM1-9, LPT1-9).
    """
    if not name:
        return default
    base = os.path.basename(name).strip()
    cleaned = re.sub(r'[\\/*?:"<>|\x00-\x1f]', '', base).strip()
    cleaned = cleaned.rstrip('. ')
    reserved = {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(1, 10)} | {f"lpt{i}" for i in range(1, 10)}
    stem, _ = os.path.splitext(cleaned)
    if cleaned.lower() in reserved or stem.lower() in reserved or not cleaned:
        return default
    return cleaned


def validate_aura_zip(zip_file: zipfile.ZipFile, max_files: int = 100, max_uncompressed_bytes: int = 250 * 1024 * 1024) -> Tuple[bool, str]:
    """
    Verifica che il file ZIP di un pacchetto .aura sia sicuro:
    - Non superi il numero massimo di file consentito.
    - Non superi la dimensione decompressa massima (protezione zip-bomb).
    - Nessun percorso contenga directory traversal (.. come componente di cartella o path assoluto).
    Restituisce (True, "") oppure (False, codice_errore).
    """
    total_size = 0
    infolist = zip_file.infolist()
    if len(infolist) > max_files:
        return False, "ERR_TOO_MANY_FILES"

    for info in infolist:
        total_size += info.file_size
        if total_size > max_uncompressed_bytes:
            return False, "ERR_UNCOMPRESSED_SIZE"
        
        # Verifica segmenti di percorso individuali per bloccare '..' senza bloccare file come '..foo.png'
        # e blocca percorsi con drive (C:) o root (/ o \) su Windows
        p = Path(info.filename)
        if p.drive or p.root or p.is_absolute() or any(part == ".." for part in p.parts):
            return False, "ERR_UNSAFE_PATH"

    return True, ""


_last_crash_dialog_time = 0.0
_last_error_signature = ""
_repeated_error_count = 0
_last_log_write_time = 0.0


def install_global_exception_handler() -> None:
    """
    Installa un gestore globale di eccezioni (sys.excepthook) e abilita faulthandler
    per registrare crash nativi e non gestiti in %APPDATA%/AuraLayer/crash.log.
    """
    log_dir = get_app_data_dir()
    crash_file = os.path.join(log_dir, "crash.log")
    native_crash_file = os.path.join(log_dir, "native_crash.log")

    # Rotazione iniziale del crash log prima di agganciare qualsiasi descrittore di file
    try:
        if os.path.exists(crash_file) and os.path.getsize(crash_file) > 1024 * 1024:
            old_log = os.path.join(log_dir, "crash.old.log")
            if os.path.exists(old_log):
                os.remove(old_log)
            os.rename(crash_file, old_log)
    except OSError:
        pass

    # Abilita faulthandler su un file dedicato per tracciare hard crash C/Win32 di ctypes
    try:
        fh_native = open(native_crash_file, "a", encoding="utf-8")
        faulthandler.enable(file=fh_native)
    except Exception:
        pass

    def excepthook(exc_type, exc_value, exc_traceback):
        global _last_crash_dialog_time, _last_error_signature, _repeated_error_count, _last_log_write_time
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        last = traceback.extract_tb(exc_traceback)[-1] if exc_traceback else None
        err_sig = f"{exc_type.__name__}@{last.filename}:{last.lineno}" if last else exc_type.__name__
        now_mono = time.monotonic()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Se è lo stesso identico errore ripetuto rapidamente (finestra scorrevole), raggruppa e deduplica
            if err_sig == _last_error_signature and (now_mono - _last_log_write_time < 2.0):
                _repeated_error_count += 1
                _last_log_write_time = now_mono
            else:
                if _repeated_error_count > 0:
                    with open(crash_file, "a", encoding="utf-8") as f:
                        f.write(f"[{now_str}] (Errore precedente {_last_error_signature} ripetuto {_repeated_error_count} volte)\n")
                    _repeated_error_count = 0

                # Rotazione runtime del file crash.log se supera 1 MB
                try:
                    if os.path.exists(crash_file) and os.path.getsize(crash_file) > 1024 * 1024:
                        old_log = os.path.join(log_dir, "crash.old.log")
                        if os.path.exists(old_log):
                            os.remove(old_log)
                        os.rename(crash_file, old_log)
                except OSError:
                    pass

                _last_error_signature = err_sig
                _last_log_write_time = now_mono

                tb_lines = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                entry = f"\n{'='*70}\n[CRASH REPORT - {now_str}]\n{tb_lines}{'='*70}\n"

                with open(crash_file, "a", encoding="utf-8") as f:
                    f.write(entry)
                    f.flush()
        except Exception:
            pass

        # Mostra dialog di avviso con rate-limiting (massimo 1 ogni 30 secondi) per evitare cascate di popup
        try:
            if "unittest" not in sys.modules and (now_mono - _last_crash_dialog_time > 30.0):
                _last_crash_dialog_time = now_mono
                from PyQt6.QtWidgets import QApplication, QMessageBox
                if QApplication.instance():
                    try:
                        from .translations import t
                        title = t("crash_critical_title", "Aura Layer - Errore Critico")
                        msg_template = t("crash_critical_msg", "Si è verificato un errore imprevisto.\n\nI dettagli sono stati salvati in:\n{path}")
                        msg = msg_template.format(path=crash_file)
                    except Exception:
                        title = "Aura Layer - Errore Critico"
                        msg = f"Si è verificato un errore imprevisto.\n\nI dettagli sono stati salvati in:\n{crash_file}"

                    QMessageBox.critical(None, title, msg)
        except Exception:
            pass

        if sys.__excepthook__:
            sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = excepthook


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

    # Percorsi locali basati sulla directory radice dell'app
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_characters_dir = os.path.join(base_dir, "characters")
    local_config_file = os.path.join(base_dir, "config.json")

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
