# Live2D Functionality from Open-LLM-VTuber

## Overview
The Open-LLM-VTuber project implements Live2D functionality using PixiJS and the Live2D Cubism SDK. The system allows for interactive 2D characters with emotion expressions, voice synchronization, and gesture interactions.

## Key Components

### 1. Backend Implementation (Python)
- **Live2dModel Class** (`src/open_llm_vtuber/live2d_model.py`):
  - Handles Live2D model information and emotion mapping
  - Parses emotion keywords from text responses (e.g., `[joy]`, `[anger]`, `[surprise]`)
  - Maps emotions to specific expression indices in the model
  - Manages model dictionary and configuration

### 2. Model Configuration
- **Model Dictionary** (`model_dict.json`):
  ```json
  [
    {
      "name": "mao_pro",
      "url": "/live2d-models/mao_pro/runtime/mao_pro.model3.json",
      "kScale": 0.5,
      "initialXshift": 0,
      "initialYshift": 0,
      "kXOffset": 1150,
      "idleMotionGroupName": "Idle",
      "emotionMap": {
        "neutral": 0,
        "anger": 2,
        "disgust": 2,
        "fear": 1,
        "joy": 3,
        "smirk": 3,
        "sadness": 1,
        "surprise": 3
      },
      "tapMotions": {
        "HitAreaHead": { "": 1 },
        "HitAreaBody": { "": 1 }
      }
    }
  ]
  ```

### 3. Frontend Implementation (JavaScript/React)
- **Live2D React Component**: Handles rendering and interaction
- **LAppAdapter Class**: Provides interface to Live2D Cubism framework
- **WebSocket Integration**: Synchronizes emotions and expressions with backend

### 4. Core Live2D Files
- **Model Files**: `.model3.json`, `.moc3`, `.physics3.json`
- **Cubism Core**: `live2dcubismcore.js`, `live2d.min.js`
- **Runtime Libraries**: Various WASM and ONNX files for audio processing

### 5. Server Integration
- **FastAPI Server** (`src/open_llm_vtuber/server.py`):
  - Serves Live2D models via `/live2d-models` endpoint
  - Provides model information via `/live2d-models/info` endpoint
  - Handles WebSocket communication for emotion control

## Key Features

### Emotion Recognition and Control
- Parses emotion keywords from AI responses
- Maps emotions to specific expression indices
- Real-time emotion switching based on conversation context

### Interactive Elements
- Click/tap detection on character body parts
- Gesture responses to user interactions
- Voice synchronization with character mouth movements

### Model Management
- Dynamic model loading and switching
- Multiple character support
- Expression and motion management

## Technical Architecture

### Backend Flow:
1. AI generates response with emotion keywords (e.g., "[joy] Hello there!")
2. Live2dModel class extracts emotion tags
3. WebSocket sends emotion data to frontend
4. Frontend updates character expression

### Frontend Flow:
1. PixiJS renderer displays Live2D character
2. WebSocket receives emotion data
3. LAppAdapter updates character expression
4. Audio playback triggers lip-sync animations

## File Structure
```
live2d-models/
├── mao_pro/
│   └── runtime/
│       ├── mao_pro.model3.json
│       ├── mao_pro.moc3
│       ├── mao_pro.physics3.json
│       └── textures/
└── shizuku/
    └── runtime/
        ├── shizuku.model3.json
        ├── shizuku.moc3
        ├── shizuku.physics3.json
        └── textures/
```

## Integration Points
- WebSocket communication for emotion control
- REST API for model information
- Audio playback synchronization
- Gesture/touch interaction handling