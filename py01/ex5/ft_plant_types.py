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
        return (f"{self.name} {self.height}cm, {self.age} {day} old")


class Flower(Plant):
    """
    Serves as a blueprint for any plant (Flower),
    """
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        """
        Every plant might have a name, height, and age also a color
        """
        super().__init__(name, height, age)
        self.color = color

    def bloom(self) -> None:
        print(f"{self.name} is blooming beautifully!")

    def print_plant(self) -> str:
        """
        Print the plant with their infos
        """
        if (self.age == 1):
            day = "day"
        else:
            day = "days"
        return (f"{self.name} (Flower): {self.height}cm, {self.age} {day}, {self.color} color")

class Tree(Plant):
    """
    Serves as a blueprint for any plant (Flower),
    """
    def __init__(self, name: str, height: float, age: int, trunk_diameter: float) -> None:
        """
        Every plant might have a name, height, and age also a color
        """
        super().__init__(name, height, age)
        self.color = color

    def produce_shade(self) -> None:
        print(f"{self.name} is blooming beautifully!")

    def print_plant(self) -> str:
        """
        Print the plant with their infos
        """
        if (self.age == 1):
            day = "day"
        else:
            day = "days"
        return (f"{self.name} (Flower): {self.height}cm, {self.age} {day}, {self.color} color")

def main():
    """
    A program that runs when executed directly
    $>python ft_*.py
    """
    rose = Flower("Rose", 25, 30, "red")
    print("=== Garden Plant Types ===")
    rose.print_plant()
    rose.bloom()
    print("")
    
# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main()
