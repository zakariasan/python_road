"""
SpellCard - Instant magic effects
"""
from ex0.Card import Card


class SpellCard(Card):
    """
    Concrete implementation of a spell card.
    Spells are one-time use instant effects.
    """
    def __init__(
            self,
            name: str,
            cost: int,
            rarity: str,
            effect_type: str
            ) -> None:
        """ instance of spellCard """
        super().__init__(name, cost, rarity)
        self.effect_type = effect_type
        self.used = False

    def play(self, game_state: dict) -> dict:
        """Play the spell - one time use"""
        self.used = True
        descriptions = {
            "damage": f"Deal {self.cost} damage to target",
            "heal": f"Restore {self.cost * 2} health",
            "buff": f"Grant +{self.cost} attack to ally",
            "debuff": f"Reduce enemy attack by {self.cost}"
        }
        effect_desc = descriptions.get(
                self.effect_type,
                f"Apply {self.effect_type} effect")
        return {
            **game_state,
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": effect_desc
        }

    def resolve_effect(self, targets: list) -> dict:
        """Resolve the spell effect on targets"""
        return {
            "spell": self.name,
            "effect_type": self.effect_type,
            "targets": targets,
            "resolved": True
        }

    def get_card_info(self) -> dict:
        """Get info about the spell card"""
        info = super().get_card_info()
        info.update({
            "type": "Spell",
            "effect_type": self.effect_type,
            "used": self.used
        })
        return info
