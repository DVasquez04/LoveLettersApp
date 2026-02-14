Overview

Purpose: simple, offline app to reveal random love letters by mood and save favorites.
Platform: Windows executable; no install or internet required.
Data: reads text files from the letters folders, saves favorites locally.
Features

Moods: opens a random letter from mood folders.
Anti-repeat: avoids showing the same letter twice in a row.
Favorites: add/remove; view and reopen saved letters later.
Popups: centered, on top, and close via the internal button.
About: short message you can personalize.
How To Use

Run: open LoveLettersApp.exe.
Navigate: use sidebar (Home, Moods, Favoritos, About).
Reveal: click “Revelar Carta” under a mood.
Save: click “Agregar a favoritos” in a letter popup.
Open saved: in Favoritos, click the envelope to view; use “Eliminar” to remove.
Folder Structure

App: LoveLettersApp.py
Letters: letters → subfolders per mood (e.g., Feliz, Triste), each with .txt files.
Assets: assets → app.ico icon and any future images.
Favorites file: Favoritas.txt created next to the executable.
Favorites & Persistence

Format: saves entries as Mood:Index in Favoritas.txt.
Location: stored beside the .exe for portability.
Customize

App title: edit APP_TITLE in LoveLettersApp.py.
Welcome message: update the footer label text in LoveLettersApp.py.
Moods list: add/remove mood names in _ensure_moods_section() within LoveLettersApp.py.
Folder mapping: adjust MOOD_DIR_MAP so mood names match folder names in letters.
Colors per mood: tweak MOOD_ACCENT_COLORS in LoveLettersApp.py for blocks and accents.
Emojis: edit mood_symbols in _ensure_moods_section() to change the icon per mood.
Icon: replace app.ico and rebuild (see below).
Text content: add .txt letters under letters/<mood> — one letter per file.
Build From Source (optional)

Requirements: Python 3.11, customtkinter, Pillow, PyInstaller.
Install:
python -m pip install customtkinter pillow pyinstaller

Build folder-based exe (recommended for Windows):
python -m PyInstaller --clean --name LoveLettersApp --onedir --noconsole `
  --icon assets\app.ico `
  --add-data "assets;assets" `
  --add-data "letters;letters" `
  LoveLettersApp.py

Run: open LoveLettersApp.exe.
Note: the app auto-detects bundled assets and letters and writes Favoritas.txt next to the exe for easy sharing.
