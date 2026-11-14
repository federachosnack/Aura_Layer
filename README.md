# Aura Layer

![License](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

Aura Layer is a desktop character overlay application for Windows that lets you place animated characters directly on your desktop.

Characters can remain static, move freely around the screen, interact with screen edges, or react to gravity. You can also add custom characters, animations, audio, and configure appearance and performance settings.

**Status**: Stable Windows v1.2.0 release available. Aura Layer is actively maintained and will continue to receive updates, improvements, and new features.

## Download

The latest stable version of Aura Layer is available from the [Releases](https://github.com/federachosnack/Aura_Layer/releases) page.

Each release includes the corresponding executable and release notes. Previous releases will remain available so users can continue using older versions when preferred or when compatibility with a specific version is required.

## Features

- **Desktop Character Overlay**: Display animated characters directly on your Windows desktop
- **Cyber Glass Fluent UI**: Modern translucent launcher with glassmorphic styling, neon accents, and smooth transitions
- **Toss & Fling Ballistic Physics**: Fling characters across screens with realistic inertia, damping bounces, and zero-CPU sleep on rest
- **Multi-Monitor Dynamic Engine**: Seamless multi-monitor support with real-time drag synchronization, coordinate scaling, and disconnect recovery
- **Desktop Context Menu**: Right-click active characters directly on your desktop to lock/unlock, switch behavior, test audio, or move between monitors
- **Safe Overflow Mode**: Free positioning of static characters docked along screen edges and overlapping the Windows taskbar
- **Character Package System (.aura)**: One-click export and import of portable character bundles containing animations, audio, and metadata
- **Global System Hotkey (Ctrl+Alt+H)**: Native Windows shortcut to instantly hide or show all desktop companions, even during full-screen games
- **Audio Customization**: Custom sound/voice per character with individual volume control, startup toggle, and one-click removal
- **Multiple Behaviors**: Choose from static, free walk, smooth peek-a-boo random edge, or interactive gravity
- **AI Background Removal**: Remove backgrounds from character images using AI (rembg) with lazy loading for instant startup
- **Multi-language Support**: Complete, symmetrical Italian and English localization
- **System Tray Integration**: Minimize to system tray with quick access and emergency unlock controls
- **Configurable Settings**: Customize startup behavior, appearance, and performance
- **FPS Control**: Set individual and global FPS limits with precise numeric keyboard input
- **Click-through Mode**: Allow mouse clicks to pass through characters to the windows underneath
- **Crash-Proof & Atomic Architecture**: Atomic configuration writes, corrupted file recovery, and strict 64-bit ctypes safety

## Installation

### From Executable

1. Download the desired release from the [Releases](https://github.com/federachosnack/Aura_Layer/releases) page
2. Run `AuraLayer.exe`
3. The application will start in the system tray

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/federachosnack/Aura_Layer.git
   cd Aura_Layer/anima-overlay
   ```

2. Create a virtual environment:
   ```bash
   python -m venv ../.venv
   ../.venv/Scripts/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Building Executable

To build the standalone executable, install development dependencies and run the build script:

```bash
pip install -r requirements-dev.txt
python build_pyinstaller.py
```

The executable will be created in the `dist_temp/` directory.

## Usage

1. **Launch the Application**: Run `AuraLayer.exe` or `python main.py`
2. **Open Launcher**: Click the system tray icon and select "Open Launcher"
3. **Add Character**: Click "Add Character" and provide:
   - Character name
   - Animation file (GIF, APNG, WebP, PNG, or other supported formats)
   - Optional audio file
   - Behavior settings
4. **Launch Character**: Click "Launch" to display the character on your desktop
5. **Customize**: Use the settings tab to configure appearance and behavior

## Character Behaviors

- **Static**: Character stays in place with Safe Overflow support (can overlap borders and taskbar)
- **Free Walk**: Character moves freely across screens with boundary detection
- **Random Edge (Peek-a-boo)**: Smooth cubic easing edge peek, pause, and retreat behavior
- **Gravity (Toss & Fling)**: Natural gravity and drag-throw physics with soft bounce damping and instant zero-CPU sleep on rest

## Settings

- **Startup**: Start with Windows, start minimized
- **Appearance**: Theme selection, grid size
- **Performance**: Global FPS limit, fullscreen pause
- **Language**: Choose between Italian and English

## AI Background Removal

The application includes AI-powered background removal using rembg:

1. Select a character in the launcher
2. Click "Remove background with AI"
3. The application will process the image and create a transparent background version
4. Original files are automatically backed up

**Note**: The first use requires an internet connection to download the AI model (~176MB).

## Project Structure

```
Aura_Layer/
├── .gitignore
├── LICENSE
├── README.md
└── anima-overlay/
    ├── main.py                 # Application entry point & tray lifecycle
    ├── build_pyinstaller.py    # Standalone PyInstaller compilation script
    ├── requirements.txt        # Runtime dependencies
    ├── requirements-dev.txt    # Build & testing dependencies
    ├── tests/                  # Automated test suite (pytest / unittest)
    │   ├── test_character.py
    │   ├── test_utils_security.py
    │   ├── test_i18n.py
    │   └── test_hook_and_lifecycle.py
    └── src/
        ├── launcher.py          # Cyber Glass UI window & package manager
        ├── character.py         # Character model, type validation & clamping
        ├── overlay_window.py    # Desktop overlay & singleton WinEvent hook
        ├── behaviors.py         # Physics (Gravity, FreeWalk, RandomEdge)
        ├── config_manager.py    # Atomic configuration manager
        ├── tray_manager.py      # System tray integration
        ├── translations.py      # Symmetrical localization (245 keys)
        ├── background_remover.py # AI background removal
        └── utils.py             # Atomic I/O, security, app logging
```

## Dependencies

- PyQt6: GUI framework (GPLv3)
- Pillow: Image and animation processing
- rembg: AI background removal
- onnxruntime: Machine learning runtime
- pywin32: Windows API integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

Run the full automated test suite using unittest or pytest:

```bash
cd anima-overlay
python -m unittest discover -s tests -p "test_*.py"
```

## License

Aura Layer is open-source software licensed under the **GNU General Public License v3.0 (GPLv3)** in compliance with the PyQt6 framework requirements. See the [LICENSE](LICENSE) file for complete terms.

## Roadmap

- [ ] Linux / Steam Deck support (Wayland & X11 transparent overlays)
- [ ] macOS support (Metal transparency layer)
- [ ] PySide6 (LGPL) migration option
- [ ] Spatialized 3D audio effects based on character screen coordinates
- [ ] Community online repository for one-click `.aura` package sharing

## Troubleshooting

If you encounter unexpected behavior or errors:
- Diagnostics and operational logs are stored in `%APPDATA%\AuraLayer`:
  - `app.log`: Operational events, warnings, and character loading diagnostics.
  - `crash.log`: Python tracebacks with automatic deduplication and runtime rotation.
  - `native_crash.log`: Low-level C/Win32 faulthandler crash dumps.
- To open the logs folder: Press `Win + R`, type `%APPDATA%\AuraLayer` and press Enter.
- When reporting an issue on GitHub, please attach these log files.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

- PyQt6 for the excellent GUI framework
- rembg for AI background removal
- ONNX Runtime for machine learning runtime
- The open-source community for inspiration and tools
