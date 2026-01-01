#!/usr/bin/env python3

"""
File has Write a function named ft_plant_age
"""


def ft_plant_age():
    """
    function hat asks for a plant’s age in days
    """
    age = int(input("Enter plant age in days: "))
    if age >= 60:
        print("Plant is ready to harvest!")
    else:
        print("Plant needs more time to grow.")
