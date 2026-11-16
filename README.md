# phantom-architecture

A catalog of unbuilt buildings — twenty-five designs, across five centuries, that never left the page. A project inspired by *Phantom Architecture* (Wilkinson, 2017).

**Site:** https://danielsiegle.com/phantom-architecture/

## Local development

```bash
uv sync
uv run mkdocs serve  # live reload at localhost:8000
```

## Deploy

Pushes to `main` trigger `.github/workflows/deploy.yml`, which runs `mkdocs gh-deploy --force` and publishes to the `gh-pages` branch.

## Illustrations

Each entry carries a schematic elevation rendered to SVG in a unified blueprint style. The generator lives in `scripts/generate_illustrations.py`. Run:

```bash
uv run python scripts/generate_illustrations.py
```

Output goes to `docs/assets/illustrations/`. The generator is deterministic; rerunning produces identical files.

## Future directions

See `docs/ideas.md` for project directions that came out of the initial design session — the five nearby variants, and one blend. This catalog (direction #1) is the first of them.
