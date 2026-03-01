"""
TournamentCard - Card + Combatable + Rankable
"""
from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    """
    A card built for tournament play.
    Combines:
      - Card        : play, get_card_info, is_playable
      - Combatable  : attack, defend, get_combat_stats
      - Rankable    : calculate_rating, update_wins/losses, get_rank_info

    Rating uses a simple ELO-style calculation:
      base_rating + (wins * 16) - (losses * 16)
    """

    BASE_RATING = 1000

    def __init__(
            self,
            name: str,
            cost: int,
            rarity: str,
            attack_power: int,
            defense: int,
            base_rating: int = 1000
            ) -> None:
        """Constructor of all """
        super().__init__(name, cost, rarity)
        self.attack_power = attack_power
        self.defense = defense
        self.health = defense * 3
        self._wins = 0
        self._losses = 0
        self._rating = base_rating

    def play(self, game_state: dict) -> dict:
        """Play the tournament card"""
        return {
            **game_state,
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": f"Tournament card {self.name} enters the arena"
        }

    def get_card_info(self) -> dict:
        """Return card info including tournament type"""
        info = super().get_card_info()
        info.update({
            "type": "Tournament",
            "attack_power": self.attack_power,
            "defense": self.defense
        })
        return info

    def attack(self, target) -> dict:
        """Attack a target"""
        return {
            "attacker": self.name,
            "target": target,
            "damage": self.attack_power,
            "combat_type": "tournament"
        }

    def defend(self, incoming_damage: int) -> dict:
        """Block incoming damage using defense"""
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

    def calculate_rating(self) -> int:
        """ELO-style rating: base + wins*16 - losses*16"""
        win = (self._wins * 16)
        loss = (self._losses * 16)
        self._rating = self.BASE_RATING + win - loss
        return self._rating

    def update_wins(self, wins: int) -> None:
        """Add wins and recalculate rating"""
        self._wins += wins
        self.calculate_rating()

    def update_losses(self, losses: int) -> None:
        """Add losses and recalculate rating"""
        self._losses += losses
        self.calculate_rating()

    def get_rank_info(self) -> dict:
        """Return full ranking info"""
        return {
            "name": self.name,
            "rating": self._rating,
            "wins": self._wins,
            "losses": self._losses,
            "record": f"{self._wins}-{self._losses}"
        }

    def get_tournament_stats(self) -> dict:
        """Return combined card + rank stats"""
        return {
            **self.get_card_info(),
            **self.get_rank_info(),
            "combat": self.get_combat_stats()
        }
