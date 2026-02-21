from ex0 import Card

"""
 Create a concrete implementation
"""


class CreatureCard(Card):
    """ Creat your own Card """
    def __init__(
            self,
            name: str,
            cost: int,
            rarity: str,
            attack: int,
            health: int
            ) -> None:
        super().__init__(name, cost, rarity)
        try:
            if int(attack) > 0:
                self.attack = attack
            else:
                raise ValueError("Attack must be a positive int")
            if int(health) > 0:
                self.health = health
            else:
                raise ValueError("Health must be a positive int")
        except Exception as e:
            print(f"Error: {str(e)}")

    def play(self, game_state: dict) -> dict:
        """ play your Card """
        return {
                **game_state,
                "card_played": self.name,
                "mana_used": self.cost,
                'effect': 'Creature summoned to battlefield'
                }

    def get_card_info(self) -> dict:
        """ Get info about the card """
        info = super().get_card_info()
        info.update({
            "type": "Creature",
            "attack": self.attack,
            "health": self.health
            })
        return info

    def attack_target(self, target) -> dict:
        """ let;s attack the target """
        return {
                "attacker": self.name,
                "target": target,
                "damage_dealt": self.attack,
                "combat_resolved": True
                }
