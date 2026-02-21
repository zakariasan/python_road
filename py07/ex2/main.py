"""
Exercise 2: Ability System - Multiple interface inheritance
"""
from ex2.EliteCard import EliteCard


def main() -> None:
    print("\n=== DataDeck Ability System ===\n")

    # Show what interfaces EliteCard implements
    print("EliteCard capabilities:")
    print("- Card: ['play', 'get_card_info', 'is_playable']")
    print("- Combatable: ['attack', 'defend', 'get_combat_stats']")
    print("- Magical: ['cast_spell', 'channel_mana', 'get_magic_stats']")
    print()

    # Create an elite card
    warrior = EliteCard(
        name="Arcane Warrior",
        cost=6,
        rarity="Legendary",
        attack_power=5,
        defense=3,
        mana_pool=4
    )

    print(f"Playing {warrior.name} (Elite Card):\n")

    # ── Combat phase ─────────────────────────────────────────────────
    print("Combat phase:")
    print(f"Attack result: {warrior.attack('Enemy')}")
    print(f"Defense result: {warrior.defend(5)}")
    print()

    # ── Magic phase ──────────────────────────────────────────────────
    print("Magic phase:")
    print(f"Spell cast: {warrior.cast_spell('Fireball', ['Enemy1', 'Enemy2'])}")
    print(f"Mana channel: {warrior.channel_mana(3)}")
    print()

    print("Multiple interface implementation successful!")


if __name__ == "__main__":
    main()
