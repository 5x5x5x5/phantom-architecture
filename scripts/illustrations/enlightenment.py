"""Part II — the Enlightenment."""

from __future__ import annotations

import math
import random

from .kit import (
    FAINT,
    INK,
    PAPER,
    Pt,
    arc,
    box,
    circle,
    cypress,
    dim_v,
    ground,
    hatch,
    line,
    note,
    person,
    poly,
    rect,
    scale_bar,
    text,
    tone,
    write,
)  # fmt: skip


def newton_cenotaph() -> None:
    """Boullée's sphere, sunk into three planted terraces."""
    cx, gy, r = 360.0, 432.0, 150.0
    cy = gy - r - 2
    rng = random.Random(1784)
    b = [ground(gy), circle(cx, cy, r, 1.7, PAPER)]
    b.append(
        hatch(
            arc(cx, cy, r, r, -78, 78) + arc(cx, cy, r * 0.6, r, 78, -78), 3, 60, o=0.4
        )
    )
    # the shell is pierced so that daylight reads as stars from inside
    for _ in range(120):
        a, d = rng.uniform(0, math.tau), r * 0.93 * math.sqrt(rng.random())
        b.append(
            circle(
                cx + d * math.cos(a),
                cy - d * math.sin(a),
                rng.choice((0.6, 0.8, 1.1)),
                0,
                INK,
            )
        )

    for hw, top, bot, trees in (
        (176, 322, 358, 20),
        (222, 358, 396, 23),
        (262, 396, gy, 26),
    ):
        if hw == 176:
            for deg in range(-84, 85, 4):
                b.append(
                    cypress(cx + (hw - 6) * math.sin(math.radians(deg)), top, trees)
                )
        b.append(rect(cx - hw, top, 2 * hw, bot - top, 1.3, PAPER))
        b.append(line(cx - hw, top + 4, cx + hw, top + 4, 0.5))
        b.append(
            hatch(
                [
                    (cx + hw * 0.7, top),
                    (cx + hw, top),
                    (cx + hw, bot),
                    (cx + hw * 0.7, bot),
                ],
                3,
                60,
                o=0.35,
            )
        )
        if hw != 176:
            inner = hw - 44
            for deg in range(-84, 85, 4):
                x = cx + (inner + 38) * math.sin(math.radians(deg))
                if abs(x - cx) > 42:
                    b.append(cypress(x, top, trees))

    stair = [(cx - 36, gy), (cx + 36, gy), (cx + 18, 358), (cx - 18, 358)]
    b.append(poly(stair, 1.0, PAPER))
    for i in range(1, 18):
        y = gy - i * 4.1
        half = 36 - 18 * (gy - y) / (gy - 358)
        b.append(line(cx - half, y, cx + half, y, 0.4))
    portal = [(cx - 8, 358), *arc(cx, 342, 8, 8, 180, 0, 8), (cx + 8, 358)]
    b.append(poly(portal, 0, INK))
    for x, y in (
        (cx - 7, 372),
        (cx + 5, 392),
        (cx - 52, gy),
        (cx + 61, gy),
        (cx + 70, gy),
        (148, gy),
        (604, gy),
    ):
        b.append(person(x, y, 3.6))
    b.append(dim_v(650, cy - r, cy + r, "sphere c. 150 m"))
    write(
        "newton-cenotaph",
        "Cenotaph for Newton — Boullée, 1784",
        "elevation",
        "figures at the stair to scale",
        "".join(b),
    )


def chaux() -> None:
    """Ledoux's saltworks: the half that was built, and the half that was not."""
    cx, cy, rr = 360.0, 258.0, 118.0

    def at(deg: float, rad: float) -> Pt:
        a = math.radians(deg)
        return (cx + rad * math.cos(a), cy - rad * math.sin(a))

    b = []
    # projected: the mirror half that would have closed the circle
    for rad in (rr, rr + 24, rr + 54):
        b.append(
            poly(
                arc(cx, cy, rad, rad, 180, 360, 40),
                0.7,
                c=FAINT,
                close=False,
                dash="4 3",
            )
        )
    for deg in (198, 234, 270, 306, 342):
        b.append(
            poly(box(*at(deg, rr + 10), 46, 17, deg - 90), 0.7, c=FAINT, dash="3 2.5")
        )
        b.append(line(cx, cy, *at(deg, rr), 0.35, FAINT, dash="2 4"))
    b.append(text(cx, cy + 60, "Second half projected", 6.5, "middle"))
    b.append(text(cx, cy + 70, "never built", 6.5, "middle"))

    # built: court, gardens behind each pavilion, and the wall along the diameter
    b.append(tone(arc(cx, cy, rr, rr, 0, 180, 40), 0.06))
    for deg in range(0, 181, 5):
        b.append(line(*at(deg, rr + 25), *at(deg, rr + 51), 0.35, FAINT))
    for rad, wt in ((rr, 1.0), (rr + 24, 0.6), (rr + 54, 1.2)):
        b.append(poly(arc(cx, cy, rad, rad, 0, 180, 40), wt, close=False))
    b.append(line(cx - rr - 54, cy, cx + rr + 54, cy, 1.2))
    for deg in (18, 54, 90, 126, 162):
        b.append(line(cx, cy - 17, *at(deg, rr), 0.4, FAINT))
        gate = deg == 90
        b.append(
            poly(
                box(
                    *at(deg, rr + 10), 56 if gate else 46, 19 if gate else 17, deg - 90
                ),
                1.0,
                INK,
                o=0.85,
            )
        )
    for i in range(6):
        b.append(circle(cx - 20 + i * 8, cy - rr - 24, 1.4, 0, INK))
        b.append(circle(cx - 12.5 + i * 5, cy - 22, 1.1, 0, INK))
    b += [
        rect(cx - 15, cy - 17, 30, 30, 1.0, INK, o=0.9),
        rect(cx - 94, cy - 13, 64, 24, 1.0, INK, o=0.85),
        rect(cx + 30, cy - 13, 64, 24, 1.0, INK, o=0.85),
        rect(cx - 10, cy + 19, 20, 11, 0.8, PAPER),
        text(cx, cy - rr - 62, "Gatehouse", 6.5, "middle"),
        note(578, 150, "Workshops + lodgings", at(18, rr + 10)),
        note(578, 236, "Kitchen gardens", at(5, rr + 38)),
        note(578, 318, "Director's house", (cx + 9, cy + 7)),
        note(142, 150, "Lines of sight", at(140, rr * 0.6), "end"),
        note(142, 318, "Salt workshops", (cx - 70, cy + 5), "end"),
        rect(48, 438, 12, 6, 0.8, INK, o=0.85),
        text(66, 444, "Built 1775–79", 6.5),
        rect(160, 438, 12, 6, 0.7, c=FAINT, dash="3 2.5"),
        text(178, 444, "Projected", 6.5),
        scale_bar(608, 440, 64, "100 m"),
    ]
    write("chaux", "Royal Saltworks at Chaux — Ledoux, 1775", "plan", "", "".join(b))


def _statue(x: float, y: float) -> str:
    return line(x, y, x, y - 6, 1.0) + circle(x, y - 7.5, 1.3, 0, INK)


def soane_royal_palace() -> None:
    """Soane's student palace: portico, saucer dome, colonnaded wings."""
    cx, gy = 360.0, 432.0
    b = [ground(gy)]

    # dome and drum, behind everything
    dome = [(cx - 42, 229), *arc(cx, 229, 42, 31, 180, 0, 20), (cx + 42, 229)]
    b += [
        poly(dome, 1.2, PAPER),
        hatch(
            arc(cx, 229, 42, 31, 0, 80, 10) + arc(cx, 229, 24, 31, 80, 0, 10),
            2.6,
            60,
            o=0.4,
        ),
        rect(cx - 5, 193, 10, 6, 0.9, PAPER),
        circle(cx, 190, 2.4, 0.9, PAPER),
        rect(cx - 46, 229, 92, 5, 0.9, PAPER),
        rect(cx - 50, 234, 100, 6, 0.9, PAPER),
        rect(cx - 54, 240, 108, 34, 1.1, PAPER),
    ]
    for deg in range(-75, 76, 15):
        x = cx + 54 * math.sin(math.radians(deg))
        b.append(line(x, 243, x, 272, 0.5))

    # wings and end pavilions
    for sx in (-1, 1):
        inner, outer = cx + sx * 150, cx + sx * 290
        pav = outer - sx * 50
        lo, hi = min(inner, pav), max(inner, pav)
        b += [
            rect(lo, 346, hi - lo, gy - 346, 1.1, PAPER),
            rect(lo, 338, hi - lo, 8, 0.9, PAPER),
            rect(lo, 329, hi - lo, 9, 0.6, PAPER),
            line(lo, 416, hi, 416, 0.6),
        ]
        for i in range(int((hi - lo) / 4)):
            b.append(line(lo + 2 + i * 4, 331, lo + 2 + i * 4, 337, 0.4))
        bay = (hi - lo) / 4
        for i in range(5):
            b.append(rect(lo + i * bay - 2, 346, 4, 70, 0.7, PAPER))
        for i in range(4):
            x = lo + (i + 0.5) * bay
            b.append(
                poly(
                    [(x - 5, 410), *arc(x, 376, 5, 5, 180, 0, 6), (x + 5, 410)],
                    0.7,
                    INK,
                    o=0.7,
                )
            )
        plo, phi = min(pav, outer), max(pav, outer)
        mid = (plo + phi) / 2
        b += [
            rect(plo, 330, 50, gy - 330, 1.2, PAPER),
            poly([(plo - 4, 330), (mid, 311), (phi + 4, 330)], 1.2, PAPER),
            line(plo, 416, phi, 416, 0.6),
            poly(
                [(mid - 7, 416), *arc(mid, 368, 7, 7, 180, 0, 6), (mid + 7, 416)],
                0.7,
                INK,
                o=0.7,
            ),
            _statue(mid, 311),
        ]
        for dx in (-19, 19):
            b.append(rect(mid + dx - 2.5, 338, 5, 78, 0.7, PAPER))

    # main block
    b += [
        rect(cx - 150, 300, 300, gy - 300, 1.3, PAPER),
        rect(cx - 150, 272, 300, 18, 0.9, PAPER),
        rect(cx - 154, 290, 308, 10, 1.0, PAPER),
        line(cx - 150, 410, cx + 150, 410, 0.8),
    ]
    for y in (416, 421.5, 427):
        b.append(line(cx - 150, y, cx + 150, y, 0.35))
    for i in range(75):
        x = cx - 148 + i * 4
        b.append(line(x, 276, x, 287, 0.35))
    for sx in (-1, 1):
        for i in range(4):
            x = cx + sx * (79 + i * 23.6)
            b.append(rect(x - 2.5, 300, 5, 110, 0.7, PAPER))
            b.append(_statue(x, 272))
        for i in range(3):
            x = cx + sx * (90.8 + i * 23.6)
            b.append(rect(x - 4.5, 370, 9, 28, 0.7, INK, o=0.7))
            b.append(poly([(x - 6.5, 366), (x, 361), (x + 6.5, 366)], 0.7))
            b.append(rect(x - 4, 318, 8, 13, 0.7, INK, o=0.7))

    # portico in front
    b.append(
        tone([(cx - 75, 306), (cx + 75, 306), (cx + 75, 410), (cx - 75, 410)], 0.22)
    )
    b.append(
        poly(
            [(cx - 9, 410), *arc(cx, 366, 9, 9, 180, 0, 8), (cx + 9, 410)],
            0,
            INK,
            o=0.75,
        )
    )
    for i in range(6):
        x = cx - 68 + i * 27.2
        b += [
            rect(x - 3.6, 312, 7.2, 96, 0.9, PAPER),
            rect(x - 5.2, 306, 10.4, 6, 0.8, PAPER),
            rect(x - 5, 407, 10, 3, 0.8, PAPER),
        ]
    b += [
        rect(cx - 79, 292, 158, 14, 1.1, PAPER),
        line(cx - 79, 299, cx + 79, 299, 0.4),
        poly([(cx - 84, 292), (cx, 257), (cx + 84, 292)], 1.3, PAPER),
        poly([(cx - 68, 288), (cx, 262), (cx + 68, 288)], 0.5),
        _statue(cx, 257),
        _statue(cx - 82, 292),
        _statue(cx + 82, 292),
    ]
    steps = [(cx - 75, 410), (cx + 75, 410), (cx + 94, gy), (cx - 94, gy)]
    b.append(poly(steps, 1.0, PAPER))
    for i in range(1, 5):
        y = 410 + i * 4.4
        half = 75 + 19 * (y - 410) / 22
        b.append(line(cx - half, y, cx + half, y, 0.4))
    for x, y in (
        (cx - 24, 419),
        (cx + 31, 423),
        (cx - 118, gy),
        (cx + 132, gy),
        (cx + 140, gy),
        (112, gy),
        (590, gy),
    ):
        b.append(person(x, y, 9))
    b.append(note(cx + 70, 200, "Low saucer dome", (cx + 22, 208)))
    write(
        "soane-royal-palace",
        "Royal Palace at Westminster — Soane, 1779",
        "elevation",
        "no dimensions specified",
        "".join(b),
    )


ALL = [newton_cenotaph, chaux, soane_royal_palace]
