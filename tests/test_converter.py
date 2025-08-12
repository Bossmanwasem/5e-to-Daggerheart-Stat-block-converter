import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import converter


def test_basic_conversion():
    data = {
        "name": "Orc",
        "strength": 16,
        "dexterity": 12,
        "constitution": 16,
        "intelligence": 7,
        "wisdom": 11,
        "charisma": 10,
        "armor_class": 13,
        "hit_points": 15,
        "challenge_rating": 0.5,
    }
    expected = {
        "name": "Orc",
        "level": 1,  # ceil(0.5)
        "body": 16,  # avg(16,16)
        "agility": 12,
        "mind": 9,  # avg(7,11)
        "spirit": 10,
        "defense": 13,
        "health": 15,
    }
    assert converter.convert_5e_to_daggerheart(data) == expected
