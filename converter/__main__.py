import json, sys, os, yaml
import typer
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .parsers import parse_5etools_json
from .convert import convert_5e_to_dh

app = typer.Typer(add_completion=False, help="5e → Daggerheart converter")

@app.command()
def convert(
    input_path: str = typer.Argument(..., help="Path to a 5eTools-style monster JSON"),
    out: str = typer.Option("out", "--out", "-o", help="Output folder"),
    template: str = typer.Option(None, help="Override Jinja2 template"),
    mapping: str = typer.Option(None, help="Override YAML mapping file"),
):
    """Convert a single 5e JSON monster into a Daggerheart adversary (Markdown)."""
    if not os.path.isfile(input_path):
        typer.echo(f"[!] Not found: {input_path}")
        raise typer.Exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    monster = parse_5etools_json(data)

    map_path = mapping or os.path.join(os.path.dirname(__file__), "mappings", "5e_to_dh.yml")
    with open(map_path, "r", encoding="utf-8") as f:
        mappings = yaml.safe_load(f)

    adv = convert_5e_to_dh(monster, mappings)

    # Setup Jinja
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "render", "templates")),
        autoescape=select_autoescape()
    )
    tpl_name = os.path.basename(template) if template else "adversary.md.j2"
    tpl_dir = os.path.dirname(template) if template else None
    if tpl_dir:
        env.loader = FileSystemLoader(tpl_dir)
    tpl = env.get_template(tpl_name)

    os.makedirs(out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(input_path))[0]
    out_md = os.path.join(out, f"{stem}.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(tpl.render(adv=adv))

    typer.echo(f"[✓] Wrote {out_md}")

if __name__ == "__main__":
    app()
