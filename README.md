# Aura Layer

![License](https://img.shields.io/badge/license-Aura%20Layer-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

Aura Layer is a desktop character overlay application for Windows that lets you place animated characters directly on your desktop.

Characters can remain static, move freely around the screen, interact with screen edges, or react to gravity. You can also add custom characters, animations, audio, and configure appearance and performance settings.

**Status**: Stable Windows release available. Aura Layer is actively maintained and will continue to receive updates, improvements, and new features.

## Download

The latest stable version of Aura Layer is available from the [Releases](https://github.com/federachosnack/Aura_Layer/releases) page.

Each release includes the corresponding executable and release notes. Previous releases will remain available so users can continue using older versions when preferred or when compatibility with a specific version is required.

## Features

- **Desktop Character Overlay**: Display animated characters directly on your Windows desktop
- **Multiple Behaviors**: Choose from static, free walk, random edge, or gravity behaviors
- **Custom Characters**: Add your own characters with custom animations and audio
- **AI Background Removal**: Remove backgrounds from character images using AI (rembg)
- **Multi-language Support**: Available in Italian and English
- **System Tray Integration**: Minimize to system tray with quick access
- **Configurable Settings**: Customize startup behavior, appearance, and performance
- **FPS Control**: Set individual and global FPS limits for performance optimization
- **Click-through Mode**: Allow mouse clicks to pass through characters to the windows underneath

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

To build the executable using PyInstaller:

```bash
python build_pyinstaller.py
```

The executable will be created in the `dist_temp/` directory.

## Usage

1. **Launch the Application**: Run `AuraLayer.exe` or `python main.py`
2. **Open Launcher**: Click the system tray icon and select "Open Launcher"
3. **Add Character**: Click "Add Character" and provide:
   - Character name
   - Animation file (GIF, PNG, or other supported formats)
   - Optional audio file
   - Behavior settings
4. **Launch Character**: Click "Launch" to display the character on your desktop
5. **Customize**: Use the settings tab to configure appearance and behavior

## Character Behaviors

- **Static**: Character stays in one position (can be dragged)
- **Free Walk**: Character moves freely around the screen
- **Random Edge**: Character appears at random screen edges
- **Gravity**: Character falls with gravity physics

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
    ├── main.py                 # Application entry point
    ├── build_pyinstaller.py    # Build script
    ├── requirements.txt        # Python dependencies
    └── src/
        ├── launcher.py          # Main UI window
        ├── character.py         # Character management
        ├── config_manager.py    # Configuration handling
        ├── tray_manager.py      # System tray integration
        ├── translations.py      # Translation system
        ├── background_remover.py # AI background removal
        └── ...
```

## Dependencies

- PyQt6: GUI framework
- Pillow: Image processing
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

## Translation

To add a new language:

1. Add translations to `anima-overlay/src/translations.py`
2. Add the language selector option in `anima-overlay/src/launcher.py`
3. Update the configuration system

## License

Aura Layer is distributed under the Aura Layer License, a custom source-available license.

The license permits:
- Free use for any purpose
- Study and modification of the software
- Private modifications (no obligation to publish source code)
- Free distribution of original and modified versions
- Commercial distribution of substantially modified versions (with significant improvements)

The license restricts:
- Commercial sale of the original software
- Commercial sale of minimally modified versions
- Use of the Aura Layer name to imply official endorsement

See the [LICENSE](LICENSE) file for the complete terms.

## Roadmap

- [ ] Linux support
- [ ] Further multi-monitor improvements
- [ ] Additional interaction features
- [ ] Performance and stability improvements

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

- PyQt6 for the excellent GUI framework
- rembg for AI background removal
- ONNX Runtime for machine learning runtime
- The open-source community for inspiration and tools
