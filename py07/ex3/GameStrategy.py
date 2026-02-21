"""
GameStrategy - Abstract strategy interface
"""
from abc import ABC, abstractmethod


class GameStrategy(ABC):
    """
    Abstract interface defining how a player strategy behaves.
    Different strategies (aggressive, defensive, control) implement this.
    """

    @abstractmethod
    def execute_turn(self, hand: list, battlefield: list) -> dict:
        """Execute a full turn given hand and battlefield state"""
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Return the name of this strategy"""
        pass

    @abstractmethod
    def prioritize_targets(self, available_targets: list) -> list:
        """Return targets sorted by priority for this strategy"""
        pass
