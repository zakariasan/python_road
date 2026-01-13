#!/usr/bin/env python3

import sys
"""
Create custom plant alerts, and keep your digital
greenhouse thriving even when things go wrong.
"""


def main(av):
    """
    Build a simple command interpreter that shows you’ve mastered the art
    of receiving external data.
    """

    size = len(av)
    print("=== Command Quest ===")
    if (size == 1):
        print(f"No arguments provided!\nProgram name: {av[0]}")
    else:
        count = 1
        print(f"Program name: {av[0]}\nArguments received: {size - 1}")
        for arg in av:
            print(f"Argument {count}: {arg}")
            count += 1
    print(f"Total arguments: {len(av)}")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main(sys.argv)
