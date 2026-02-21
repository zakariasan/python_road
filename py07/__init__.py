"""
DataDeck - Master the Art of Abstract Card Architecture
Root package init - exposes all exercise modules.
"""
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard

from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck

from ex2.Combatable import Combatable
from ex2.Magical import Magical
from ex2.EliteCard import EliteCard

from ex3.GameStrategy import GameStrategy
from ex3.CardFactory import CardFactory
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.GameEngine import GameEngine

from ex4.Rankable import Rankable
from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform

__all__ = [
    # ex0
    "Card",
    "CreatureCard",
    # ex1
    "SpellCard",
    "ArtifactCard",
    "Deck",
    # ex2
    "Combatable",
    "Magical",
    "EliteCard",
    # ex3
    "GameStrategy",
    "CardFactory",
    "AggressiveStrategy",
    "FantasyCardFactory",
    "GameEngine",
    # ex4
    "Rankable",
    "TournamentCard",
    "TournamentPlatform",
]
