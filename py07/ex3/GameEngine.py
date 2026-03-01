"""
GameEngine - Orchestrates factory + strategy together
"""
from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    """
    The brain of DataDeck.
    Combines a CardFactory (what cards exist) with a
    GameStrategy (how to play them) to simulate turns.
    """

    def __init__(self) -> None:
        """Gat starting """
        self._factory: CardFactory | None = None
        self._strategy: GameStrategy | None = None
        self._turns_simulated: int = 0
        self._total_damage: int = 0
        self._cards_created: int = 0
        self._hand: list = []

    def configure_engine(
            self,
            factory: CardFactory,
            strategy: GameStrategy
            ) -> None:
        """Set which factory and strategy the engine uses"""
        self._factory = factory
        self._strategy = strategy

        dragon = self._factory.create_creature("dragon")
        goblin = self._factory.create_creature("goblin")
        bolt = self._factory.create_spell("lightning")
        self._hand = [dragon, goblin, bolt]
        self._cards_created = len(self._hand)

    def simulate_turn(self) -> dict:
        """Run one turn using the configured strategy"""
        if not self._factory or not self._strategy:
            return {"error": "Engine not configured"}

        hand_display = [
            f"{c.name} ({c.cost})" for c in self._hand
        ]
        print(f"Hand: [{', '.join(hand_display)}]")
        print()

        result = self._strategy.execute_turn(self._hand, [])

        self._turns_simulated += 1
        self._total_damage += result.get("damage_dealt", 0)

        return {
            "strategy": self._strategy.get_strategy_name(),
            "actions": result
        }

    def get_engine_status(self) -> dict:
        """Return a report of engine activity"""
        return {
            "turns_simulated": self._turns_simulated,
            "strategy_used": self._strategy.get_strategy_name()
            if self._strategy else None,
            "total_damage": self._total_damage,
            "cards_created": self._cards_created
        }
