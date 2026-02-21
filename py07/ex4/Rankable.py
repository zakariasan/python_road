"""
Rankable - Abstract ranking interface
"""
from abc import ABC, abstractmethod


class Rankable(ABC):
    """
    Abstract interface for anything that can be ranked.
    Tracks wins, losses, and calculates a rating score.
    """

    @abstractmethod
    def calculate_rating(self) -> int:
        """Calculate and return the current rating"""
        pass

    @abstractmethod
    def update_wins(self, wins: int) -> None:
        """Add wins to the record"""
        pass

    @abstractmethod
    def update_losses(self, losses: int) -> None:
        """Add losses to the record"""
        pass

    @abstractmethod
    def get_rank_info(self) -> dict:
        """Return full ranking information"""
        pass
