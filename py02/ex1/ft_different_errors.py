#!/usr/bin/env python3

"""
Create custom plant alerts, and keep your digital
greenhouse thriving even when things go wrong.
"""

error_nbr = [0]


def garden_operations() -> int | str | None:
    """Demo of catches that can we have in python show Error"""

    if error_nbr[0] == 0:
        return int("abc")
    elif error_nbr[0] == 1:
        return 1337 / 0
    elif error_nbr[0] == 2:
        return open("missing.txt", "r")
    elif error_nbr[0] == 3:
        plants = {"Flower": 5, "Tree": 1}
        return plants['missing_plant']


def test_error_types():
    """ handlle each of the error that happening here"""
    print("=== Garden Error Types Demo ===")

    print("\nTesting ValueError...")
    try:
        error_nbr[0] = 0
        garden_operations()
    except ValueError:
        print("Caught ValueError: invalid literal for int()")

    print("\nTesting ZeroDivisionError...")
    try:
        error_nbr[0] = 1
        garden_operations()
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero")

    print("\nTesting FileNotFoundError...")
    try:
        error_nbr[0] = 2
        garden_operations()
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: No such file '{e.filename}'")

    print("\nTesting KeyError...")
    try:
        error_nbr[0] = 3
        garden_operations()
    except KeyError as e:
        print(f"Caught KeyError: {e}")

    print("\nTesting multiple errors together...")
    try:
        error_nbr[0] = 1
        garden_operations()
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Caught an error, but program continues!")
    print("\nAll error types tested successfully!")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    test_error_types()
