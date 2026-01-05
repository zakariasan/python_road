#!/usr/bin/env python3

"""
Displays information about a plant in your garden(efficiently).
Class day
"""


class Plant:
    """
    Serves as a blueprint for any plant,
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
        return (
                f"{self.name} {self.height}cm, {self.age} {day}"
                + " old")


class Flower(Plant):
    """
    Serves as a blueprint for any plant (Flower),
    """
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            color: str
            ) -> None:
        """
        Every plant might have a name, height, and age also a color
        """
        super().__init__(name, height, age)
        self.color = color

    def bloom(self) -> None:
        print(f"{self.name} is blooming beautifully!")

    def print_plant(self) -> None:
        """
        Print the plant with their infos
        """
        if (self.age == 1):
            day = "day"
        else:
            day = "days"
        print(f"{self.name} (Flower): ",end="")
        print(f"{self.height}cm, {self.age} {day}, ",end="")
        print(f"{self.color} color")

class Tree(Plant):
    """
    Serves as a blueprint for any plant (Flower),
    """
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            trunk_diameter: float
            ) -> None:
        """
        Every plant might have a name, height, and age also a color
        """
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
        """
        the shade from the tree how was it
        let's calculate it.
        """
        shade: int = int((self.height * self.height * 3.14) / 10000)
        print(f"{self.name} provides {shade}", end="")
        print(" square meters of shade")

    def print_plant(self) -> str:
        """
        Print the plant with their infos
        """
        if (self.age == 1):
            day = "day"
        else:
            day = "days"
        print(f"{self.name} (Flower): ",end="")
        print(f"{self.height}cm, {self.age} {day}, ",end="")
        print(f"{self.trunk_diameter} diameter")


class Vegetable(Plant):
    """
    Serves as a blueprint for any plant (Vegetable),
    """
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            harvest_season: str,
            nutritional_value: str,
            ) -> None:
        """
        Every plant might have a name, height, and age also a color
        """
        super().__init__(name, height, age)
        self.nutritional_value = nutritional_value
        self.harvest_season = harvest_season

    def print_plant(self) -> str:
        """
        Print the plant with their infos
        """
        if (self.age == 1):
            day = "day"
        else:
            day = "days"
        print(f"{self.name} (Vegetable): ",end="")
        print(f"{self.height}cm, {self.age} {day}, ",end="")
        print(f"{self.harvest_season} harvest")
        print(f"{self.name} is rich in {self.nutritional_value}")


def main():
    """
    A program that runs when executed directly
    $>python ft_*.py
    """
    rose = Flower("Rose", 25, 30, "red")
    oak = Tree("Oak", 500, 1825, 50)
    tomato = Vegetable("Tomato", 80, 90, "summer", "vitamin C")
    print("=== Garden Plant Types ===\n")
    
    rose.print_plant()
    rose.bloom()
    print("")
    oak.print_plant()
    oak.produce_shade()
    print()
    tomato.print_plant()
# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main()
