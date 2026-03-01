"""
Exercise 4: Tournament Platform - Advanced Interface Composition
"""
from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main() -> None:
    print("\n=== DataDeck Tournament Platform ===\n")

    platform = TournamentPlatform()

    print("Registering Tournament Cards...\n")

    dragon = TournamentCard(
        name="Fire Dragon",
        cost=5,
        rarity="Legendary",
        attack_power=7,
        defense=5,
        base_rating=1000
    )
    wizard = TournamentCard(
        name="Ice Wizard",
        cost=4,
        rarity="Rare",
        attack_power=5,
        defense=4,
        base_rating=1000
    )

    dragon_id = platform.register_card(dragon)
    wizard_id = platform.register_card(wizard)

    for card_id, card in [(dragon_id, dragon), (wizard_id, wizard)]:
        info = card.get_rank_info()
        print(f"{card.name} (ID: {card_id}):")
        print("- Interfaces: [Card, Combatable, Rankable]")
        print(f"- Rating: {info['rating']}")
        print(f"- Record: {info['record']}")
        print()

    print("Creating tournament match...")
    result = platform.create_match(dragon_id, wizard_id)
    print(f"Match result: {result}")
    print()

    print("Tournament Leaderboard:")
    for entry in platform.get_leaderboard():
        print(
            f"{entry['rank']}. {entry['name']} "
            f"- Rating: {entry['rating']} "
            f"({entry['record']})"
        )
    print()

    print("Platform Report:")
    print(platform.generate_tournament_report())
    print()

    print("=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")


main()
