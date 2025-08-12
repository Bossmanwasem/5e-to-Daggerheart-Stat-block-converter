from __future__ import annotations
from typing import Dict, Any, List
import yaml
from .models import FiveEStatblock, DaggerheartAdversary, DHMove

def _pick_vitality(hp: int | None, table: List[Dict[str, Any]]) -> int:
    if hp is None:
        return 8
    for row in table:
        if hp <= row["max_hp"]:
            return row["vitality"]
    return table[-1]["vitality"]

def _avg_damage_from_actions(actions) -> float:
    # Extremely naive: if damage like "1d6+2", estimate average; else 5
    import re, math
    total = 0.0
    count = 0
    for a in actions:
        dmg = a.damage or ""
        m = re.findall(r"(\d+)d(\d+)(?:\+(\d+))?", dmg)
        if m:
            for dice, faces, mod in m:
                dice = int(dice); faces = int(faces); mod = int(mod or 0)
                avg = dice * (faces + 1) / 2 + mod
                total += avg; count += 1
    return (total / count) if count else 5.0

def _pick_damage(avg: float, table: List[Dict[str, Any]]) -> str:
    for row in table:
        if avg <= row["max_avg"]:
            return row["dice"]
    return table[-1]["dice"]

def _defenses_from_ac(ac: int | None, base_guard: int, ac_pivot: int) -> Dict[str, int]:
    # Placeholder: map AC to Guard; set Will/Wits to 10 baseline
    if ac is None:
        return {"Guard": 10, "Will": 10, "Wits": 10}
    offset = ac - ac_pivot
    guard = base_guard + offset
    return {"Guard": guard, "Will": 10, "Wits": 10}

def _tags_from_type(t: str | None, mapping: Dict[str, list]) -> List[str]:
    if not t:
        return []
    t = str(t).lower()
    return mapping.get(t, [t.capitalize()])

def convert_5e_to_dh(m: FiveEStatblock, mappings: Dict[str, Any]) -> DaggerheartAdversary:
    tier = mappings.get("cr_to_tier", {}).get(str(m.cr), "Tier 1")
    vitality = _pick_vitality(m.hp, mappings.get("hp_to_vitality", []))
    avg_dmg = _avg_damage_from_actions(m.actions)
    damage = _pick_damage(avg_dmg, mappings.get("damage_step", []))
    defenses = _defenses_from_ac(m.ac,
                                 mappings["ac_to_defense_offset"]["base_guard"],
                                 mappings["ac_to_defense_offset"]["ac_pivot"])
    tags = _tags_from_type(m.type, mappings.get("type_to_tags", {}))
    speed = {}
    if m.speed:
        for k in ["walk","fly","swim","climb","burrow"]:
            v = getattr(m.speed, k)
            if v: speed[k] = v

    # Convert 5e traits/actions into DH "moves" (very naive mapping for MVP)
    moves = []
    for a in m.actions[:3]:
        text = a.desc or "Use a basic attack."
        moves.append(DHMove(name=a.name, text=text))
    features = [t.desc for t in m.traits[:3] if t.desc]

    return DaggerheartAdversary(
        name=m.name,
        role="Standard",
        tier=tier,
        tags=tags,
        defenses=defenses,
        vitality=vitality,
        damage=damage,
        speed=speed,
        senses=m.senses,
        languages=m.languages,
        features=features,
        moves=moves,
    )
