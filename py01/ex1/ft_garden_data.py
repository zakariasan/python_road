#!/usr/bin/env python3

"""
Displays information about a plant in your garden(efficiently).
Class day
"""


class Plant:
    """
    Serves as a blueprint for any plant,
    rather than handling each one individually.
    """
    def __init__(self, name: str, height: float, age: int) -> None:
        """
        Every plant might have a name, height, and age
        """
        self.name = name
        self.height = height
        self.age = age

    def print_plant(self) -> str:
        """
        Print the plant with their infos
        """
        if (self.age == 1):
            day = "day"
        else:
            day = "days"
        return (f"{self.name} {self.height}cm, {self.age} {day} old")


def main():
    """
    A program that runs when executed directly
    Display the plant information using print()
    """
    rose = Plant("Rose", 25, 30)
    sun = Plant("Sunflower", 80, 45)
    cac = Plant("Cactus", 15, 120)
    print("=== Garden Plant Registry ===")
    print(rose.print_plant())
    print(sun.print_plant())
    print(cac.print_plant())


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main()
