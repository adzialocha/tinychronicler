import serial
from loguru import logger
from serial.serialutil import SerialException

ARDUINO_TTY = '/dev/ttyUSB0'
BAUD_RATE = 19200

ser = None
try:
    ser = serial.Serial(port=ARDUINO_TTY, baudrate=BAUD_RATE, timeout=1)
except SerialException as err:
    logger.error("Could not set up arduino serial connection: {}".format(err))


def send_command(command_id: int):
    if ser is None:
        raise Exception("Arduino is not set up")
    ser.write(str(command_id).encode('utf-8'))


def run_test_sequence():
    send_command(1)


# @TODO: Define all commands
