#!/usr/bin/env python3

"""
Displays information about a plant in your garden(efficiently).
Class day
"""


class GardenManager:
    """
    Serves as a blueprint for any plant GardenManager,
    """
    def __init__(self, name: str) -> None:
        """
        Every plant might have a name, height, and age
        """
        self.name = name

    @classmethod
    def create_garden_network(cls):
        pass

class GardenStats(GardenManager):
    """
    Helper to calculat and manage statistics
    """
    def __init__(self, name: str) -> None:
        """
        Every plant might have a name, height, and age
        """
        super().__init__(self, name)

    @staticmethod
    def calc_manager():
        pass

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


class FloweringPlant(Plant):
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

class PrizeFlower(FloweringPlant):
    pass

# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main()
