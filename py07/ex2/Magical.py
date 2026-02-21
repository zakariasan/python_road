"""
Magical - Abstract magic interface
"""
from abc import ABC, abstractmethod


class Magical(ABC):
    """
    Abstract interface for cards that can use magic.
    Any card implementing this can cast spells and channel mana.
    """

    @abstractmethod
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        """Cast a spell on targets"""
        pass

    @abstractmethod
    def channel_mana(self, amount: int) -> dict:
        """Channel mana to build magical power"""
        pass

    @abstractmethod
    def get_magic_stats(self) -> dict:
        """Return magic-related stats"""
        pass
