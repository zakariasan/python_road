#!/usr/bin/env python3

"""
Displays information about a plant in your garden(efficiently).
Class day
"""


class SecurePlant:
    """
    Serves as a blueprint for any plant,
    and Protect and ecapsulates sensitive data
    """
    def __init__(
            self,
            name: str,
            height: float,
            age: int
            ) -> None:
        """
        Every plant might have a name, height, and age
        """
        self.name = name
        self.__height = 0
        self.__age = 0

        self.set_height(height)
        self.set_age(age)

    def get_height(self) -> float:
        """
        right acces to get height
        """
        return self.__height

    def get_age(self) -> int:
        """
        Good way to get the age
        """
        return self.__age

    def set_height(self, value: float) -> None:
        """
        Let set the height in secure way
        """
        if (value >= 0):
            print(f"Height updated: {value}cm [OK]")
            self.__height = value
        else:
            print(f"Invalid operation attempted: height {value}cm [REJECTED]")
            print("Security: Negative height rejected")

    def set_age(self, value: int) -> None:
        if (value >= 0):
            print(f"Age updated: {value}days [OK]")
            self.__age = value
        else:
            print(f"Invalid operation attempted: age {value}days [REJECTED]")
            print("Security: Negative age rejected")

    def print_plant(self) -> str:
        """
        Print the plant with their infos
        """
        if (self.__age == 1):
            day = "day"
        else:
            day = "days"
        return (f"{self.name} ({self.__height}cm, {self.__age} {day})")


def main():
    """
    A program that runs when executed directly
    $>python ft_*.py
    """
    rose = SecurePlant("Rose", 5, 40)
    print("=== Garden Security System ===")
    print(f"Plant created: {rose.name}")
    rose.set_height(25)
    rose.set_age(30)
    print("")
    rose.set_height(-5)
    print("")
    print(f"Current plant: {rose.print_plant()}")

# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    main()
