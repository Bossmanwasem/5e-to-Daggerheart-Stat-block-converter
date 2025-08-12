# 5e → Daggerheart Converter (MVP)

Rules-driven converter that ingests a 5e monster stat block (JSON or text), normalizes it, 
applies mapping tables, and outputs a Daggerheart adversary in Markdown (and later, Foundry JSON).

## Quickstart

```bash
# (optional) create a venv
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate

# install
pip install -e .

# try the sample
dh-convert examples/5e/goblin_5etools.json --out out/
```

The result will render to `out/goblin.md` using the Jinja2 template in `converter/render/templates/adversary.md.j2`.

## Project layout
- `converter/` core package
  - `__main__.py` Typer CLI
  - `models.py` Pydantic models (5e input & Daggerheart output)
  - `mappings/5e_to_dh.yml` knobs & tables
  - `parsers/` input handlers (start with 5eTools JSON)
  - `render/` Jinja2 templates
- `examples/` sample 5e inputs + expected outputs (for tuning)
- `tests/` snapshot/balance tests
- `docs/` notes, conversion philosophy (do **not** commit private PDFs)

## Notes on licensing/content
- Do not redistribute Darrington Press/Daggerheart texts in this repo unless permitted.
- Keep the conversion logic generic and data-driven; put any private references in your own fork/docs.

## Next steps
- Add CR→Tier mapping & damage scaling tables to `mappings/5e_to_dh.yml`.
- Implement additional parsers (Homebrewery text, plain text).
- Add Foundry VTT JSON renderer if desired.
