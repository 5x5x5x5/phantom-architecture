"""Part V — the modernist scale."""

from __future__ import annotations

import random

from .kit import (
    ACCENT,
    EIFFEL,
    EMPIRE,
    FAINT,
    INK,
    PAPER,
    circle,
    dim_h,
    dim_v,
    ground,
    hatch,
    line,
    note,
    path,
    poly,
    rect,
    reference,
    scale_bar,
    text,
    tone,
    write,
)  # fmt: skip


def _notre_dame(x: float, gy: float, s: float) -> str:
    """The west front: two 69 m towers, the flèche behind."""
    out = line(x, gy - 43 * s, x, gy - 96 * s, 0.6, FAINT)
    out += rect(x - 20.5 * s, gy - 43 * s, 41 * s, 43 * s, 0.7, PAPER, FAINT)
    for sx in (-1, 1):
        out += rect(
            x + sx * 14 * s - 6.5 * s, gy - 69 * s, 13 * s, 69 * s, 0.7, PAPER, FAINT
        )
    out += circle(x, gy - 30 * s, 4.5 * s, 0.6, c=FAINT)
    return out


def plan_voisin() -> None:
    """Three of Le Corbusier's eighteen towers, against the Paris they replace."""
    gy, s = 432.0, 0.6
    th, half, wing = 200 * s, 95 * s, 28 * s
    b = [ground(gy)]

    for x in (150, 176, 200, 426, 534, 566):
        b.append(line(x, gy, x, gy - 7, 0.5))
        b.append(circle(x, gy - 10, 4.5, 0.6, PAPER))
    b.append(_notre_dame(240, gy, s))
    b.append(text(240, gy - 96 * s - 13, "Notre-Dame", 6, "middle"))
    b.append(text(240, gy - 96 * s - 5, "69 m towers", 6, "middle"))
    for i in range(5):
        b.append(
            rect(
                262 + i * 15,
                gy - 12 - (i % 2) * 2,
                14,
                12 + (i % 2) * 2,
                0.6,
                PAPER,
                FAINT,
            )
        )
    b.append(reference(480, gy, s, EIFFEL, "Eiffel Tower", "330 m"))

    for cx in (120.0, 360.0, 600.0):
        slab = [
            (cx - half, gy - th),
            (cx + half, gy - th),
            (cx + half, gy - 5),
            (cx - half, gy - 5),
        ]
        b += [poly(slab, 1.2, PAPER), tone(slab, 0.09)]
        b.append(
            hatch(
                [
                    (cx + half * 0.72, gy - th),
                    (cx + half, gy - th),
                    (cx + half, gy - 5),
                    (cx + half * 0.72, gy - 5),
                ],
                2.8,
                62,
                o=0.4,
            )
        )
        for i in range(1, 30):
            b.append(
                line(
                    cx - half,
                    gy - 5 - i * 3.9,
                    cx + half,
                    gy - 5 - i * 3.9,
                    0.25,
                    o=0.6,
                )
            )
        for i in range(1, 24):
            b.append(
                line(
                    cx - half + i * 4.75,
                    gy - th,
                    cx - half + i * 4.75,
                    gy - 5,
                    0.25,
                    o=0.6,
                )
            )
        for dx in (-38, 38):
            b.append(line(cx + dx, gy - th, cx + dx, gy - 5, 0.9))
        front = [
            (cx - wing, gy - th),
            (cx + wing, gy - th),
            (cx + wing, gy - 5),
            (cx - wing, gy - 5),
        ]
        b.append(poly(front, 1.4, PAPER))
        for i in range(1, 30):
            b.append(
                line(cx - wing, gy - 5 - i * 3.9, cx + wing, gy - 5 - i * 3.9, 0.3)
            )
        for i in range(1, 8):
            b.append(
                line(cx - wing + i * 4.2, gy - th, cx - wing + i * 4.2, gy - 5, 0.3)
            )
        b.append(line(cx - half - 2, gy - th, cx + half + 2, gy - th, 1.6))
        for i in range(-6, 7):
            b.append(line(cx + i * 8.6, gy - 5, cx + i * 8.6, gy, 0.7))

    # the elevated motorway threading the park
    b.append(rect(36, gy - 12, 648, 2.5, 0.5, PAPER))
    for x in range(48, 684, 24):
        b.append(line(x, gy - 9.5, x, gy, 0.4))
    for x in (70, 196, 204, 300, 432, 520, 528, 660):
        b.append(rect(x, gy - 14.5, 4, 2, 0, INK))

    # key plan
    px, py = 474.0, 82.0
    for r in range(3):
        for c in range(6):
            x, y = px + c * 34, py + r * 26
            b.append(rect(x - 7, y - 2.5, 14, 5, 0, INK, o=0.85))
            b.append(rect(x - 2.5, y - 7, 5, 14, 0, INK, o=0.85))
    for c in range(7):
        b.append(
            line(px - 17 + c * 34, py - 13, px - 17 + c * 34, py + 65, 0.35, FAINT)
        )
    for r in range(4):
        b.append(
            line(px - 17, py - 13 + r * 26, px + 187, py - 13 + r * 26, 0.35, FAINT)
        )
    b.append(rect(px - 13, py + 42, 94, 20, 0.6, c=ACCENT, dash="3 2"))
    b.append(text(px - 17, py + 78, "Key plan: eighteen cruciform towers", 6.5))
    b.append(text(px - 17, py + 87, "boxed: the three drawn below", 6.5))
    b.append(dim_v(50, gy - th, gy - 16, "200 m", side=-1))
    b.append(dim_h(120, 360, gy - th - 14, "400 m between towers"))
    write(
        "plan-voisin",
        "Plan Voisin — Le Corbusier, 1925",
        "elevation + key plan",
        "",
        "".join(b),
    )


def broadacre() -> None:
    """Wright's dispersed city, in plan: an acre to a family, a spire to a district."""
    rng = random.Random(1932)
    x0, y0, cell = 64.0, 72.0, 74.0
    grid = ["HHOFHHVF", "HCHHOHHF", "FHHLLHOH", "IIMHHFHH"]
    b = []
    for r, row in enumerate(grid):
        for c, kind in enumerate(row):
            x, y = x0 + c * cell, y0 + r * cell
            a, z = (x + 3, y + 3), (x + cell - 3, y + cell - 3)
            sq = [a, (z[0], a[1]), z, (a[0], z[1])]
            if kind == "H":
                lot = (cell - 6) / 6
                for i in range(1, 6):
                    b.append(
                        line(a[0] + i * lot, a[1], a[0] + i * lot, z[1], 0.25, FAINT)
                    )
                    b.append(
                        line(a[0], a[1] + i * lot, z[0], a[1] + i * lot, 0.25, FAINT)
                    )
                for i in range(6):
                    for j in range(6):
                        wd, ht = rng.choice(((4.2, 2.6), (2.6, 4.2), (3.4, 3.4)))
                        hx = a[0] + i * lot + rng.uniform(1.5, lot - wd - 1.5)
                        hy = a[1] + j * lot + rng.uniform(1.5, lot - ht - 1.5)
                        b.append(rect(hx, hy, wd, ht, 0, INK, o=0.85))
            elif kind == "O":
                for i in range(11):
                    for j in range(11):
                        b.append(
                            circle(
                                a[0] + 4 + i * 6, a[1] + 4 + j * 6, 1.5, 0, INK, o=0.45
                            )
                        )
            elif kind == "F":
                split = rng.choice((0.4, 0.5, 0.62))
                mid = a[1] + (z[1] - a[1]) * split
                top = [a, (z[0], a[1]), (z[0], mid), (a[0], mid)]
                bot = [(a[0], mid), (z[0], mid), z, (a[0], z[1])]
                b.append(hatch(top, 3, rng.choice((0, 90, 35)), o=0.45))
                b.append(hatch(bot, 3.6, rng.choice((60, 120, 90)), o=0.4))
                b.append(line(a[0], mid, z[0], mid, 0.3, FAINT))
                b.append(rect(a[0] + 6, mid - 7, 6, 4, 0, INK, o=0.85))
            elif kind == "V":
                b.append(hatch(sq, 2.2, 0, o=0.5))
            elif kind == "I":
                for i in range(3):
                    b.append(
                        rect(a[0] + 8, a[1] + 10 + i * 19, cell - 30, 10, 0, INK, o=0.6)
                    )
                b.append(line(a[0], z[1] - 4, z[0], z[1] - 4, 0.5, dash="1.5 2"))
            elif kind == "M":
                b.append(rect(a[0] + 8, a[1] + 26, cell - 22, 8, 0, INK, o=0.75))
                b.append(
                    hatch(
                        [
                            (a[0] + 8, a[1] + 40),
                            (z[0] - 8, a[1] + 40),
                            (z[0] - 8, a[1] + 58),
                            (a[0] + 8, a[1] + 58),
                        ],
                        3.5,
                        90,
                        o=0.45,
                    )
                )
            elif kind == "C":
                mx, my = x + cell / 2, y + cell / 2
                b.append(circle(mx, my, 25, 0.7))
                b.append(circle(mx, my, 15, 0.5))
                for dx, dy, wd, ht in (
                    (-31, -4, 9, 8),
                    (22, -4, 9, 8),
                    (-5, -32, 10, 8),
                    (-5, 24, 10, 8),
                ):
                    b.append(rect(mx + dx, my + dy, wd, ht, 0, INK, o=0.8))
                b.append(circle(mx, my, 4, 0, ACCENT))

    # section roads, then the arterial along the south edge
    for c in range(9):
        b.append(line(x0 + c * cell, y0, x0 + c * cell, y0 + 4 * cell + 22, 0.8))
    for r in range(5):
        b.append(line(x0, y0 + r * cell, x0 + 8 * cell, y0 + r * cell, 0.8))
    lake = f"M{x0 + 3 * cell + 22},{y0 + 2 * cell + 28}c20,-22 62,-20 92,-8c26,10 30,34 6,44c-30,12 -78,10 -98,-4c-14,-10 -12,-22 0,-32z"
    b.append(path(lake, 0.8, PAPER))
    b.append(path(lake, 0, INK, o=0.12))
    for i in range(3):
        b.append(
            line(
                x0 + 3 * cell + 44 + i * 14,
                y0 + 2 * cell + 34 + i * 9,
                x0 + 3 * cell + 84 + i * 14,
                y0 + 2 * cell + 34 + i * 9,
                0.4,
                FAINT,
            )
        )
    hy = y0 + 4 * cell + 14
    b += [
        rect(x0 - 14, hy - 6, 8 * cell + 28, 12, 0, PAPER),
        line(x0 - 14, hy - 6, x0 + 8 * cell + 14, hy - 6, 1.1),
        line(x0 - 14, hy + 6, x0 + 8 * cell + 14, hy + 6, 1.1),
        line(x0 - 14, hy, x0 + 8 * cell + 14, hy, 0.5, dash="6 4"),
    ]
    for c in (3, 6):
        for dx, dy in ((-8, -13), (8, -13)):
            b.append(circle(x0 + c * cell + dx, hy + dy, 5.5, 0.6))

    ly = 420.0
    b += [
        rect(64, ly - 5, 4.2, 2.6, 0, INK, o=0.85),
        text(73, ly - 1, "One house to the acre", 6.5),
        circle(206, ly - 3.5, 1.5, 0, INK, o=0.45),
        circle(212, ly - 3.5, 1.5, 0, INK, o=0.45),
        text(219, ly - 1, "Orchard", 6.5),
        hatch([(280, ly - 8), (294, ly - 8), (294, ly), (280, ly)], 3, 35, o=0.5),
        text(300, ly - 1, "Field", 6.5),
        rect(350, ly - 7, 16, 6, 0, INK, o=0.6),
        text(372, ly - 1, "Light industry", 6.5),
        line(64, ly + 11, 84, ly + 11, 1.1),
        line(64, ly + 15, 84, ly + 15, 1.1),
        text(90, ly + 16, "Arterial motorway, with roadside market", 6.5),
        circle(330, ly + 13, 4, 0, ACCENT),
        text(340, ly + 16, "Civic centre + the district's one spire", 6.5),
        scale_bar(584, 430, cell, "1/4 mile"),
    ]
    write(
        "broadacre", "Broadacre City — Frank Lloyd Wright, 1932", "plan", "", "".join(b)
    )


def mile_high() -> None:
    """Wright's Illinois: a mile of tapering blades over the Chicago of 1956."""
    cx, gy, s = 330.0, 420.0, 0.21
    h = 1609 * s
    top = gy - h
    rng = random.Random(1956)
    b = [ground(gy)]
    for lo, hi in ((64, 232), (404, 474)):
        x = float(lo)
        while x < hi:
            wd, hgt = rng.uniform(9, 17), rng.uniform(35, 185) * s
            b.append(rect(x, gy - hgt, wd, hgt, 0.6, PAPER, FAINT))
            x += wd + rng.uniform(-2, 5)

    blades = [
        ([(cx - 36, gy), (cx - 13, gy), (cx - 15, gy - 0.3 * h)], 0.05),
        ([(cx - 26, gy), (cx + 2, gy), (cx + 2, top + 12), (cx, top)], 0.1),
        (
            [
                (cx + 2, gy),
                (cx + 25, gy),
                (cx + 5.5, gy - 0.78 * h),
                (cx + 2, gy - 0.8 * h),
            ],
            0.18,
        ),
        ([(cx - 12, gy), (cx + 13, gy), (cx + 1, gy - 0.55 * h)], 0.02),
    ]
    for shape, wash in blades:
        b += [
            poly(shape, 1.1, PAPER),
            tone(shape, wash),
            hatch(shape, 2.7, 0, w=0.3, o=0.6),
        ]
        b.append(poly(shape, 1.1))
    b += [
        line(cx, top, cx, top - 13, 0.8),
        rect(cx - 50, gy - 5, 100, 5, 1.0, PAPER),
        poly(
            [(cx - 9, gy + 1), (cx + 9, gy + 1), (cx, gy + 30)],
            0.7,
            c=FAINT,
            dash="3 2.5",
        ),
        text(cx + 13, gy + 26, "Taproot foundation", 6.5),
        reference(530, gy, s, EMPIRE, "Empire State", "443 m"),
        reference(612, gy, s, EIFFEL, "Eiffel", "330 m"),
        dim_v(262, top, gy, "1,609 m — 528 floors", side=-1),
        note(52, 150, "Terraces step up one flank", (cx + 9, gy - 0.6 * h)),
        note(52, 300, "Chicago, 1956", (150, gy - 40)),
    ]
    write(
        "mile-high",
        "The Illinois / Mile-High — Wright, 1956",
        "elevation",
        "",
        "".join(b),
    )


ALL = [plan_voisin, broadacre, mile_high]
