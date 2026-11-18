"""Part VI — monuments of power."""

from __future__ import annotations

import math

from .kit import (
    EIFFEL,
    FAINT,
    INK,
    PAPER,
    ST_PETERS,
    Pt,
    arc,
    circle,
    dim_v,
    ground,
    hatch,
    line,
    note,
    path,
    poly,
    rect,
    reference,
    text,
    tone,
    write,
)  # fmt: skip

LIBERTY: list[Pt] = [
    (0, 11), (5, 11), (5, 8), (22, 8), (22, 6.5), (46, 5.5), (47, 3.8),
    (74, 3.8), (79, 2), (86, 2), (86, 0.9), (93, 0.3),
]  # fmt: skip


def palace_of_soviets() -> None:
    """Iofan's telescoping drums, with a hundred-metre Lenin for a finial."""
    cx, gy, s = 360.0, 434.0, 0.86
    b = [ground(gy)]

    y = gy - 56
    b.append(rect(cx - 150, y, 300, 56, 1.4, PAPER))
    b.append(
        hatch(
            [(cx + 110, y), (cx + 150, y), (cx + 150, gy), (cx + 110, gy)],
            3,
            62,
            o=0.38,
        )
    )
    for i in range(31):
        b.append(line(cx - 150 + i * 10, y + 7, cx - 150 + i * 10, gy, 0.45))
    b.append(rect(cx - 153, y, 306, 7, 1.0, PAPER))
    b.append(
        tone([(cx - 34, y + 12), (cx + 34, y + 12), (cx + 34, gy), (cx - 34, gy)], 0.3)
    )
    for i in range(7):
        b.append(rect(cx - 32 + i * 10 - 1.8, y + 12, 3.6, 44, 0, PAPER))
    stair = [(cx - 40, gy - 9), (cx + 40, gy - 9), (cx + 52, gy), (cx - 52, gy)]
    b.append(poly(stair, 0.9, PAPER))
    for i in (3, 6):
        b.append(
            line(cx - 40 - i * 1.3, gy - 9 + i, cx + 40 + i * 1.3, gy - 9 + i, 0.4)
        )

    for hw, h in ((105, 48), (85, 46), (66, 44), (50, 40), (36, 26)):
        top = y - h
        b.append(rect(cx - hw, top, 2 * hw, h, 1.3, PAPER))
        b.append(
            hatch(
                [
                    (cx + hw * 0.62, top),
                    (cx + hw, top),
                    (cx + hw, y),
                    (cx + hw * 0.62, y),
                ],
                3,
                62,
                o=0.4,
            )
        )
        for deg in range(-80, 81, 10):
            x = cx + hw * math.sin(math.radians(deg))
            b.append(line(x, top + 6, x, y, 0.5))
        b.append(rect(cx - hw - 3, top, 2 * hw + 6, 5, 0.9, PAPER))
        for sx in (-1, 1):
            b.append(rect(cx + sx * (hw + 8) - 4, y - 12, 8, 12, 0.8, PAPER))
        y = top
    b.append(rect(cx - 20, y - 11, 40, 11, 1.1, PAPER))
    feet = y - 11

    # Lenin, one arm raised
    k = 86 / 84
    coat = [
        (-9, 0),
        (9, 0),
        (10, 30),
        (11, 55),
        (13, 66),
        (6, 70),
        (-6, 70),
        (-12, 66),
        (-10, 55),
        (-10, 30),
    ]
    b.append(poly([(cx + px * k, feet - py * k) for px, py in coat], 0, INK, o=0.88))
    b.append(circle(cx + 1, feet - 77 * k, 6 * k, 0, INK, o=0.88))
    arm = [
        (cx + 11 * k, feet - 64 * k),
        (cx + 24 * k, feet - 71 * k),
        (cx + 35 * k, feet - 83 * k),
    ]
    b.append(poly(arm, 5, c=INK, close=False, o=0.88))
    head = feet - 84 * k

    b.append(reference(602, gy, s, EIFFEL, "Eiffel Tower", "330 m"))
    b.append(reference(108, gy, s, LIBERTY, "Statue of Liberty", "93 m"))
    b.append(dim_v(530, head, gy, "415 m"))
    b.append(dim_v(cx - 60, head, feet, "Lenin, 100 m", side=-1))
    write(
        "palace-of-soviets",
        "Palace of the Soviets — Iofan, 1933",
        "elevation",
        "",
        "".join(b),
    )


def _brandenburg(x: float, gy: float, s: float) -> str:
    """The Brandenburg Gate, 26 m high: six piers, an attic, the quadriga."""
    hw = 32.5 * s
    out = rect(x - hw, gy - 20 * s, 2 * hw, 4 * s, 0.7, PAPER, FAINT)
    out += rect(x - hw * 0.5, gy - 23 * s, hw, 3 * s, 0.7, PAPER, FAINT)
    out += path(f"M{x - 4},{gy - 23 * s}l4,-4l4,4", 0.7, c=FAINT)
    for i in range(6):
        px = x - hw + 3 + i * (2 * hw - 6) / 5
        out += line(px, gy - 16 * s, px, gy, 1.4, FAINT)
    return out


def volkshalle() -> None:
    """Speer's Great Hall: a dome that would have swallowed St Peter's whole."""
    cx, gy, s = 345.0, 434.0, 1.15
    spring = 316.0
    rx, ry = 144.0, 169.0
    b = [ground(gy)]

    b.append(poly(arc(cx, spring, rx, ry, 180, 0, 48), 1.6, PAPER))
    b.append(
        hatch(
            arc(cx, spring, rx, ry, 0, 84) + arc(cx, spring, rx * 0.6, ry, 84, 0),
            3.2,
            62,
            o=0.4,
        )
    )
    for f in (-0.86, -0.62, -0.32, 0, 0.32, 0.62, 0.86):
        b.append(poly(arc(cx, spring, rx * f, ry, 0, 90, 20), 0.4, close=False, o=0.75))
    for i in range(1, 7):
        z = ry * i / 7
        half = rx * math.sqrt(1 - (z / ry) ** 2)
        b.append(
            path(
                f"M{cx - half:.1f},{spring - z:.1f}Q{cx},{spring - z + 0.13 * half:.1f} {cx + half:.1f},{spring - z:.1f}",
                0.35,
                o=0.75,
            )
        )

    # lantern, with the eagle on its globe
    lt = spring - ry
    b += [
        rect(cx - 13, lt - 34, 26, 40, 1.0, PAPER),
        poly(arc(cx, lt - 34, 15, 8, 180, 0, 10), 1.0, PAPER),
        circle(cx, lt - 46, 3.2, 0.8, PAPER),
        path(f"M{cx - 9},{lt - 53}q5,-1 9,3q4,-4 9,-3", 0.9),
    ]
    for dx in (-8, -3, 3, 8):
        b.append(line(cx + dx, lt - 30, cx + dx, lt + 2, 0.5))

    b.append(rect(cx - 152, spring, 304, 33, 1.2, PAPER))
    for deg in range(-84, 85, 6):
        x = cx + 150 * math.sin(math.radians(deg))
        b.append(line(x, spring + 6, x, spring + 33, 0.6))
    b.append(rect(cx - 155, spring, 310, 5, 0.9, PAPER))

    base = 349.0
    b.append(rect(cx - 181, base, 362, gy - base, 1.5, PAPER))
    b.append(
        hatch(
            [(cx + 140, base), (cx + 181, base), (cx + 181, gy), (cx + 140, gy)],
            3.2,
            62,
            o=0.38,
        )
    )
    for i in range(27):
        x = cx - 181 + i * 13.92
        if abs(x - cx) > 84:
            b.append(line(x, base + 10, x, gy, 0.5))
    b.append(
        tone(
            [
                (cx - 78, base + 13),
                (cx + 78, base + 13),
                (cx + 78, gy - 5),
                (cx - 78, gy - 5),
            ],
            0.3,
        )
    )
    for i in range(12):
        b.append(rect(cx - 74.5 + i * 13.1, base + 13, 5, gy - base - 18, 0, PAPER))
    b += [
        rect(cx - 84, base + 3, 168, 10, 1.0, PAPER),
        rect(cx - 184, base, 368, 7, 1.0, PAPER),
        rect(cx - 90, gy - 5, 180, 5, 0.8, PAPER),
        line(cx - 87, gy - 2.5, cx + 87, gy - 2.5, 0.4),
    ]
    for sx in (-1, 1):
        x = cx + sx * 181
        b += [
            rect(x - 13, 306, 26, gy - 306, 1.4, PAPER),
            rect(x - 15, 300, 30, 6, 1.0, PAPER),
            line(x, 300, x, 291, 1.0),
            circle(x, 288, 2.6, 0.8, PAPER),
        ]
        for dx in (-6, 0, 6):
            b.append(line(x + dx, 312, x + dx, gy, 0.4))

    b.append(reference(615, gy, s, ST_PETERS, "St Peter's, Rome", "136 m"))
    b.append(_brandenburg(84, gy, s))
    b.append(text(84, gy - 26 * s - 14, "Brandenburg Gate", 6, "middle"))
    b.append(text(84, gy - 26 * s - 6, "26 m", 6, "middle"))
    b.append(dim_v(140, lt - 54, gy, "290 m", side=-1))
    b.append(note(52, 110, "Dome: 250 m clear span", (cx - 96, 196)))
    b.append(note(52, 119, "room for 180,000 standing"))
    write(
        "volkshalle", "Volkshalle / Germania — Speer, 1937", "elevation", "", "".join(b)
    )


ALL = [palace_of_soviets, volkshalle]
