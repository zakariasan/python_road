#!/usr/bin/env python3

"""
File has Write a function named ft_water_reminder
"""


def ft_water_reminder():
    """
    function hat asks for the number of days since last
    watering.
    """
    water = int(input("Days since last watering: "))
    if water > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")
