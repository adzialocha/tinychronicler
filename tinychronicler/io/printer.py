from loguru import logger
from PIL import Image
from serial.serialutil import SerialException
from thermalprinter import ThermalPrinter

from tinychronicler.database import schemas

THERMAL_PRINTER_TTY = "/dev/serial0"
TINY_CHRONICLER_IMAGE = "tc.jpg"

printer = None
try:
    printer = ThermalPrinter(port=THERMAL_PRINTER_TTY)
except SerialException as err:
    logger.error("Could not set up printer serial connection: {}".format(err))


def print_score(composition: schemas.Composition, score: str):
    if printer is None:
        raise Exception("Printer is not set up")
    printer.feed(3)
    printer.out("Tiny Chronicler @( * O * )@")
    printer.feed()
    img = Image.open(TINY_CHRONICLER_IMAGE)
    img.thumbnail((192, 192))
    printer.image(img)
    printer.out(composition.title, double_height=True)
    printer.out(composition.created_at.strftime(
        "%d.%m.%Y %H:%M"))
    printer.feed()
    for line in score.splitlines():
        printer.out(line, rotate=True)
    printer.feed(4)


def print_test_page():
    if printer is None:
        raise Exception("Printer is not set up")
    printer.out("╔══════════════════════════════╗")
    printer.out("║ Hello,                       ║")
    printer.out("║           Tiny Chronicler!   ║")
    printer.out("║      <3                      ║")
    printer.out("╚══════════════════════════════╝")
    printer.feed(3)
