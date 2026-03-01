"""
TournamentPlatform - Manages tournament registration and matches
"""
import random
from ex4.TournamentCard import TournamentCard


class TournamentPlatform:
    """
    Manages a full tournament:
    - Register cards with unique IDs
    - Run matches between registered cards
    - Track leaderboard and generate reports
    """

    def __init__(self) -> None:
        """ card_id -> TournamentCard """
        self._roster: dict[str, TournamentCard] = {}
        self._matches_played: int = 0

    def register_card(self, card: TournamentCard) -> str:
        """
        Register a card and return its unique tournament ID.
        ID format: first_word_of_name + _001
        """
        base = card.name.split()[-1].lower()
        card_id = f"{base}_001"

        counter = 1
        while card_id in self._roster:
            counter += 1
            card_id = f"{base}_{counter:03d}"

        card.calculate_rating()
        self._roster[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        """
        Simulate a match between two registered cards.
        Winner is decided by attack_power + small random factor.
        Rating updates use a fixed 16-point exchange.
        """
        if card1_id not in self._roster or card2_id not in self._roster:
            return {"error": "One or both card IDs not found"}

        card1 = self._roster[card1_id]
        card2 = self._roster[card2_id]

        score1 = card1.attack_power + random.randint(0, 5)
        score2 = card2.attack_power + random.randint(0, 5)

        if score1 >= score2:
            winner_id, loser_id = card1_id, card2_id
            winner, loser = card1, card2
        else:
            winner_id, loser_id = card2_id, card1_id
            winner, loser = card2, card1

        winner.update_wins(1)
        loser.update_losses(1)
        self._matches_played += 1

        return {
            "winner": winner_id,
            "loser": loser_id,
            "winner_rating": winner.calculate_rating(),
            "loser_rating": loser.calculate_rating()
        }

    def get_leaderboard(self) -> list:
        """
        Return cards sorted by rating descending.
        Each entry: (rank, name, rating, record)
        """
        sorted_cards = sorted(
            self._roster.items(),
            key=lambda item: item[1].calculate_rating(),
            reverse=True
        )
        board = []
        for rank, (card_id, card) in enumerate(sorted_cards, start=1):
            info = card.get_rank_info()
            board.append({
                "rank": rank,
                "id": card_id,
                "name": card.name,
                "rating": info["rating"],
                "record": info["record"]
            })
        return board

    def generate_tournament_report(self) -> dict:
        """Return a summary report of the tournament"""
        total = len(self._roster)
        avg_rating = (
            sum(c.calculate_rating() for c in self._roster.values()) // total
            if total > 0 else 0
        )
        return {
            "total_cards": total,
            "matches_played": self._matches_played,
            "avg_rating": avg_rating,
            "platform_status": "active"
        }
