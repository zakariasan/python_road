#!/usr/bin/env python3

"""
Create custom plant alerts, and keep your digital
greenhouse thriving even when things go wrong.
"""


def check_temperature(temp_str: str) -> None:
    """ Check the temperature

    Return : the Temperature
    """
    try:
        temp_int = int(temp_str)
    except Exception:
        print(f"Error: {temp_str} is not a valid number")
        return

    if (temp_int > 40):
        print(f"Error: {temp_int}°C is too hot for plants (max 40°C)")
    elif temp_int < 0:
        print(f"Error: {temp_int}°C is too cold for plants (min 0°C)")
    else:
        print(f"Temperature {temp_int}°C is perfect for plants!")


def test_temperature_input():
    """ Test my check temperature"""
    inputs: str = [
            "25",
            "abc",
            "100",
            "-50",
            ]
    print("=== Garden Temperature Checker ===")
    for inp in inputs:
        print(f"\nTesting temperature: {inp}")
        check_temperature(inp)

    print("\nAll tests completed - program didn't crash!")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    test_temperature_input()
