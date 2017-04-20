#! /usr/bin/env python3.6
from time import sleep
from os import spawnlp, P_WAIT

HEADPHONES = "Stereo Headphones FP"
SPEAKERS = "Stereo Headphones"
OXYGEN_FILE = "/proc/asound/DG/oxygen"
JACK_STATUS_LOCATION = 551
OUTPUT_DEVICE = "Analog Output"
    
def set_active(output):
    spawnlp(P_WAIT, 'amixer', 'amixer', 'set', OUTPUT_DEVICE, output)

def headphones_state(oxygen_file):
    # Python seems to cache the file if we seek directly to
    # the location we want to read
    oxygen_file.seek(0)

    # The oxygen file contains a list of hex codes representing the
    # state of the sound card. The single hex digit (half byte) located
    # at position 551 contains the state of the headphone jack.
    oxygen_file.seek(JACK_STATUS_LOCATION)
    byte = int(oxygen_file.read(1), 16)

    # The least significant bit (rightmost bit) represents whether 
    # or not headphones are plugged in to the jack. 
    # (0 for plugged in, 1 for unplugged)
    # The most significant bit (leftmost bit) represents whether
    # the headphone jack is active. (0 for active, 1 for inactive)
    return (not (byte & 0b1), not (byte >> 3 & 0b1))

def main():
    with open(OXYGEN_FILE, "rb") as f:
        while True:
            plugged_in, active = headphones_state(f)
            if plugged_in and not active:
                set_active(HEADPHONES)
            elif active and not plugged_in:
                set_active(SPEAKERS)
            sleep(1)

if __name__ == "__main__":
    main()
