#!/usr/bin/env python3

"""
Create custom plant alerts, and keep your digital
greenhouse thriving even when things go wrong.
"""


def check_plant_health(plant_name, water_level, sunlight_hours):
    """Check plant helth

    Return : message if everything is okay
    """
    try:
        if plant_name == "":
            raise ValueError("Plant name cannot be empty!")
        elif water_level < 0:
            raise ValueError(
                    f"Water level {water_level} is too low (min 1)"
                    )
        elif water_level > 11:
            raise ValueError(
                    f"Water level {water_level} is too high (max 10)"
                    )
        elif sunlight_hours <= 1:
            raise ValueError(
                f"Sunlight hours {water_level} is too low (min 2)"
                )
        elif water_level > 13:
            raise ValueError(
                f"Sunlight hours {water_level} is too high (max 12)"
                )
        else:
            print(f"Plant '{plant_name}' is healthy!")
    except Exception as e:
        print(f"Error: {e}")


def test_plant_checks():
    """ check the plant helth with values"""

    print("=== Garden Plant Health Checker ===")
    print("\nTesting good values...")
    check_plant_health("tomato", 5, 5)

    print("\nTesting empty plant name...")
    check_plant_health("", 5, 5)

    print("\nTesting bad water level...")
    check_plant_health("tomato", 15, 5)

    print("\nTesting bad sunlight hours...")
    check_plant_health("tomato", 5, 2)

    print("\nAll error raising tests completed!")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    test_plant_checks()
