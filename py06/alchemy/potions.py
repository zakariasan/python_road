"""
Potion style returning potions with diff import
"""

import alchemy.elements


def healing_potion() -> str:
    """ healing potion created before """
    return ("Healing potion brewed with "
            +
            f"{alchemy.elements.create_fire()}"
            +
            f" and {alchemy.elements.create_water()}")


def strength_potion() -> str:
    """ strength and potion """
    return (
            "Strength potion brewed with "
            +
            f"{alchemy.elements.create_earth()} and "
            +
            f"{alchemy.elements.create_fire()}"
            )


def invisibility_potion() -> str:
    """ make the world invisible """
    return (
            "Invisibility potion brewed with "
            +
            f"{alchemy.elements.create_air()} and "
            +
            f"{alchemy.elements.create_water}"
            )


def wisdom_potion() -> str:
    """ make it wiseeee"""
    return (
             "Wisdom potion brewed with all elements: "
             +
             f"{alchemy.elements.create_fire()} "
             +
             f"{alchemy.elements.create_earth()} "
             +
             f"{alchemy.elements.create_air()} "
             +
             f"{alchemy.elements.create_water}"
            )
