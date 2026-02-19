"""
GPIO Control Module
Raspberry Pi 5
Controls LED / Relay devices
"""

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

# GPIO Pin Configuration (BCM mode)
LIGHT_PIN = 17
FAN_PIN   = 27

def setup_gpio():
    if not GPIO_AVAILABLE:
        print("⚠ GPIO library not available (simulation mode)")
        return

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_PIN, GPIO.OUT)
    GPIO.setup(FAN_PIN, GPIO.OUT)

    GPIO.output(LIGHT_PIN, GPIO.LOW)
    GPIO.output(FAN_PIN, GPIO.LOW)

def light_on():
    if GPIO_AVAILABLE:
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
    print("💡 Light ON")

def light_off():
    if GPIO_AVAILABLE:
        GPIO.output(LIGHT_PIN, GPIO.LOW)
    print("💡 Light OFF")

def fan_on():
    if GPIO_AVAILABLE:
        GPIO.output(FAN_PIN, GPIO.HIGH)
    print("🌀 Fan ON")

def fan_off():
    if GPIO_AVAILABLE:
        GPIO.output(FAN_PIN, GPIO.LOW)
    print("🌀 Fan OFF")

def cleanup():
    if GPIO_AVAILABLE:
        GPIO.cleanup()

