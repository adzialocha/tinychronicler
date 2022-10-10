import asyncio
from threading import Event
import time

import mido
from mido.ports import MultiPort
from mido.messages import Message
from loguru import logger

from .osc import send_midi_note

# Signal to tell MIDI process to shut down
event = Event()


def received_message(message: Message):
    if message.type == 'note_on':
        send_midi_note(message.channel, message.note, message.velocity, True)
    elif message.type == 'note_off':
        send_midi_note(message.channel, message.note, message.velocity, False)


def open_midi_port_blocking(event: Event):
    ports = []
    port_names = []
    instruments = mido.get_input_names()
    logger.debug("Detected the following MIDI instruments:")
    for index, instrument in enumerate(instruments):
        logger.debug("#{}: {}".format(index, instrument))
        if instrument not in port_names:
            ports.append(mido.open_input(instrument))
            port_names.append(instrument)

    # Listen to all ports at the same time so we don't need to worry about
    # selecting instruments
    port = MultiPort(ports)

    while True:
        for msg in port.iter_pending():
            received_message(msg)

        # Shut down when signal was received
        if event.is_set():
            break

        time.sleep(0.0001)


def open_midi_ports():
    # Start (blocking) MIDI process in separate thread
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, open_midi_port_blocking, event)


def close_midi_ports():
    # Fire signal to tell MIDI process to shut down
    event.set()
