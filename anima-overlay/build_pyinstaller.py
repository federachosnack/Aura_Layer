#!/usr/bin/env python
"""
Script di build PyInstaller per Aura Layer.
Eseguire con: python build_pyinstaller.py
"""

import os
import subprocess
import sys
import time
import shutil

# Determina l'interprete Python (usa il venv del progetto se presente, altrimenti sys.executable)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
venv_python = os.path.join(project_root, ".venv", "Scripts", "python.exe")

if os.path.exists(venv_python):
    python_exe = venv_python
elif os.path.exists(sys.executable):
    python_exe = sys.executable
else:
    print("Errore: Nessun interprete Python valido trovato.")
    sys.exit(1)

# Configurazione build PyInstaller
PYINSTALLER_CMD = [
    python_exe,
    "-m",
    "PyInstaller",
    "--name=AuraLayer",
    "--icon=src/loghi/icon.ico",
    "--onefile",
    "--windowed",
    "--noconfirm",
    "--clean",
    "--add-data=src/loghi;loghi",
    "--collect-all=PyQt6",
    "--copy-metadata=pymatting",
    "--copy-metadata=rembg",
    "--hidden-import=PyQt6.QtMultimedia",
    "--hidden-import=PyQt6.QtCore",
    "--hidden-import=PyQt6.QtWidgets",
    "--hidden-import=PyQt6.QtGui",
    "--hidden-import=PyQt6.QtNetwork",
    "--distpath=dist_temp",
    "main.py"
]

def main():
    print("Avvio build PyInstaller per Aura Layer...")
    print("Questo processo può richiedere alcuni minuti...")

    # Termina eventuali processi AuraLayer.exe ancora attivi
    print("Terminazione eventuali processi AuraLayer.exe...")
    subprocess.run(['taskkill', '/F', '/IM', 'AuraLayer.exe'], capture_output=True)

    # Attendi che Windows rilasci gli handle
    print("Attendo 3 secondi per il rilascio degli handle...")
    time.sleep(3)

    # Rimuovi cartella temporanea se esiste
    dist_temp = os.path.join(os.path.dirname(__file__), "dist_temp")
    if os.path.exists(dist_temp):
        print("Rimozione cartella temporanea dist_temp...")
        try:
            shutil.rmtree(dist_temp)
        except PermissionError as e:
            print(f"⚠ Impossibile rimuovere dist_temp: {e}")
            print("Procedo comunque con la build...")

    # Retry logic per la build
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Tentativo di build {attempt + 1}/{max_retries}...")
            result = subprocess.run(PYINSTALLER_CMD, check=True)

            # Build completato con successo
            print("\nBuild completato con successo!")
            print("Executable creato in: dist_temp/AuraLayer.exe")
            print("\nNota: Il build e in dist_temp per evitare conflitti di file bloccati.")
            print("Puoi testare l'exe direttamente da quella cartella.")

            break
        except subprocess.CalledProcessError as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"\n✗ Errore durante la build (tentativo {attempt + 1}): {e}")
                print(f"Attendo {wait_time} secondi prima di riprovare...")
                time.sleep(wait_time)
            else:
                print(f"\n✗ Errore durante la build dopo {max_retries} tentativi: {e}")
                print("Suggerimento: verifica con Resource Monitor quale processo tiene occupata la cartella dist\\AuraLayer")
                sys.exit(1)

if __name__ == "__main__":
    main()
