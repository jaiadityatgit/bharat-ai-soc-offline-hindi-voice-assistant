# Setup Guide

## Requirements

- Raspberry Pi 5
- Raspberry Pi OS (64-bit)
- INMP441 I2S Microphone
- Speaker (Bluetooth or 3.5mm)
- Python 3

## System Preparation

Update system:

sudo apt update  
sudo apt upgrade -y  

Install dependencies:

sudo apt install python3-pip python3-venv portaudio19-dev \
espeak-ng alsa-utils sox libsox-fmt-all pulseaudio

## Python Environment

Create virtual environment:

python3 -m venv venv  
source venv/bin/activate  

Install packages:

pip install vosk pyaudio

## Model Setup

Download Vosk Hindi model and extract into project directory.

Download Piper Hindi voice model for text-to-speech.

## Audio Configuration

Check microphone:

arecord -l

Test microphone:

arecord -D hw:2,0 -f S16_LE -r 16000 -c 1 -d 5 test.wav  
aplay test.wav

## Running Assistant

Activate environment:

source venv/bin/activate  

Run:

python src/final_hindi_assistant.py

