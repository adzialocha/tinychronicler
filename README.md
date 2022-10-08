# Tiny Chronicler `@( * O * )@`

Tiny Chronicler is a travelling music robot. It runs on a RaspberryPi computer equipped with an web interface to upload images, audio recordings and video files to generate intermedial musical compositions based on the uploaded material. Every composition can be printed as a score with a small thermal printer. The pieces are performed live with MIDI instruments and the Tiny Chronicler together who shows videos, makes sounds, shines with LED lights and sings.

## Hardware

- Raspberry Pi 4 Model B w. HDMI output
- Sound card for Raspberry Pi ([HifiBerry DAC2 Pro](https://www.hifiberry.com/shop/boards/hifiberry-dac2-pro/))
- 32x32 Pixel LED matrix ([Adafruit](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/))
- Arduino MEGA 2560 to run LED matrix
- Thermal printer ([Sparkfun](https://www.sparkfun.com/products/14970))
- USB MIDI keyboard
- USB MIDI drum pad

## Requirements

- Python 3.8.11
- [Poetry](https://python-poetry.org)
- PureData

## Setup

1. Assemble all parts following the steps in [`HARDWARE.md`](HARDWARE.md).
2. Follow the steps in [`SETUP.md`](SETUP.md) to install Tiny Chronicler and all other required services on your Raspberry Pi.
3. The Pi will create a WiFi network named `tinychronicler`. You can access it with the password `tinychronicler`.
4. Start a browser and open the [web interface](tinychronicler/web) of Tiny Chronicler by entering the URL `http://tinychronicler.local`.

## Development

```bash
# Install dependencies
poetry install

# Run application in virtual environment, open browser at localhost:8000
poetry run python tinychronicler

# Run Jupyter Lab to experiment with code in `/notebooks` folder
poetry run jupyter lab ./notebooks

# Start shell to allow running any other application in virtual environment
poetry shell

# Check linters
isort .
flake8
```

## License

[`MIT`](LICENSE)
