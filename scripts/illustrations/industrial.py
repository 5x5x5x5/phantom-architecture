"""Part III — into the industrial."""

from __future__ import annotations

import itertools
import math

from .kit import (
    FAINT,
    INK,
    PAPER,
    Pt,
    arc,
    circle,
    dim_v,
    ground,
    hatch,
    line,
    note,
    path,
    person,
    poly,
    rect,
    reference,
    tone,
    write,
)  # fmt: skip

FLATIRON: list[Pt] = [(0, 15), (87, 15)]
TRAJAN: list[Pt] = [
    (0, 3.6), (5.5, 3.6), (5.5, 1.9), (34, 1.7), (34, 2.5), (35.5, 2.5),
    (35.5, 1.2), (38, 0.4),
]  # fmt: skip
TRIBUNE_BUILT: list[Pt] = [
    (0, 15), (8, 15), (8, 13.5), (100, 13.5), (100, 12), (112, 12),
    (112, 10), (128, 9.5), (128, 7), (137, 6), (141, 1.5),
]  # fmt: skip


def citta_nuova() -> None:
    """Sant'Elia's stepped block: the lifts stand outside it, bridged at every floor."""
    gy, fl, setb, floors = 432.0, 24.0, 10.0, 11
    face, back, podium = 300.0, 560.0, 370.0
    top = podium - floors * fl
    b = [ground(gy)]

    # a power station beyond, and the elevated road passing behind
    for x in (604, 630, 656):
        b.append(
            poly(
                [(x - 7, gy), (x - 4, 236), (x + 4, 236), (x + 7, gy)],
                0.6,
                PAPER,
                FAINT,
            )
        )
        b.append(line(x - 5, 244, x + 5, 244, 0.5, FAINT))
    b.append(poly([(578, gy), (590, 330), (676, 330), (684, gy)], 0.6, PAPER, FAINT))
    for x0, x1 in ((40, 236), (566, 684)):
        b.append(rect(x0, 386, x1 - x0, 6, 0.9, PAPER))
        b.append(line(x0, 381, x1, 381, 0.5))
        x = x0 + 6
        while x + 40 <= x1 + 2:
            b.append(path(f"M{x},{gy}V402a17,10 0 0 1 34,0V{gy}", 0.8))
            x += 38
    b += [
        rect(84, 371, 40, 10, 0.8, PAPER),
        line(104, 371, 110, 362, 0.6),
        line(84, 376, 124, 376, 0.4),
    ]

    body: list[Pt] = [(face - 14, gy), (face, podium)]
    for k in range(floors):
        x = face + k * setb
        body += [(x, podium - k * fl), (x, podium - (k + 1) * fl)]
    body += [(face + floors * setb, top), (back, top), (back, gy)]
    b.append(poly(body, 1.5, PAPER))
    b.append(
        hatch(
            [(back - 46, top), (back, top), (back, gy), (back - 46, gy)],
            3.2,
            60,
            o=0.38,
        )
    )
    for k in range(floors):
        x, y = face + k * setb, podium - k * fl
        b.append(line(x, y, back, y, 0.5))
        b.append(
            tone(
                [
                    (x + 5, y - 18),
                    (back - 52, y - 18),
                    (back - 52, y - 7),
                    (x + 5, y - 7),
                ],
                0.16,
            )
        )
        for i in range(int((back - 57 - x) / 8)):
            b.append(line(x + 9 + i * 8, y - 18, x + 9 + i * 8, y - 7, 0.4))
        b.append(line(x - setb, y - 5, x, y - 5, 0.6) if k else "")
    for i in range(1, 4):
        b.append(line(face - 14 + i * 3.5, gy - i * 15.5, back, gy - i * 15.5, 0.4))
    for x in (back - 46, back - 92, back - 138):
        b.append(rect(x - 4, top - 14, 8, 14, 0.9, PAPER))
    # rooftop sign frame and mast
    b.append(rect(444, top - 40, 70, 28, 0.8))
    for i in range(1, 7):
        b.append(line(444 + i * 10, top - 40, 444 + i * 10, top - 12, 0.4))
    b += [
        line(444, top - 26, 514, top - 26, 0.4),
        line(456, top - 12, 456, top, 0.8),
        line(502, top - 12, 502, top, 0.8),
    ]

    # the lift tower, cross-braced, with a bridge to each floor
    tx0, tx1, ttop = 236.0, 262.0, top - 22
    b.append(rect(tx0, ttop, tx1 - tx0, gy - ttop, 1.3, PAPER))
    y = gy
    while y - fl >= ttop:
        b.append(
            path(
                f"M{tx0},{y}L{tx1},{y - fl}M{tx1},{y}L{tx0},{y - fl}M{tx0},{y - fl}H{tx1}",
                0.4,
            )
        )
        y -= fl
    b += [
        rect(tx0 + 5, ttop - 8, tx1 - tx0 - 10, 8, 1.0, PAPER),
        line(249, ttop - 8, 249, ttop - 18, 0.8),
    ]
    for k in range(floors + 1):
        x, y = face + k * setb, podium - k * fl
        b.append(rect(tx1, y - 5, x - tx1, 5, 0.9, PAPER))
        if x - tx1 > 70:
            b.append(path(f"M{tx1},{y}l{(x - tx1) / 2},9l{(x - tx1) / 2},-9", 0.5))
    for x, y in (
        (284, podium - 5),
        (300, podium - 3 * fl - 5),
        (322, podium - 7 * fl - 5),
        (352, podium - 10 * fl - 5),
        (150, 381),
        (188, 381),
        (64, gy),
        (210, gy),
        (590, gy),
    ):
        b.append(person(x, y, 11))
    b += [
        note(48, 96, "Lift tower, standing free", (tx0 + 4, 150)),
        note(48, 196, "A bridge to every floor", (280, podium - 6 * fl - 2)),
        note(48, 330, "Elevated roadway + tram", (140, 381)),
    ]
    write(
        "citta-nuova",
        "Città Nuova — Sant'Elia, 1914",
        "elevation",
        "the casa a gradinata",
        "".join(b),
    )


def _bullet(
    cx: float, gy: float, h: float, w0: float, f: float = 1.0, k: int = 28
) -> list[Pt]:
    """One side of a parabolic tower, base to tip, at fraction ``f`` of its width."""
    return [(cx + f * w0 * math.sqrt(1 - i / k), gy - h * i / k) for i in range(k + 1)]


def hotel_attraction() -> None:
    """Gaudí's New York hotel: a cluster of parabolic towers about a taller one."""
    cx, gy = 330.0, 436.0
    b = [ground(gy)]
    for x, wd, h in (
        (52, 26, 22),
        (80, 20, 31),
        (102, 30, 18),
        (134, 18, 26),
        (508, 22, 28),
        (640, 24, 20),
        (666, 16, 30),
    ):
        b.append(rect(x, gy - h, wd, h, 0.6, PAPER, FAINT))
    towers = [
        (0.0, 336.0, 62.0),
        (-76, 214, 40),
        (76, 214, 40),
        (-134, 140, 33),
        (134, 140, 33),
        (0, 92, 46),
    ]
    for dx, h, w0 in towers:
        x = cx + dx
        b.append(
            poly(_bullet(x, gy, h, w0, -1) + _bullet(x, gy, h, w0)[::-1], 1.4, PAPER)
        )
        b.append(
            hatch(
                _bullet(x, gy, h, w0, 0.5) + _bullet(x, gy, h, w0)[::-1], 3, 62, o=0.4
            )
        )
        for f in (-0.66, -0.33, 0, 0.33, 0.66):
            b.append(poly(_bullet(x, gy, h, w0, f), 0.4, close=False, o=0.7))
        z = 14.0
        while z < h - 10:
            half = w0 * math.sqrt(1 - z / h)
            b.append(line(x - half, gy - z, x + half, gy - z, 0.35, o=0.7))
            for f in (-0.83, -0.5, -0.17, 0.17, 0.5, 0.83):
                b.append(rect(x + f * half - 1, gy - z + 3, 2, 5, 0, INK, o=0.6))
            z += 13
        if dx or h > 300:
            b.append(line(x, gy - h, x, gy - h - 8, 0.9))
            b.append(circle(x, gy - h - 10, 2.2, 0.8, PAPER))
    # the crowning star
    top = gy - 336 - 10
    b.append(circle(cx, top, 5, 1.0, PAPER))
    for deg in range(0, 360, 45):
        a = math.radians(deg)
        b.append(
            line(
                cx + 6 * math.cos(a),
                top - 6 * math.sin(a),
                cx + 11 * math.cos(a),
                top - 11 * math.sin(a),
                0.7,
            )
        )
    b.append(
        poly(
            [(cx - 12, gy), *arc(cx, gy - 30, 12, 14, 180, 0, 10), (cx + 12, gy)],
            0,
            INK,
            o=0.75,
        )
    )
    b.append(reference(585, gy, 1.0, FLATIRON, "Flatiron", "87 m"))
    for i in range(1, 21):
        b.append(line(570, gy - i * 4.2, 600, gy - i * 4.2, 0.3, FAINT))
    b.append(dim_v(530, gy - 357, gy, "360 m"))
    b.append(note(52, 150, "Star-shaped crown", (cx - 7, top)))
    write(
        "hotel-attraction",
        "Hotel Attraction — Gaudí, 1908",
        "elevation",
        "New York, as sketched",
        "".join(b),
    )


def tribune_column() -> None:
    """Loos's entry: a Doric column, inhabited, on an office-block plinth."""
    cx, gy = 360.0, 434.0
    b = [ground(gy)]

    def hw(t: float) -> float:
        return 40 - 7 * t**1.6  # entasis

    shaft_bot, shaft_top = 334.0, 164.0
    k = 34
    side = [
        (hw(i / k), shaft_bot - (shaft_bot - shaft_top) * i / k) for i in range(k + 1)
    ]
    b.append(
        poly(
            [(cx - w, y) for w, y in side] + [(cx + w, y) for w, y in side[::-1]],
            1.4,
            PAPER,
        )
    )
    b.append(
        hatch(
            [(cx + w * 0.5, y) for w, y in side] + [(cx + w, y) for w, y in side[::-1]],
            3,
            62,
            o=0.42,
        )
    )
    flutes = [math.sin(math.radians(d)) for d in range(-80, 81, 16)]
    for f in flutes:
        b.append(poly([(cx + f * w, y) for w, y in side], 0.45, close=False))
    # the giveaway: a window in every flute, floor after floor
    for floor in range(21):
        y = shaft_bot - 9 - floor * 7.8
        w = hw((shaft_bot - y) / (shaft_bot - shaft_top))
        for f0, f1 in itertools.pairwise(flutes):
            mid, span = (f0 + f1) / 2 * w, (f1 - f0) * w
            b.append(rect(cx + mid - span * 0.2, y, span * 0.4, 4.2, 0, INK, o=0.7))

    echinus = [
        (cx - 33, 158),
        (cx - 37, 150),
        (cx - 50, 142),
        (cx + 50, 142),
        (cx + 37, 150),
        (cx + 33, 158),
    ]
    b += [
        poly(echinus, 1.2, PAPER),
        rect(cx - 52, 129, 104, 13, 1.3, PAPER),
        rect(cx - 33, 158, 66, 6, 0.9, PAPER),
        line(cx - 33, 160, cx + 33, 160, 0.4),
        line(cx - 33, 162, cx + 33, 162, 0.4),
        rect(cx - 54, 338, 108, 4, 0.9, PAPER),
        rect(cx - 46, 334, 92, 4, 0.9, PAPER),
        rect(cx - 78, 342, 156, 92, 1.4, PAPER),
        rect(cx - 81, 342, 162, 5, 1.0, PAPER),
        hatch(
            [(cx + 50, 347), (cx + 78, 347), (cx + 78, gy), (cx + 50, gy)],
            3,
            62,
            o=0.35,
        ),
        line(cx - 78, 418, cx + 78, 418, 0.6),
    ]
    for row in range(9):
        for col in range(11):
            b.append(
                rect(cx - 69 + col * 13.2, 352 + row * 7.3, 6, 4.2, 0, INK, o=0.68)
            )
    b.append(rect(cx - 14, 419, 28, 15, 0, INK, o=0.8))
    for dx in (-6, 6):
        b.append(rect(cx + dx - 1.5, 419, 3, 15, 0, PAPER))
    for x in (cx - 40, cx + 30, cx + 104, cx - 120, 250, 470):
        b.append(person(x, gy, 4.5))
    b.append(reference(170, gy, 2.5, TRAJAN, "Trajan's Column", "38 m"))
    b.append(reference(575, gy, 2.5, TRIBUNE_BUILT, "Tribune Tower", "as built, 141 m"))
    for i in range(1, 30):
        b.append(
            line(575 - 33, gy - i * 8.2 - 16, 575 + 33, gy - i * 8.2 - 16, 0.3, FAINT)
        )
    b.append(dim_v(458, 129, gy, "c. 122 m"))
    b.append(note(210, 250, "Every flute", (cx - 30, 252), "end"))
    b.append(note(210, 259, "a column of windows", None, "end"))
    write(
        "tribune-column",
        "Chicago Tribune Column — Loos, 1922",
        "elevation",
        "competition entry",
        "".join(b),
    )


ALL = [citta_nuova, hotel_attraction, tribune_column]
