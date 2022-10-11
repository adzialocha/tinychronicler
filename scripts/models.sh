#!/bin/bash
# Download all speech recognition models into the right folder

MODELS_DIR="models"
MODELS_URL="https://alphacephei.com/vosk/models"

models=(
    "vosk-model-small-cn-0.22.zip"
    "vosk-model-small-de-0.15.zip"
    "vosk-model-small-en-us-0.15.zip"
    "vosk-model-small-es-0.42.zip"
    "vosk-model-small-fr-0.22.zip"
    "vosk-model-small-it-0.22.zip"
    "vosk-model-small-ja-0.22.zip"
    "vosk-model-small-pl-0.22.zip"
    "vosk-model-small-ru-0.22.zip"
)

for i in "${models[@]}"
do
    wget -O tmp.zip "$MODELS_URL/$i"
    unzip tmp.zip -d $MODELS_DIR
    rm tmp.zip
done
