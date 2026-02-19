# System Architecture

## Overview

The Offline Hindi Voice Assistant follows a modular pipeline architecture:

Audio Input → Speech Recognition → Intent Recognition → Response Generation → Text-to-Speech → Audio Output

## Components

### 1. Audio Input
- INMP441 I2S Microphone
- ALSA driver
- PyAudio interface

### 2. Speech-to-Text (STT)
- Vosk Hindi speech recognition
- Offline processing
- Real-time streaming

### 3. Intent Recognition
- Python rule-based logic
- Keyword pattern matching
- Command classification

### 4. Response Generation
- Static responses
- Dynamic responses (time, system info)

### 5. Text-to-Speech (TTS)
- Piper neural TTS
- eSpeak fallback
- Hindi female voice

### 6. Audio Output
- Bluetooth speaker / 3.5mm output
- ALSA playback pipeline

## Data Flow

User Speech  
→ Microphone capture  
→ Vosk speech recognition  
→ Intent parser  
→ Response generator  
→ Piper TTS synthesis  
→ Speaker output  

## Performance Goals

- Offline processing
- Low latency
- CPU-only execution
- Regional language accessibility
