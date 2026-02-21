from ex0.CreatureCard import CreatureCard

"""
    Exercise 0: Card Foundation - Master abstract base classes
"""


def main() -> None:
    print("\n=== DataDeck Card Foundation ===\n")

    print("Testing Abstract Base Class Design:\n")
    print("CreatureCard Info:\n")
    my_card = CreatureCard(
            'Fire Dragon',
            5,
            'Legendary',
            7,
            5)
    print(my_card.get_card_info())
    print()
    print("Playing Fire Dragon with 6 mana available:")
    print(f"Playable: {my_card.is_playable(6)}")
    print(f"Play result: {my_card.play({})}")

    print()
    print("Fire Dragon attacks Goblin Warrior:")
    print(f"Attack result: {my_card.attack_target('Goblin Warrior')}")

    print()
    print("Testing insufficient mana (3 available):")
    print(f"Playable {my_card.is_playable(3)}")

    print()
    print("Abstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()
