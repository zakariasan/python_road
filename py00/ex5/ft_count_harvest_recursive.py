#!/usr/bin/env python3

"""
Count days recursively until harvest time.
"""


def ft_print_days_recursive(n):
    """
    function helper to make the recursion easy
    """
    if (n == 0):
        return
    ft_print_days_recursice(n - 1)
    print(f"Day {n}")


def ft_count_harvest_recursive():
    """
    function hat asks for the number of days since last
    watering.
    """
    day = int(input("Days until harvest: "))
    if day >= 1:
        ft_print_days_recursive(day)
        print("Harvest time!")
