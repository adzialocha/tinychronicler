from pythonosc.udp_client import SimpleUDPClient

OSC_ENDPOINT = "127.0.0.1"
OSC_PORT = 5005

client = SimpleUDPClient(address=OSC_ENDPOINT, port=OSC_PORT)


def send_message():
    # @TODO
    client.send_message("/test")
