import asyncio

import serial
from loguru import logger
from serial.serialutil import SerialException

ARDUINO_TTY = '/dev/ttyACM0'
BAUD_RATE = 19200

ser = None
try:
    ser = serial.Serial(port=ARDUINO_TTY, baudrate=BAUD_RATE, timeout=1)
    ser.reset_input_buffer()
except SerialException as err:
    logger.error("Could not set up arduino serial connection: {}".format(err))


def send_command(command_id: int):
    if ser is None:
        return
    ser.write(str(command_id).encode('utf-8'))


async def run_test_sequence():
    if ser is None:
        raise Exception("Arduino is not set up")
    print_background()
    await asyncio.sleep(1)
    print_left_eye()
    await asyncio.sleep(1)
    print_right_eye()
    await asyncio.sleep(1)
    print_mouth()
    await asyncio.sleep(1)
    reset_mouth()
    await asyncio.sleep(1)
    reset_eyes()
    await asyncio.sleep(1)
    print_both_eyes()
    await asyncio.sleep(1)
    reset_all()


def print_background():
    send_command(1)


def print_left_eye():
    send_command(2)


def print_right_eye():
    send_command(3)


def print_both_eyes():
    send_command(4)


def print_mouth():
    send_command(5)


def reset_eyes():
    send_command(6)


def reset_mouth():
    send_command(7)


def reset_all():
    send_command(0)
