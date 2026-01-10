#!/usr/bin/env python3

"""
Displays information about a plant in your garden(efficiently).
$> Class day
"""


class Plant:
    """The Mother for all plants in the garden."""
    def __init__(self, name: str, height: float) -> None:
        """Every plant might have a name, height."""
        self.name = name
        self.height = height
        self.growth = height

    def grow(self) -> None:
        """ Plant can grow by 1cm per day """
        self.height += 1
        print(f"{self.name} grew 1cm")

    def get_total_growth(self) -> float:
        """Calculate how much the plant has grown """
        return self.height - self.growth

    def print_plant(self) -> str:
        """Print the plant with their infos """
        return (f"{self.name} {self.height}cm")


class FloweringPlant(Plant):
    """Serves as a Blueprint for plant (Flower),"""
    def __init__(
            self,
            name: str,
            height: float,
            color: str
            ) -> None:
        """ Every plant(Flower) might have a Plant attr,also a color """
        super().__init__(name, height)
        self.color = color
        self.blooming = True

    def bloom(self) -> str:
        """Return current bloom status"""
        if (self.blooming):
            return ("blooming")
        return ("not blooming")

    def print_plant(self) -> str:
        """ Print the plant with their infos add color and blooming"""
        get_info = super().print_plant()
        return f"{get_info}, {self.color} flowers ({self.bloom()})"


class PrizeFlower(FloweringPlant):
    """Serves as a blueprint for any prize flower (PrizeFlower),"""
    def __init__(
            self,
            name: str,
            height: float,
            color: str,
            pts: int
            ) -> None:
        """
        Every plant(PrizeFlower) might have a name, height
        and age also a color and points
        """
        super().__init__(name, height, color)
        self.pts = pts

    def print_plant(self) -> str:
        """ Print the plant with their infos(prize) """
        get_info = super().print_plant()
        return f"{get_info}, Prize points: {self.pts}"


class Garden:
    """ Serves as a blueprint for any Garden. """
    def __init__(self, name: str) -> None:
        """ Init the Garden Owner and his worth """
        self.name = name
        self.plants = []

    def add_plant(self, plant: Plant) -> None:
        """ add Plant to self Garden """
        self.plants.append(plant)

    def grow_all(self) -> None:
        if not self.plants:
            print(f"{self.name} has no plants")
        else:
            print(f"{self.name} is helping all plants grow...")
            for plant in self.plants:
                plant.grow()

    def report(self) -> None:
        """Formated report for the self owner"""
        print(f"=== {self.name}'s Garden Report ===")
        for plant in self.plants:
            print(f"- {plant.print_plant()}")


class GardenManager:
    """Serves as a blueprint for any GardenManager."""

    gardens = {}

    class GardenStats:
        """ Helper to calculat and manage statistics """

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
                if type(plant).__name__ == "PrizeFlower":
                    prize += 1
                elif type(plant).__name__ == "FloweringPlant":
                    flowring += 1
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
                cnt += plant.get_total_growth()
            return cnt

        @staticmethod
        def heights_validation(plants: list) -> bool:
            """Check if there is a height grow or not"""
            growth = GardenManager.GardenStats.total_growth(plants)
            return (growth > 0)

        @staticmethod
        def calculate_score(plants: list) -> int:
            """Calculate Garden Score based on:
            - Plant heights
            - prize points
            - bonus plants
            """
            if not plants:
                return 0

            score = 0
            for plant in plants:
                score += int(plant.height)
                if type(plant).__name__ == "PrizeFlower":
                    score += plant.pts
            score += GardenManager.GardenStats.total_plants(plants) * 10
            return score

        @staticmethod
        def total_plants(plants: list) -> int:
            """ Calculat the total plants """
            count = 0
            for _ in plants:
                count += 1
            return (count)

    def add_garden(self, garden: Garden) -> None:
        """ register a garden with the manager (instance method) """
        self.gardens[garden.name] = garden

    def analyse(self, name: str) -> None:
        """ A summary about the garden """
        garden = self.gardens[name]
        status = self.GardenStats
        values = status.count_plants_types(garden.plants)
        growth = status.total_growth(garden.plants)
        print(
                f"Plants added: {len(garden.plants)}, "
                f"Total growth: {growth}cm "
                )
        print(
                f"Plants types: {values[0]} regular, "
                f"{values[1]} flowering, {values[2]} prize flowers")

    @classmethod
    def create_garden_network(cls: list) -> None:
        """ display staticstics about all gardens """
        if not cls.gardens:
            print("No gardens in the network")
        count = 0
        print("Garden scores -", end="")
        size = 0
        for _ in cls.gardens:
            size += 1
        for name, garden in cls.gardens.items():
            count += 1
            score = cls.GardenStats.calculate_score(garden.plants)
            print(f" {name}: {score}", end="")
            if (count <= size - 1):
                print(",", end="")
        print(f"\nTotal gardens managed: {count}")


def main():
    print("=== Garden Management System Demo ===    ")
    alice = Garden("Alice")
    bob = Garden("Bob")
    manager = GardenManager()

    manager.add_garden(alice)
    manager.add_garden(bob)
    plants = [
            Plant("Oak Tree", 100),
            FloweringPlant("Rose", 25, "red"),
            PrizeFlower("Sunflower", 50, "yellow", 10)
            ]
    for plant in plants:
        alice.add_plant(plant)
        print(f"Added {plant.name} to {alice.name}'s garden")

    bob.add_plant(Plant("Cactus", 42))
    bob.add_plant(Plant("Fern", 30))
    print()
    alice.grow_all()
    print("")
    alice.report()
    print("")

    manager.analyse(alice.name)

    print("\nHeight validation test: ", end="")
    print(manager.GardenStats.heights_validation(alice.plants))

    manager.create_garden_network()

# This line means: "If someone runs this file directly, call main()"


if __name__ == "__main__":
    main()
