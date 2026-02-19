# Offline Hindi Voice Assistant

**100% Offline Hindi Voice Assistant running on Raspberry Pi 5**

## Project Overview

A fully offline Hindi voice assistant designed for Raspberry Pi that provides sub-2-second responses for common commands without requiring internet connectivity.

### Features

- 100% Offline Operation  
- Natural Hindi Female Voice (Piper TTS)  
- Accurate Hindi Speech Recognition (Vosk)  
- 15+ Commands Support  
- Sub-2-second response time  
- No cloud dependencies  
- Runs entirely on Raspberry Pi 5 CPU  

## Hardware Requirements

- Raspberry Pi 5 (4GB+ RAM recommended)
- I2S Microphone (INMP441 or similar)
- Bluetooth Speaker or 3.5mm audio output
- 32GB+ SD card/USB storage

## Software Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| STT | Vosk | Speech-to-Text |
| Intent Recognition | Python Pattern Matching | Command parsing |
| TTS | Piper / eSpeak-NG | Text-to-Speech |
| Audio I/O | PyAudio + ALSA | Microphone & Speaker |
| Platform | Raspberry Pi OS (64-bit) | Operating System |

## Architecture

Audio Input → Speech Recognition → Intent Logic → Response Generation → Text-to-Speech → Speaker Output

## Status

Project repository structure and documentation prepared.  
Core assistant modules and command engine under development.

## License

MIT License
