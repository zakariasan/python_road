"""
ArtifactCard - Permanent game modifiers
"""
from ex0.Card import Card


class ArtifactCard(Card):
    """
    Concrete implementation of an artifact card.
    Artifacts stay in play and provide ongoing effects.
    """
    def __init__(
            self,
            name: str,
            cost: int,
            rarity: str,
            durability: int,
            effect: str
            ) -> None:
        """ Starting form the Art of Card"""
        super().__init__(name, cost, rarity)
        self.durability = durability
        self.effect = effect
        self.active = True

    def play(self, game_state: dict) -> dict:
        """Play the artifact - stays on the battlefield"""
        return {
            **game_state,
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": f"Permanent: {self.effect}"
        }

    def activate_ability(self) -> dict:
        """Activate the artifact's ongoing effect"""
        if not self.active or self.durability <= 0:
            return {
                "artifact": self.name,
                "activated": False,
                "reason": "Artifact is destroyed"
            }
        self.durability -= 1
        if self.durability == 0:
            self.active = False
        return {
            "artifact": self.name,
            "effect": self.effect,
            "activated": True,
            "durability_remaining": self.durability
        }

    def get_card_info(self) -> dict:
        """Get info about the artifact card"""
        info = super().get_card_info()
        info.update({
            "type": "Artifact",
            "durability": self.durability,
            "effect": self.effect,
            "active": self.active
        })
        return info
