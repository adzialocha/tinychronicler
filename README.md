# Tiny Chronicler `@( * O * )@`

Tiny Chronicler is a travelling music robot. It runs on a RaspberryPi computer equipped with an web interface to upload images, audio recordings and video files to generate intermedial musical compositions based on the uploaded material. Every composition can be printed as a score with a small thermal printer. The pieces are performed live with MIDI instruments and the Tiny Chronicler together who shows videos, makes sounds, shines with LED lights and sings.

## Hardware

- Raspberry Pi 4 Model B w. HDMI output
- Sound card (HifiBerry)
- 16x16 LED matrix
- Thermal printer
- USB MIDI keyboard
- USB MIDI drum pad

## Requirements

- Python 3.8
- [Poetry](https://python-poetry.org)
- PureData

## Development

```bash
# Install dependencies
poetry install

# Run application in virtual environment, open browser at localhost:8000
poetry run python tinychronicler
```

## License

`MIT`
