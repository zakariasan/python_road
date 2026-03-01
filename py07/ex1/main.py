"""
Exercise 1: Deck Builder - Polymorphism with multiple card types
"""
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck


def main() -> None:
    print("\n=== DataDeck Deck Builder ===\n")
    print("Building deck with different card types...")

    deck = Deck()

    dragon = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    bolt = SpellCard("Lightning Bolt", 3, "Common", "damage")
    crystal = ArtifactCard("Mana Crystal", 2, "Rare", 5, "+1 mana per turn")

    deck.add_card(bolt)
    deck.add_card(dragon)
    deck.add_card(crystal)

    print(f"Deck stats: {deck.get_deck_stats()}")
    print()
    print("Drawing and playing cards:")
    print()

    deck.shuffle()

    while True:
        card = deck.draw_card()
        if card is None:
            break
        card_type = card.get_card_info().get("type", "Wirdo_Card")
        print(f"Drew: {card.name} ({card_type})")
        print(f"Play result: {card.play({})}")
        print()

    print("Polymorphism in action: Same interface, different card behaviors!")


main()
