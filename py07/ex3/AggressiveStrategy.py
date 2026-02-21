"""
AggressiveStrategy - Concrete aggressive play strategy
"""
from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):
    """
    Aggressive strategy: play low-cost cards fast,
    attack directly, maximize damage dealt.
    """

    def get_strategy_name(self) -> str:
        """Return strategy name"""
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:
        """
        Aggressive priority: always go for the Enemy Player first,
        then enemy creatures by lowest health.
        """
        player_targets = [t for t in available_targets if "Player" in t]
        other_targets = [t for t in available_targets if "Player" not in t]
        return player_targets + other_targets

    def execute_turn(self, hand: list, battlefield: list) -> dict:
        """
        Execute an aggressive turn:
        - Play lowest cost cards first to flood the board
        - Attack enemy player directly
        """
        # Sort hand by cost ascending (cheap cards first)
        sorted_hand = sorted(hand, key=lambda c: c.cost)

        mana_budget = 10  # available mana for this turn
        cards_played = []
        mana_used = 0
        damage_dealt = 0

        for card in sorted_hand:
            if card.cost <= (mana_budget - mana_used):
                cards_played.append(card.name)
                mana_used += card.cost
                # creatures deal their attack, spells deal cost as damage
                card_info = card.get_card_info()
                if card_info.get("type") == "Creature":
                    damage_dealt += card_info.get("attack", card.cost)
                else:
                    damage_dealt += card.cost

        targets = self.prioritize_targets(["Enemy Player", "Enemy Creature"])

        return {
            "cards_played": cards_played,
            "mana_used": mana_used,
            "targets_attacked": [targets[0]] if targets else [],
            "damage_dealt": damage_dealt
        }
