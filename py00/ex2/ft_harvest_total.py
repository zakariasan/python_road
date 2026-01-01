#!/usr/bin/env python3

"""
File where A gardener harvested vegetables on 3 different days
"""


def ft_harvest_total():
    """
    func asks for the weight of each harvest and calculates the total.
    """
    day1 = int(input("Day 1 harvest: "))
    day2 = int(input("Day 2 harvest: "))
    day3 = int(input("Day 3 harvest: "))
    print(f"Total harvest: {day1 + day2 + day3}")
