#!/usr/bin/env python3

"""
Displays information about a plant in your garden(efficiently).
Class day

"""


class Plant:
    """
    Serves as a blueprint for any plant,
    """
    def __init__(self, name: str, height: float) -> None:
        """
        Every plant might have a name, height, and age
        """
        self.name = name
        self.height = height

    def grow(self) -> None:
        """
        Plant can grow by 1cm per day
        """
        self.height += 1
        print(f"{self.name} grew 1cm")

    def print_plant(self) -> str:
        """
        Print the plant with their infos
        """
        return (f"{self.name} {self.height}cm")


class FloweringPlant(Plant):
    """
    Serves as a blueprint for any plant (Flower),
    """
    def __init__(
            self,
            name: str,
            height: float,
            color: str
            ) -> None:
        """
        Every plant(Flower) might have a name, height
        and age also a color
        """
        super().__init__(name, height)
        self.color = color
        self.blooming = True

    def bloom(self) -> str:
        if (self.blooming):
            return ("blooming")
        return ("not blooming")

    def print_plant(self) -> str:
        """
        Print the plant with their infos
        """
        get_info = super().print_plant()
        return f"{get_info}, {self.color} flowers ({self.bloom()})"


class PrizeFlower(FloweringPlant):
    """
    Serves as a blueprint for any prize flower (Flower),
    """
    def __init__(
            self,
            name: str,
            height: float,
            color: str,
            pts: int
            ) -> None:
        """
        Every plant(Flower) might have a name, height
        and age also a color and points
        """
        super().__init__(name, height, color)
        self.pts = pts

    def print_plant(self) -> str:
        """
        Print the plant with their infos(prize)
        """
        get_info = super().print_plant()
        return f"{get_info}, Prize points: {self.pts}"


class Garden:
    """
    Serves as a blueprint for any Garden.
    """
    def __init__(self, name: str) -> None:
        """
        Init the Garden Owner and his worth
        """
        self.name = name
        self.plants = []

    def add_plant(self, plant: Plant) -> None:
        self.plants.append(plant)
        print(f"Added {plant.name} to {self.name}'s garden")

    def grow_all(self) -> None:
        if self.plants == []:
            print(f"{self.name} has no plants")
        else:
            print(f"{self.name} is helping all plants grow...")
            for plant in self.plants:
                plant.grow()

    def report(self) -> None:
        print(f"=== {self.name}'s Garden Report ===")
        for plant in self.plants:
            print(f"- {plant.print_plant()}")


class GardenManager:
    """
    Serves as a blueprint for any GardenManager,
    """
    gardens = {}

    class GardenStats:
        """
        Helper to calculat and manage statistics
        """
        @staticmethod
        def count_plants_types(plants: list) -> list:
            """
            Counts all types of plants
            > [regular plants, fowring plants, prize plants]
            """
            regular = 0
            flowring = 0
            prize = 0
            for plant in plants:
                if isinstance(plant, FloweringPlant):
                    flowring += 1
                elif isinstance(plant, PrizeFlower):
                    prize += 1
                else:
                    regular += 1
            return [regular, flowring, prize]

        @staticmethod
        def total_growth(plants: list) -> int:
            """
            Calculat the total growth of all plants
            """
            cnt = 0
            for plant in plants:
                cnt += plant.height
            return cnt

        @staticmethod
        def total_plants(plants: list) -> int:
            """
            Calculat the total plants
            """
            return (len(plants))

    def add_garden(self, garden: Garden) -> None:
        self.gardens[garden.name] = garden

    def analyse(self, name: str) -> None:
        garden = self.gardens[name]
        status = self.gardenStats
        values = status.count_plants_types(garden.plants)
        growth = status.total_growth(garden.plants)

        print(
                f"Plants added: {len(garden.plants)}, "
                f"Total growth: {growth}cm "
                )
        print(
                f"Plants types: {values[0]} regular, "
                f"{values[1]}flowering, {values[2]} prize"
                )

    @classmethod
    def create_garden_network(cls) -> None:
        print(f"Total gardens managed: {len(cls.gardens)}")


def main():
    print("=== Garden Management System Demo ===    ")
    alice = Garden("Alice")
    manager = GardenManager()
    manager.add_garden(alice)
    plants = [
            Plant("Oak Tree", 101),
            FloweringPlant("Rose", 26, "red"),
            PrizeFlower("Sunflower", 51, "yellow", 10)
            ]
    for plant in plants:
        alice.add_plant(plant)
    print()
    alice.grow_all()
    print()
    alice.report()
    print()
    print(manager.analyse(alice.name))


# This line means: "If someone runs this file directly, call main()"


if __name__ == "__main__":
    main()
