"""
FantasyCardFactory - Creates fantasy themed cards
"""
import random
from ex3.CardFactory import CardFactory
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard


class FantasyCardFactory(CardFactory):
    """
    Concrete factory that creates fantasy-themed cards:
    creatures like Dragons and Goblins, elemental spells,
    and magical artifacts.
    """

    _creatures = {
        "dragon": ("Fire Dragon", 5, "Legendary", 7, 5),
        "goblin": ("Goblin Warrior", 2, "Common", 3, 2),
        # "knight": ("Iron Knight", 4, "Rare", 4, 6),
    }

    _spells = {
        "fireball": ("Fireball", 4, "Rare", "damage"),
        "lightning": ("Lightning Bolt", 3, "Common", "damage"),
        "heal": ("Holy Light", 2, "Common", "heal"),
    }

    _artifacts = {
        "mana_ring": ("Mana Ring", 2, "Rare", 5, "+1 mana per turn"),
        "staff": ("Arcane Staff", 3, "Rare", 4, "+2 spell damage"),
        "crystal": ("Mana Crystal", 1, "Common", 3, "+1 mana per turn"),
    }

    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        """Create a fantasy creature."""
        if isinstance(name_or_power, str) and name_or_power in self._creatures:
            data = self._creatures[name_or_power]
        else:
            data = random.choice(list(self._creatures.values()))
        name, cost, rarity, attack, health = data
        return CreatureCard(name, cost, rarity, attack, health)

    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        """Create a fantasy spell."""
        if isinstance(name_or_power, str) and name_or_power in self._spells:
            data = self._spells[name_or_power]
        else:
            data = random.choice(list(self._spells.values()))
        name, cost, rarity, effect_type = data
        return SpellCard(name, cost, rarity, effect_type)

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        """Create a fantasy artifacttt."""
        if isinstance(name_or_power, str) and name_or_power in self._artifacts:
            data = self._artifacts[name_or_power]
        else:
            data = random.choice(list(self._artifacts.values()))
        name, cost, rarity, durability, effect = data
        return ArtifactCard(name, cost, rarity, durability, effect)

    def create_themed_deck(self, size: int) -> dict:
        """Create a balanced themed deck of given size"""
        creatures = []
        spells = []
        artifacts = []

        for i in range(size):
            roll = i % 3
            if roll == 0:
                creatures.append(self.create_creature())
            elif roll == 1:
                spells.append(self.create_spell())
            else:
                artifacts.append(self.create_artifact())

        return {
            "creatures": creatures,
            "spells": spells,
            "artifacts": artifacts,
            "total": size
        }

    def get_supported_types(self) -> dict:
        """Return all card types this factory supports"""
        return {
            "creatures": list(self._creatures.keys()),
            "spells": list(self._spells.keys()),
            "artifacts": list(self._artifacts.keys())
        }
