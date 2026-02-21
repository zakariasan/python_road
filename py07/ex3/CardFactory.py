"""
CardFactory - Abstract factory interface
"""
from abc import ABC, abstractmethod
from ex0.Card import Card


class CardFactory(ABC):
    """
    Abstract factory that defines how cards are created.
    Each concrete factory produces a themed set of cards.
    """

    @abstractmethod
    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        """Create and return a creature card"""
        pass

    @abstractmethod
    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        """Create and return a spell card"""
        pass

    @abstractmethod
    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        """Create and return an artifact card"""
        pass

    @abstractmethod
    def create_themed_deck(self, size: int) -> dict:
        """Create a full themed deck of given size"""
        pass

    @abstractmethod
    def get_supported_types(self) -> dict:
        """Return all supported card types this factory can create"""
        pass
