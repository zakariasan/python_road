#!/usr/bin/env python3

"""
File has Write a function for iterative object
"""


def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    """
    count from 1 to a given number, printing each day until harvest
    time.
    """
    seed = seed_type.capitalize()
    if unit == "packets":
        print(f"{seed} seeds: {quantity} packets available")
    elif unit == "grams":
        print(f"{seed} seeds: {quantity} grams total")
    elif unit == "area":
        print(f"{seed} seeds: covers {quantity} square meters")
    else:
        print("Unknown unit type")
