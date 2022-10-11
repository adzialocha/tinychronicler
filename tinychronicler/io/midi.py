import mido
from mido.ports import MultiPort
from mido.messages import Message
from loguru import logger

from .osc import send_midi_note


def received_message(message: Message):
    if message.type == 'note_on':
        send_midi_note(message.channel, message.note, message.velocity, True)
    elif message.type == 'note_off':
        send_midi_note(message.channel, message.note, message.velocity, False)


# Listen to all ports at the same time so we don't need to worry about
# selecting instruments
ports = []
port_names = []
instruments = mido.get_input_names()
logger.debug("Detected the following MIDI instruments:")
for index, instrument in enumerate(instruments):
    logger.debug("#{}: {}".format(index, instrument))
    if instrument not in port_names:
        ports.append(mido.open_input(
            instrument, callback=received_message))
        port_names.append(instrument)
port = MultiPort(ports)


def open_midi_ports():
    pass


def close_midi_ports():
    pass
