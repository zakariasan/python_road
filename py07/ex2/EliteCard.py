"""
EliteCard - Multiple inheritance: Card + Combatable + Magical
"""
from ex0.Card import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical


class EliteCard(Card, Combatable, Magical):
    """
    A powerful card that combines card fundamentals
    with combat AND magical abilities.

    Multiple inheritance means this class must implement
    ALL abstract methods from Card, Combatable, and Magical.
    """

    def __init__(
            self,
            name: str,
            cost: int,
            rarity: str,
            attack_power: int,
            defense: int,
            mana_pool: int
            ) -> None:
        super().__init__(name, cost, rarity)
        self.attack_power = attack_power  # combat damage
        self.defense = defense            # damage blocking
        self.mana_pool = mana_pool        # available magic mana
        self.health = defense * 2        # health based on defense

    # ── Card abstract method ──────────────────────────────────────────
    def play(self, game_state: dict) -> dict:
        """Play the elite card onto the battlefield"""
        return {
            **game_state,
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": f"Elite card summoned with {self.attack_power} attack"
        }

    def get_card_info(self) -> dict:
        """Return full card info"""
        info = super().get_card_info()
        info.update({
            "type": "Elite",
            "attack_power": self.attack_power,
            "defense": self.defense,
            "mana_pool": self.mana_pool
        })
        return info

    # ── Combatable abstract methods ───────────────────────────────────
    def attack(self, target) -> dict:
        """Attack a target with melee damage"""
        return {
            "attacker": self.name,
            "target": target,
            "damage": self.attack_power,
            "combat_type": "melee"
        }

    def defend(self, incoming_damage: int) -> dict:
        """Block some incoming damage using defense stat"""
        blocked = min(self.defense, incoming_damage)
        taken = incoming_damage - blocked
        self.health -= taken
        return {
            "defender": self.name,
            "damage_taken": taken,
            "damage_blocked": blocked,
            "still_alive": self.health > 0
        }

    def get_combat_stats(self) -> dict:
        """Return combat stats"""
        return {
            "name": self.name,
            "attack_power": self.attack_power,
            "defense": self.defense,
            "health": self.health
        }

    # ── Magical abstract methods ──────────────────────────────────────
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        """Cast a spell consuming mana"""
        mana_cost = len(targets) + 1  # simple cost: 1 per target + 1 base
        self.mana_pool -= mana_cost
        return {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "mana_used": mana_cost
        }

    def channel_mana(self, amount: int) -> dict:
        """Channel mana to refill the pool"""
        self.mana_pool += amount
        return {
            "channeled": amount,
            "total_mana": self.mana_pool
        }

    def get_magic_stats(self) -> dict:
        """Return magic stats"""
        return {
            "name": self.name,
            "mana_pool": self.mana_pool
        }
