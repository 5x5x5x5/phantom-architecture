"""Generate the schematic SVG for every catalog entry.

The drawings live in ``scripts/illustrations/``, one module per part of the
catalog, on a shared kit of primitives (``kit.py``). Output is deterministic:
running this twice writes byte-identical files.

Run:
    uv run python scripts/generate_illustrations.py

Output: docs/assets/illustrations/<slug>.svg (twenty-five files).
"""

from __future__ import annotations

import logging

from illustrations import (
    enlightenment,
    industrial,
    late,
    modernism,
    power,
    revolution,
    utopias,
    visions,
)

PARTS = [
    visions,
    enlightenment,
    industrial,
    revolution,
    modernism,
    power,
    utopias,
    late,
]


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for part in PARTS:
        for draw in part.ALL:
            draw()


if __name__ == "__main__":
    main()
