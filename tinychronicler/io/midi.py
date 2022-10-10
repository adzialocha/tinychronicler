import asyncio
from threading import Event
import time

import mido
from mido.ports import MultiPort
from loguru import logger

from .osc import send_midi_note

INSTRUMENT_ID = 2

event = Event()


def received_message(message):
    logger.debug(message)
    send_midi_note()


def open_midi_port_blocking(event: Event):
    ports = []
    instruments = mido.get_input_names()
    logger.debug("Detected the following MIDI instruments:")
    for index, instrument in enumerate(instruments):
        logger.debug("#{}: {}".format(index, instrument))
        ports.append(mido.open_input(instrument))

    port = MultiPort(ports)

    while True:
        for msg in port.iter_pending():
            received_message(msg)
        if event.is_set():
            break
        time.sleep(0.0001)


def open_midi_ports():
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, open_midi_port_blocking, event)


def close_midi_ports():
    event.set()
