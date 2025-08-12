# 5e to Daggerheart Stat Block Converter

This repository contains a simple Python utility for translating a subset of
Dungeons & Dragons 5th Edition creature statistics into an equivalent
representation for the Daggerheart role‑playing game.

The mapping implemented here is intentionally lightweight and is intended as a
starting point for further refinement.  Not all concepts from either system are
covered.

## Usage

```
python converter.py path/to/5e_stat_block.json -o daggerheart.json
```

The input file must be a JSON object with the following keys:

- `name`
- `strength`
- `dexterity`
- `constitution`
- `intelligence`
- `wisdom`
- `charisma`
- `armor_class`
- `hit_points`
- `challenge_rating`

The resulting file will contain a Daggerheart stat block with the fields:
`name`, `level`, `body`, `agility`, `mind`, `spirit`, `defense`, and `health`.

## Development

Run the tests with:

```
pytest
```
