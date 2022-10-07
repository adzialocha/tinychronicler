from thermalprinter import ThermalPrinter

THERMAL_PRINTER_TTY = '/dev/ttyAMA0'

printer = ThermalPrinter(port=THERMAL_PRINTER_TTY)


def print_composition():
    # @TODO
    printer.out("Test")
