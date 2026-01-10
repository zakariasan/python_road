#!/usr/bin/env python3

"""
Displays information about a plant in your garden(efficiently).
Class day
"""


class Plant:
    """Serves as a blueprint for any plant."""
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

    def print_plant(self) -> str:
        """ Print the plant with their infos """
        if (self.starting_age == 1):
            day = "day"
        else:
            day = "days"
        return (
                f"{self.name} ({self.__class__.__name__})"
                +
                f" {self.starting_height}cm, {self.starting_age} {day}"
                )


class Flower(Plant):
    """ Serves as a blueprint for any plant (Flower). """
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            color: str
            ) -> None:
        """ Every plant might have a name, height, and age also a color"""
        super().__init__(name, height, age)
        self.color = color

    def bloom(self) -> None:
        """ Check if the Flower is blooming """
        print(f"{self.name} is blooming beautifully!")

    def print_plant(self) -> str:
        """ Print the plant with their infos """
        plant = super().print_plant()
        return (f"{plant}, {self.color} color")


class Tree(Plant):
    """ Serves as a blueprint for any plant (Tree)"""
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            trunk_diameter: float
            ) -> None:
        """ Every plant might have a name, height, and age also a color"""
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
        """
        the shade from the tree how was it
        let's calculate it.
        """
        shade: int = int(
                (self.starting_height * self.starting_height * 3.14)
                / 10000)
        print(f"{self.name} provides {shade}", end="")
        print(" square meters of shade")

    def print_plant(self) -> str:
        """ Print the plant with their infos """
        plant: str = super().print_plant()
        return (f"{plant}, {self.trunk_diameter} diameter")


class Vegetable(Plant):
    """ Serves as a blueprint for any plant (Vegetable)"""
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            harvest_season: str,
            nutritional_value: str,
            ) -> None:
        """ Every plant might have a name, height, and age and harvest"""
        super().__init__(name, height, age)
        self.nutritional_value = nutritional_value
        self.harvest_season = harvest_season

    def print_plant(self) -> str:
        """ Print the plant with their infos """
        plant: str = super().print_plant()
        return (
                f"{plant}, {self.harvest_season} harvest"
                +
                f"{self.name} is rich in {self.nutritional_value}"
                )


def main():
    """
    A program that runs when executed directly
    $>python ft_*.py
    """
    print("=== Garden Plant Types ===\n")
    rose = Flower("Rose", 25, 30, "red")
    oak = Tree("Oak", 500, 1825, 50)
    tomato = Vegetable("Tomato", 80, 90, "summer", "vitamin C")
    print(rose.print_plant())
    rose.bloom()
    print()
    print(oak.print_plant())
    oak.produce_shade()
    print()
    print(tomato.print_plant())


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main()
