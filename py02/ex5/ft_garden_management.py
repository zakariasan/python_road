#!/usr/bin/env python3

"""
Create custom plant alerts, and keep your digital
greenhouse thriving even when things go wrong.
"""


class Plant:
    """The Mother for all plants in the garden."""
    def __init__(
            self,
            name: str,
            water_level: float,
            sun_light: float
            ) -> None:
        """Every plant might have a name, height."""
        self.name = name
        self.water_level = water_level
        self.sun_light = sun_light


class GardenManager:
    """Serves as a blueprint for any GardenManager."""

    def __init__(self) -> None:
        """ Each garden has plants now """
        self.plants = []
        self.size = 0
        self.tank = 90

    def water_plants(self) -> None:
        """ Add Plant while checking if it Good or Not"""
        print("Watering plants...")
        print("Opening watering system")
        try:
            if (self.tank < 50):
                raise Exception("Not enough water in tank")
            for plant in self.plants:
                print(f"Watering {plant.name} - success")
        finally:
            print("Closing watering system (cleanup)")

    def check_all_plants(self):
        """ checking all plants """
        print("Checking plant health...")
        for plant in self.plants:
            self.check_plant_health(
                    plant.name,
                    plant.water_level,
                    plant.sun_light)

    def check_plant_health(self, plant_name, water_level, sunlight_hours):
        """Check plant helth

        Return : message if everything is okay
        """
        try:
            if plant_name == "":
                raise ValueError("Plant name cannot be empty!")
            elif water_level < 0:
                raise ValueError(
                        f"Water level {water_level} is too low (min 1)"
                        )
            elif water_level > 11:
                raise ValueError(
                        f"Water level {water_level} is too high (max 10)")
            elif sunlight_hours <= 1:
                raise ValueError(
                    f"Sunlight hours {water_level} is too low (min 2)")
            elif water_level > 13:
                raise ValueError(
                        f"Sunlight hours {water_level} is too high (max 12)")
            else:
                print(
                        f"{plant_name}"
                        +
                        f"(water: {water_level}, sun {sunlight_hours})")
        except Exception as e:
            print(f"Error: {e}")

    def add_plants(self, plants: Plant) -> None:
        """ Watering Plants for the future """
        try:
            print("Adding plants to garden...")
            for plant in plants:
                if plant is None or plant.name is None:
                    raise Exception("Plant name cannot be empty!")
                print(f"Added {plant.name} successfully")
                self.plants.append(plant)
                self.size += 1
        except Exception as e:
            print(f"Error Adding plant: {e}")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    print("=== Garden Management System ===\n")
    plants = [
            Plant("tomato", 5, 8),
            Plant("lettuce", 15, 8),
            None,
            ]
    manager = GardenManager()
    manager.add_plants(plants)
    print()
    manager.water_plants()
    print()
    manager.check_all_plants()
    print("\nGarden management system test complete!")
