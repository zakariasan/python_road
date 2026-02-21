"""
The abstract foundation class
"""

from abc import ABC, abstractmethod


class Card(ABC):
    """
    abstract fondation class
    """
    def __init__(self, name: str, cost: int, rarity: str) -> None:
        """Constructor"""
        self.name = name
        self.cost = cost
        self.rarity = rarity

    @abstractmethod
    def play(self, game_state: dict) -> dict:
        """ play your card """
        pass

    def get_card_info(self) -> dict:
        """ Get infos about the card """
        return {
                'name': self.name,
                'cost': self.cost,
                'rarity': self.rarity
                }

    def is_playable(self, available_mana: int) -> bool:
        """ check if you can play with the card or no """
        return available_mana >= self.cost
