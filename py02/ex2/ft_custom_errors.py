#!/usr/bin/env python3

"""
Create custom plant alerts, and keep your digital
greenhouse thriving even when things go wrong.
"""


class GardenError(Exception):
    """A Basic Error for garden problems"""
    pass


class PlantError(GardenError):
    """For problems with plants"""

    def __init__(self, name, status="wilting") -> None:
        self.name = name
        self.status = status
        self.msg = f"The {self.name} plant is {self.status}!"

    def print_error(self):
        return self.msg


class WaterError(GardenError):
    """For problems with watering"""
    def __init__(self, level):
        self.msg = "Not enough water in the tank!"

    def print_error(self):
        return self.msg


def check_plant(plant_name: str, status: str):
    """ checking if the plant is healthy """
    if status == 'wilting':
        raise PlantError(plant_name, status)


def check_water(level: float) -> None:
    """ Check water level"""
    if level < 50:
        raise WaterError(level)


def test_funcs():
    """ test all functionalities in this project """

    print("=== Custom Garden Errors Demo ===")
    print("\nTesting PlantError...")
    try:
        check_plant("tomato", "wilting")
    except PlantError as e:
        print(f"Caught PlantError: {e.msg}")

    print("\nTesting WaterError...")
    try:
        check_water(20)
    except WaterError as e:
        print(f"Caught WaterError: {e.msg}")

    print("\nTesting catching all garden errors...")
    try:
        check_plant("tomato", "wilting")
    except GardenError as e:
        print(f"Caught PlantError: {e.msg}")

    try:
        check_water(37)
    except GardenError as e:
        print(f"Caught WaterError: {e.msg}")

    print("\nAll custom error types work correctly!")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    test_funcs()
