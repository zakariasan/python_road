"""
Exercise 3: Game Engine - Abstract Factory + Strategy Pattern
"""
from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.GameEngine import GameEngine


def main() -> None:
    print("\n=== DataDeck Game Engine ===\n")

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()
    engine = GameEngine()

    print("Configuring Fantasy Card Game...")
    print(f"Factory: {factory.__class__.__name__}")
    print(f"Strategy: {strategy.get_strategy_name()}")
    print(f"Available types: {factory.get_supported_types()}")
    print()

    engine.configure_engine(factory, strategy)

    print("Simulating aggressive turn...")
    turn = engine.simulate_turn()

    print("Turn execution:")
    print(f"Strategy: {turn['strategy']}")
    print(f"Actions: {turn['actions']}")
    print()

    print(f"Game Report:")
    print(engine.get_engine_status())
    print()

    print("Abstract Factory + Strategy Pattern: Maximum flexibility achieved!")


if __name__ == "__main__":
    main()
