#!/usr/bin/env python3

"""
Displays information about a plant in your garden(efficiently).
Class day
"""


class Plant:
    """ Serves as a blueprint for any plant. """
    def __init__(
            self,
            name: str,
            starting_height: float,
            starting_age: int
            ) -> None:
        """ Every plant might have a name, height, and age """
        self.name = name
        self.starting_height = starting_height
        self.starting_age = starting_age
        self.height = starting_height

    def grow(self) -> None:
        """ Grow by +1cm each day """
        self.height += 1

    def age(self) -> None:
        """ age of plant day by +1day """
        self.starting_age += 1

    def get_info(self) -> None:
        """ Display the current plant status """
        print(self.print_plant())
        if (self.height > self.starting_height):
            print(f"Growth this week: +{self.height - self.starting_height}cm")

    def print_plant(self) -> str:
        """ Print the plant with their infos """
        if (self.starting_age == 1):
            day = "day"
        else:
            day = "days"
        return (f"{self.name} {self.height}cm, {self.starting_age} {day} old")


def main():
    """
    A program that runs when executed directly
    $>python ft_*.py
    """
    print("=== Day 1 ===")
    rose = Plant("Rose", 25, 30)
    rose.get_info()
    for day in range(2, 8):
        rose.age()
        rose.grow()
    print("=== Day 7 ===")
    rose.get_info()


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main()
