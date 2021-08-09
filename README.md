# tinychronicler

Tiny Chronicler is a travelling music robot built with RaspberryPi equipped with an web interface to upload images, audio recordings and video files to generate intermedial musical compositions out of the uploaded material. Every composition can be printed as a score with a small thermal printer and then performed live with Tiny Chronicler together who shows videos, makes sounds, shines with LED lights and sings.

## Hardware

- Raspberry Pi 4 Model B w. HDMI output
- Sound card (HifiBerry)
- 16x16 LED matrix
- Thermal printer

## Requirements

- Python 3.9
- [Poetry](https://python-poetry.org)
- PureData

## Development

```bash
# Install dependencies
poetry install

# Run application, open browser at localhost:8000
poetry run python tinychronicler
```

## License

`MIT`
