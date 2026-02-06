"""Advaced file of transformation """

from ..potions import healing_potion
from .basic import lead_to_gold


def philosophers_stone() -> str:
    """ Complicated philosopher Trans"""
    return (
            f"Philosopher’s stone created using {lead_to_gold()}"
            +
            f" and {healing_potion()}"
            )


def elixir_of_life() -> str:
    """ Elixir of the world next Complexe func"""
    return "Elixir of life: eternal youth achieved!"
