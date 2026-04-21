# phantom-architecture — catalog of unbuilt buildings

MkDocs Material site deployed to GitHub Pages. A catalog of twenty-five
designs that were drawn, modeled, or otherwise imagined but never built
(or were partially built and then lost).

## Layout

    docs/
      index.md                          Front matter / introduction
      ideas.md                          Six project directions from the
                                        original design session — this
                                        catalog is #1
      about.md                          Method, sources, attribution
      visions-before-modernity/         Part I (3 entries)
      enlightenment/                    Part II (3 entries)
      industrial/                       Part III (3 entries)
      revolution/                       Part IV (2 entries)
      modernism/                        Part V (3 entries)
      power/                            Part VI (2 entries)
      utopias/                          Part VII (6 entries)
      late/                             Part VIII (3 entries)
      assets/illustrations/             SVGs, one per entry
      stylesheets/archive.css           Custom CSS (paper/blueprint palette)
    scripts/generate_illustrations.py   Deterministic SVG generator

## Voice

- Scholarly but not dry. Each entry reads like a museum placard
  written by someone who has thought about the design for a long time.
- Historical accuracy in the main strokes; acknowledge interpretive
  sections as such.
- Each entry: 400-600 words, divided roughly into:
  - Metadata header (architect, year, site, height, status)
  - What it was
  - Why it failed
  - What it meant / what-if

## Commands

- `uv sync` — install mkdocs-material
- `uv run mkdocs serve` — live preview
- `uv run mkdocs build` — static output in `site/`
- `uv run python scripts/generate_illustrations.py` — (re)generate all SVGs
- `git push origin main` — triggers GitHub Actions deploy
