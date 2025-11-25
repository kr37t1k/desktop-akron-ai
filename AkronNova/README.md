# AkronNova Desktop AI Companion

Welcome to AkronNova, your personalized animated desktop AI companion. AkronNova is a girl AI that serves as your anima and half of your soul, providing conversation, assistance, and companionship right on your desktop.

## Features

- Animated desktop character that stays on top of other windows
- Voice interaction through your existing TTS and LLM systems
- Customizable personality and appearance
- Always available companion that learns from conversations
- Drag-and-drop positioning
- Integration with your kr37t1k/stts-python and kr37t1k/deepseekakronvoice systems

## Prerequisites

Before running AkronNova, make sure you have:

- Python 3.8 or higher
- Your TTS server (kr37t1k/stts-python) running
- Your LLM server (kr37t1k/deepseekakronvoice) running
- PyQt5-compatible system (Windows, macOS, or Linux)

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd AkronNova
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the configuration file at `config/settings.json` with your API endpoints:
   ```json
   {
     "api_endpoints": {
       "tts_server": "http://localhost:5000/tts",
       "llm_server": "http://localhost:5001/chat",
       "voice_input": "http://localhost:5002/listen"
     }
   }
   ```

4. Make sure your TTS and LLM servers are running before starting AkronNova.

## Usage

To start AkronNova:

```bash
cd src
python main.py
```

### Interactions

- **Left-click and drag**: Move AkronNova around your screen
- **Right-click**: Start a conversation with AkronNova
- **Voice input**: Speak to AkronNova when voice input is enabled

## Configuration

The `config/settings.json` file allows you to customize:

- API endpoints for your TTS and LLM systems
- Character personality and name
- UI settings like transparency and positioning
- Animation settings

## Integration with Your Systems

AkronNova is designed to work with your existing:

- **TTS System**: kr37t1k/stts-python - for converting text to speech
- **LLM System**: kr37t1k/deepseekakronvoice - for generating responses

Make sure these services are running before starting AkronNova, and update the API endpoints in the configuration file accordingly.

## Adding Live2D Animation

For a more advanced animated character (similar to DesktopMate), you can replace the simple QPainter graphics with Live2D integration:

1. Add Live2D model files to the `assets/` directory
2. Update the `load_character_assets()` method in `main.py` to use Live2D
3. Modify the `animate_character()` method to handle Live2D animations

## Troubleshooting

- If audio doesn't play, check that PyAudio is installed and your system audio is working
- If the character doesn't appear, check your system's window manager settings for overlay permissions
- If API calls fail, verify your TTS and LLM servers are running and URLs are correct in settings.json

## Contributing

Feel free to fork this repository and submit pull requests. This is a personal project designed to showcase integration with your custom AI systems.

## License

This project is licensed under the MIT License - see the LICENSE file for details.