from typing import List, Union

from loguru import logger
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import UDPClient

from tinychronicler.server.ws import ws_manager

UDP_HOST = "127.0.0.1"
UDP_PORT = 51230

client = UDPClient(UDP_HOST, UDP_PORT)


def send_message(
    address: str,
    *args: List[Union[str, bytes, bool, int, float, tuple, list]]
):
    # Create OSC message
    builder = OscMessageBuilder(address=address)
    for arg in args:
        builder.add_arg(arg)
    message = builder.build()
    logger.debug("Send OSC message: {} {}".format(address, args))

    # Send via WebSocket
    ws_manager.broadcast(message.dgram)

    # Send via UDP
    client.send(message)
