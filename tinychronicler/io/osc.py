from typing import List, Union

from pythonosc.osc_message_builder import OscMessageBuilder

from tinychronicler.server.ws import WebSocketConnectionManager


def send_message(
    address: str,
    *args: List[Union[str, bytes, bool, int, float, tuple, list]]
):
    builder = OscMessageBuilder(address=address)
    for arg in args:
        builder.add_arg(arg)
    message = builder.build()

    # Send message to websocket clients
    ws_manager = WebSocketConnectionManager()
    ws_manager.add_to_queue(message.dgram)


def send_midi_note():
    send_message("/instrument/1/note")
