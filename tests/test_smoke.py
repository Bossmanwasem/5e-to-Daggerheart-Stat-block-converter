import json, os
from converter.parsers import parse_5etools_json
from converter.convert import convert_5e_to_dh
import yaml

def test_convert_smoke():
    with open("examples/5e/goblin_5etools.json","r",encoding="utf-8") as f:
        data = json.load(f)
    m = parse_5etools_json(data)
    with open("converter/mappings/5e_to_dh.yml","r",encoding="utf-8") as f:
        mappings = yaml.safe_load(f)
    adv = convert_5e_to_dh(m, mappings)
    assert adv.name == "Goblin"
    assert adv.vitality > 0
    assert adv.damage in {"1d6","1d8","1d10","2d6","2d8","2d10"}
