"""5e to Daggerheart creature stat block converter.

This module provides utilities to convert a subset of Dungeons & Dragons
5th Edition creature statistics into an equivalent representation for the
Daggerheart role‑playing game.

The conversion implemented here is intentionally simplistic.  Daggerheart
is a different system and there is no one‑to‑one mapping for all concepts.
However, the mapping used by this tool can serve as a starting point for
further refinement.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FiveEStatBlock:
    """Subset of fields from a 5e creature stat block."""

    name: str
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    armor_class: int
    hit_points: int
    challenge_rating: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FiveEStatBlock":
        required = [
            "name",
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
            "armor_class",
            "hit_points",
            "challenge_rating",
        ]
        missing = [key for key in required if key not in data]
        if missing:
            raise KeyError(f"Missing keys for FiveEStatBlock: {', '.join(missing)}")
        return cls(**{key: data[key] for key in required})


@dataclass
class DaggerheartStatBlock:
    """Simple Daggerheart representation produced by the converter."""

    name: str
    level: int
    body: int
    agility: int
    mind: int
    spirit: int
    defense: int
    health: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "level": self.level,
            "body": self.body,
            "agility": self.agility,
            "mind": self.mind,
            "spirit": self.spirit,
            "defense": self.defense,
            "health": self.health,
        }


def ability_average(*scores: int) -> int:
    """Return the rounded average of the provided ability scores."""

    return int(round(sum(scores) / len(scores)))


def challenge_to_level(cr: float) -> int:
    """Convert a 5e challenge rating to an approximate Daggerheart level."""

    import math

    if cr <= 0:
        return 0
    # Map CR directly to level, always rounding up and capping at 20.
    return int(min(math.ceil(cr), 20))


def convert_5e_to_daggerheart(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a 5e stat block dictionary to a Daggerheart representation.

    Parameters
    ----------
    data:
        Mapping containing at least the keys required by :class:`FiveEStatBlock`.

    Returns
    -------
    dict
        Dictionary representing the Daggerheart stat block.
    """

    five_e = FiveEStatBlock.from_dict(data)
    daggerheart = DaggerheartStatBlock(
        name=five_e.name,
        level=challenge_to_level(five_e.challenge_rating),
        body=ability_average(five_e.strength, five_e.constitution),
        agility=five_e.dexterity,
        mind=ability_average(five_e.intelligence, five_e.wisdom),
        spirit=five_e.charisma,
        defense=five_e.armor_class,
        health=five_e.hit_points,
    )
    return daggerheart.to_dict()


if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Convert a 5e stat block JSON file to Daggerheart format",
    )
    parser.add_argument("input", type=Path, help="Path to 5e stat block JSON file")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output path for Daggerheart JSON"
    )
    args = parser.parse_args()

    with args.input.open() as fp:
        data = json.load(fp)

    result = convert_5e_to_daggerheart(data)

    if args.output:
        with args.output.open("w") as fp:
            json.dump(result, fp, indent=2)
    else:
        json.dump(result, sys.stdout, indent=2)
        print()
