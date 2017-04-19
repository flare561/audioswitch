#! /usr/bin/env python3.6
from time import sleep
from os import system

HEADPHONES = "'Stereo Headphones FP'"
SPEAKERS = "'Stereo Headphones'"

    
def set_active(output):
    system(f"amixer set 'Analog Output' {output}")

def headphones_state(oxygen_file):
    # Python seems to cache the file if we seek directly to
    # the location we want to read
    oxygen_file.seek(0)

    # The oxygen file contains a list of hex codes representing the
    # state of the sound card. The single hex digit located at position
    # 551 contains the state of the headphone jack.
    oxygen_file.seek(551)
    byte = int(oxygen_file.read(1), 16)

    # The first bit (from left to right) represents whether the headphone
    # jack is active (0 for active, 1 for inactive), while the last bit
    # represents whether something is plugged in to the headphone jack.
    # (0 for plugged in, 1 for unplugged)
    return (not (byte & 0b1), not (byte >> 3 & 0b1))

def main():
    with open("/proc/asound/DG/oxygen", "rb") as f:
        while True:
            plugged_in, active = headphones_state(f)
            if plugged_in and not active:
                set_active(HEADPHONES)
            elif active and not plugged_in:
                set_active(SPEAKERS)
            sleep(1)

if __name__ == "__main__":
    main()
