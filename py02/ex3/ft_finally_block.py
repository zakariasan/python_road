#!/usr/bin/env python3

"""
Create custom plant alerts, and keep your digital
greenhouse thriving even when things go wrong.
"""


def water_plants(plant_list: list) -> None:
    """
    Sometimes your garden program needs to clean up after itself,
    even if an error happens
    """

    print("Opening watering system")
    try:
        for plant in plant_list:
            if plant is None:
                raise ValueError("Cannot water None - invalid plant!")
            print(f"Watering {plant}")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        print("Closing watering system (cleanup)")


def test_watering_system():
    """ Let;s test Our watering plants"""
    plants = [
            "tomato",
            "lettuce",
            "carrots"
            ]
    print("=== Garden Watering System ===")
    print("\nTesting normal watering...")
    try:
        water_plants(plants)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print()

    plants_2 = [
            "tomato",
            None,
            "lettuce",
            "carrots"
            ]
    print("Testing normal watering...")
    try:
        water_plants(plants_2)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("\nWatering completed successfully!")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    test_watering_system()
