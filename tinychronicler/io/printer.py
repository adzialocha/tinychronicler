from loguru import logger
from serial.serialutil import SerialException
from thermalprinter import ThermalPrinter

THERMAL_PRINTER_TTY = '/dev/ttyAMA0'

printer = None
try:
    printer = ThermalPrinter(port=THERMAL_PRINTER_TTY)
except SerialException as err:
    logger.error("Could not set up printer serial connection: {}".format(err))


def print_composition():
    if printer is None:
        raise Exception("Printer is not set up")

    # @TODO
    printer.out("Test")


def print_test_page():
    if printer is None:
        raise Exception("Printer is not set up")

    printer.out("□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□")
    printer.out("Hello,")
    printer.out("                Tiny Chronicler!")
    printer.out("           <3", bold=True)
    printer.out("□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□")
    printer.feed(5)
