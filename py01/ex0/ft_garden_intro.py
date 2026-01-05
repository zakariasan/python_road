#!/usr/bin/env python3

"""
Displays information about a plant in your garden.
"""


def main():
    """
    A program that runs when executed directly
    Store plant information in simple variables (name, height, age)
    Display the plant information using print()
    """
    name = "Rose"
    height = 25
    age = 30
    print("=== Welcome to My Garden ===")
    print(f"Plant: {name}")
    print(f"Height: {height}cm")
    print(f"Age: {age} days")
    print("\n=== End of Program ===")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main()
