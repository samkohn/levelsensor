#!/bin/sh

echo "Setting environment variables..."

export ARDUINO_DIR="/Users/pmadigan/research/levelsensor/arduino/arduino/build/macosx/work/Arduino.app/Contents/Java"
echo "ARDUINO_DIR = $ARDUINO_DIR"
export ARDMK_DIR="/Users/pmadigan/research/levelsensor/arduino/arduino-mk"
echo "ARDMK_DIR = $ARDMK_DIR"
export AVR_TOOLS_DIR="/opt/local/"
echo "AVR_TOOLS_DIR = $AVR_TOOLS_DIR"
export MONITOR_PORT="/dev/cu.usbmodem1411"
echo "MONITOR_PORT = $MONITOR_PORT"
export BOARD_TAG="uno"
echo "BOARD_TAG = $BOARD_TAG"
export LS_DIR="/Users/pmadigan/research/levelsensor/arduino/projs/levelsensor"
echo "LS_DIR = $LS_DIR"

echo "Done!"
echo ""

alias levelsensor="python -i $LS_DIR/control.py"

echo "Type 'levelsensor' to begin"
