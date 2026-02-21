"""
Combatable - Abstract combat interface
"""
from abc import ABC, abstractmethod


class Combatable(ABC):
    """
    Abstract interface for cards that can fight in combat.
    Any card implementing this can attack and defend.
    """

    @abstractmethod
    def attack(self, target) -> dict:
        """Attack a target"""
        pass

    @abstractmethod
    def defend(self, incoming_damage: int) -> dict:
        """Defend against incoming damage"""
        pass

    @abstractmethod
    def get_combat_stats(self) -> dict:
        """Return combat-related stats"""
        pass
