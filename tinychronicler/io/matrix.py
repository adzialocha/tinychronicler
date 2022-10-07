import serial

ARDUINO_TTY = '/dev/ttyUSB0'
BAUD_RATE = 19200

ser = serial.Serial(port=ARDUINO_TTY, baudrate=BAUD_RATE, timeout=1)


def send_command(command_id: int):
    ser.write(str(command_id).encode('utf-8'))

# @TODO: Define all commands
