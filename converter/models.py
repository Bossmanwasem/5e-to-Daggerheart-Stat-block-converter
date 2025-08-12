from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# ---- 5e normalized input (subset for MVP) ----

class FiveESpeed(BaseModel):
    walk: Optional[int] = None
    fly: Optional[int] = None
    swim: Optional[int] = None
    climb: Optional[int] = None
    burrow: Optional[int] = None

class FiveEAction(BaseModel):
    name: str
    desc: str
    to_hit: Optional[int] = None
    damage: Optional[str] = None  # e.g., "1d6+2"
    save_dc: Optional[int] = None
    save_ability: Optional[str] = None

class FiveEStatblock(BaseModel):
    name: str
    size: Optional[str] = None
    type: Optional[str] = None
    alignment: Optional[str] = None
    ac: Optional[int] = None
    hp: Optional[int] = None
    hit_dice: Optional[str] = None
    speed: Optional[FiveESpeed] = None
    str: Optional[int] = None
    dex: Optional[int] = None
    con: Optional[int] = None
    int: Optional[int] = None
    wis: Optional[int] = None
    cha: Optional[int] = None
    skills: Dict[str, int] = Field(default_factory=dict)
    senses: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    cr: Optional[str] = None
    traits: List[FiveEAction] = Field(default_factory=list)
    actions: List[FiveEAction] = Field(default_factory=list)
    reactions: List[FiveEAction] = Field(default_factory=list)
    legendary_actions: List[FiveEAction] = Field(default_factory=list)

# ---- Daggerheart adversary output (very rough MVP scaffold) ----

class DHMove(BaseModel):
    name: str
    text: str
    trigger: Optional[str] = None

class DaggerheartAdversary(BaseModel):
    name: str
    role: str = "Standard"  # e.g., Minion / Standard / Elite / Boss (tune later)
    tier: str = "Tier 1"    # placeholder tier mapping
    tags: List[str] = Field(default_factory=list)
    defenses: Dict[str, int] = Field(default_factory=dict)  # e.g., Guard, Will, Wits
    vitality: int = 8        # placeholder
    damage: str = "1d6"      # placeholder
    speed: Dict[str, int] = Field(default_factory=dict)
    senses: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    moves: List[DHMove] = Field(default_factory=list)
