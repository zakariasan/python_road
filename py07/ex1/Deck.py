"""
Deck - Management system for cards
"""
import random
from typing import Optional
from ex0.Card import Card


class Deck:
    """
    Manages a collection of cards.
    Can hold any card type that inherits from Card.
    """
    def __init__(self) -> None:
        """ Plat where we can play with our Cards """
        self._cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        """Add a card to the deck"""
        self._cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        """Remove a card by name"""
        for card in self._cards:
            if card.name == card_name:
                self._cards.remove(card)
                return True
        return False

    def shuffle(self) -> None:
        """Shuffle the deck randomly"""
        random.shuffle(self._cards)

    def draw_card(self) -> Optional[Card]:
        """Draw the top card from the deck"""
        if not self._cards:
            return None
        return self._cards.pop(0)

    def get_deck_stats(self) -> dict:
        """Return statistics about the current deck"""
        total = len(self._cards)
        creatures = sum(
            1 for c in self.
            _cards if c.get_card_info().get("type") == "Creature"
        )
        spells = sum(
            1 for c in self.
            _cards if c.get_card_info().get("type") == "Spell"
        )
        artifacts = sum(
            1 for c in self.
            _cards if c.get_card_info().get("type") == "Artifact"
        )
        avg_cost = round(
            sum(c.cost for c in self._cards) / total, 1
        ) if total > 0 else 0.0

        return {
            "total_cards": total,
            "creatures": creatures,
            "spells": spells,
            "artifacts": artifacts,
            "avg_cost": avg_cost
        }
