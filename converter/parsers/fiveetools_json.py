from __future__ import annotations
from typing import Any, Dict, List
from pydantic import TypeAdapter
from ..models import FiveEStatblock, FiveEAction, FiveESpeed

def _extract_actions(lst: List[Dict[str, Any]]) -> List[FiveEAction]:
    out = []
    for it in lst or []:
        name = it.get("name") or it.get("title") or "Action"
        desc = it.get("entries") or it.get("desc") or ""
        if isinstance(desc, list):
            desc = " ".join(x if isinstance(x, str) else str(x) for x in desc)
        to_hit = it.get("attackBonus")
        damage = None
        if "damage" in it:
            # try to join damage parts if present
            dmg = it["damage"]
            if isinstance(dmg, list):
                damage = " + ".join(d.get("roll", "") for d in dmg if isinstance(d, dict))
        out.append(FiveEAction(name=name, desc=desc or "", to_hit=to_hit, damage=damage))
    return out

def parse_5etools_json(data: Dict[str, Any]) -> FiveEStatblock:
    # Expect a single monster object similar to 5eTools schema
    name = data.get("name", "Unknown")
    ac = None
    if "ac" in data:
        ac_entry = data["ac"]
        if isinstance(ac_entry, list):
            ac = ac_entry[0].get("ac") if isinstance(ac_entry[0], dict) else ac_entry[0]
        elif isinstance(ac_entry, dict):
            ac = ac_entry.get("ac")
        else:
            ac = ac_entry

    hp = None
    if "hp" in data:
        hp_entry = data["hp"]
        if isinstance(hp_entry, dict):
            hp = hp_entry.get("average")
            hit_dice = hp_entry.get("formula")
        else:
            hp = hp_entry
            hit_dice = None
    else:
        hit_dice = None

    speed = data.get("speed", {})
    spd = FiveESpeed(
        walk=speed.get("walk"),
        fly=speed.get("fly"),
        swim=speed.get("swim"),
        climb=speed.get("climb"),
        burrow=speed.get("burrow"),
    )

    senses = []
    if "senses" in data:
        if isinstance(data["senses"], list):
            senses = data["senses"]
        elif isinstance(data["senses"], str):
            senses = [data["senses"]]

    languages = []
    if "languages" in data:
        if isinstance(data["languages"], list):
            languages = data["languages"]
        elif isinstance(data["languages"], str):
            languages = [data["languages"]]

    actions = _extract_actions(data.get("action", []))
    traits = _extract_actions(data.get("trait", []))
    reactions = _extract_actions(data.get("reaction", []))
    legendary = _extract_actions(data.get("legendary", []))

    model = FiveEStatblock(
        name=name,
        size=data.get("size"),
        type=data.get("type"),
        alignment=data.get("alignment"),
        ac=ac,
        hp=hp,
        hit_dice=hit_dice,
        speed=spd,
        str=data.get("str"),
        dex=data.get("dex"),
        con=data.get("con"),
        int=data.get("int"),
        wis=data.get("wis"),
        cha=data.get("cha"),
        skills={},
        senses=senses,
        languages=languages,
        cr=str(data.get("cr")) if data.get("cr") is not None else None,
        traits=traits,
        actions=actions,
        reactions=reactions,
        legendary_actions=legendary,
    )
    return model
