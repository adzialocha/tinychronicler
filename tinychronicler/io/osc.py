from typing import List, Union

from pythonosc.osc_message_builder import OscMessageBuilder

from tinychronicler.server.ws import ws_manager


def send_message(
    address: str,
    *args: List[Union[str, bytes, bool, int, float, tuple, list]]
):
    builder = OscMessageBuilder(address=address)
    for arg in args:
        builder.add_arg(arg)
    message = builder.build()
    ws_manager.broadcast(message.dgram)
