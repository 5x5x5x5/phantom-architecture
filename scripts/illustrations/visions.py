"""Part I — visions before modernity."""

from __future__ import annotations

import itertools
import math

from .kit import (
    ACCENT,
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
    quad,
    rect,
    reference,
    scale_bar,
    text,
    water,
    write,
)  # fmt: skip

ANTWERP_SPIRE: list[Pt] = [
    (0, 11), (58, 11), (58, 8), (88, 7), (88, 5), (106, 3.5), (123, 0.3),
]  # fmt: skip


def babel() -> None:
    """Bruegel's tower as a single rising ramp: ledges step on alternate sides."""
    cx, gy = 330.0, 432.0
    turn, step, lw, r0 = 44.0, 18.0, 12.0, 196.0  # px per turn / radius lost / ramp
    r = [r0 - k * step for k in range(8)]
    b = [ground(gy, 36, 548), water(gy, 548, 684)]

    left: list[Pt] = [(cx - r0, gy)]
    for k in range(6):
        left += [(cx - r[k] + lw, gy - k * turn), (cx - r[k + 1], gy - (k + 1) * turn)]
    left.append((cx - r[6] + lw, gy - 6 * turn))
    right: list[Pt] = [(cx + r0 - 3, gy), (cx + r0 - step / 2, gy - turn / 2)]
    for k in range(5):
        x = cx + r[k] - step / 2 - lw
        right += [(x, gy - (k + 0.5) * turn), (x - step + lw, gy - (k + 1.5) * turn)]
    right.append((cx + r[5] - step / 2 - lw, gy - 5.5 * turn))
    ruin: list[Pt] = [
        (cx - 72, gy - 292), (cx - 61, gy - 285), (cx - 52, gy - 301),
        (cx - 41, gy - 296), (cx - 30, gy - 311), (cx - 11, gy - 313),
        (cx - 2, gy - 303), (cx + 13, gy - 309), (cx + 24, gy - 296),
        (cx + 37, gy - 299), (cx + 45, gy - 283), (cx + 57, gy - 279),
        (cx + 68, gy - 266), (cx + 77, gy - 270),
    ]  # fmt: skip
    b.append(poly(left + ruin + right[::-1], 1.5, PAPER))
    shade = right + [(cx + (x - cx) * 0.55, y) for x, y in right[::-1]]
    b.append(hatch(shade, 3.2, 62, o=0.4))

    for k in range(7):
        y0, y1 = gy - k * turn, gy - (k + 0.5) * turn
        sag = 0.15 * r[k] if k else 0.0
        outer = ((cx - r[k], y0), (cx, (y0 + y1) / 2 + sag), (cx + r[k] - step / 2, y1))
        inner = (
            (cx - r[k] + lw, y0),
            (cx, (y0 + y1) / 2 + sag - 6),
            (cx + r[k] - step / 2 - lw, y1),
        )
        reach = 1.0 if k < 6 else 0.62  # the top ramp runs out into the ruin
        for curve, wt in ((outer, 1.1), (inner, 0.5)):
            p = [quad(*curve, t * reach / 20) for t in range(21)]
            b.append(poly(p, wt, close=False))
        # arcades: evenly spaced round the drum, so they crowd at the edges
        for deg in range(-72, 73, 12):
            t = 0.5 + 0.5 * math.sin(math.radians(deg))
            if t > reach - 0.08:
                continue
            x, y = quad(*inner, t)
            wd = max(2.0, 9.5 * math.cos(math.radians(deg)))
            arch = [
                (x - wd / 2, y - 1),
                *arc(x, y - 17, wd / 2, wd / 2, 180, 0, 6),
                (x + wd / 2, y - 1),
            ]
            b.append(poly(arch, 0, INK, o=0.62))
            b.append(rect(x - wd / 4, y - 31, wd / 2, 5, 0, INK, o=0.5))

    # the exposed inner core, and work still in progress
    for dx in (-22, -6, 12):
        b.append(line(cx + dx, gy - 300, cx + dx, gy - 272, 0.5, o=0.6))
    b.append(path(f"M{cx - 22},{gy - 284}q8,-9 16,0q9,-9 18,0", 0.5, o=0.6))
    for x, y in ((cx - 128, gy - 132), (cx + 92, gy - 198), (cx - 84, gy - 220)):
        b.append(path(f"M{x},{y}v-13l9,4M{x},{y - 13}l-4,5", 0.6))

    for x, y, wd in ((104, 190, 58), (518, 232, 70), (84, 262, 40)):
        b.append(
            path(
                f"M{x},{y}q{wd / 4},-7 {wd / 2},-1q{wd / 4},-6 {wd / 2},1", 0.5, c=FAINT
            )
        )

    b.append(reference(74, gy, 0.62, ANTWERP_SPIRE, "Antwerp", "cathedral", "123 m"))
    for i in range(4):
        x = 96 + i * 9
        b.append(
            poly(
                [(x, gy), (x, gy - 5), (x + 4, gy - 9), (x + 8, gy - 5), (x + 8, gy)],
                0.6,
                PAPER,
                FAINT,
            )
        )
    for x, sz in ((600, 1.0), (652, 0.75)):
        b.append(path(f"M{x - 11 * sz},{gy - 3}q{11 * sz},7 {22 * sz},0z", 0.7, PAPER))
        b.append(path(f"M{x},{gy - 3}v{-20 * sz}l{9 * sz},{14 * sz}h{-9 * sz}", 0.6))
    b.append(dim_v(562, gy - 313, gy, "c. 500 m as painted"))
    write(
        "babel",
        "The Tower of Babel — Bruegel, 1563",
        "elevation",
        "after the Vienna panel",
        "".join(b),
    )


def sforzinda() -> None:
    """Filarete's star: two squares overlaid, inscribed in a circular moat."""
    cx, cy, rr = 360.0, 256.0, 168.0
    ri = rr * math.cos(math.radians(45)) / math.cos(math.radians(22.5))

    def at(deg: float, rad: float) -> Pt:
        a = math.radians(deg)
        return (cx + rad * math.cos(a), cy - rad * math.sin(a))

    star = [at(22.5 * i, rr if i % 2 == 0 else ri) for i in range(16)]
    b = [
        circle(cx, cy, rr + 11, 1.0, INK, o=0.16),
        circle(cx, cy, rr + 11, 1.0),
        circle(cx, cy, rr + 1, 0.8, PAPER),
        hatch(arc(cx, cy, rr, rr, 0, 360, 48), 5, 30, o=0.28),
        poly(star, 1.8, PAPER),
        poly([at(22.5 * i, (rr if i % 2 == 0 else ri) * 0.94) for i in range(16)], 0.6),
    ]
    for off in (0, 45):
        b.append(
            poly([at(off + 90 * i, rr) for i in range(4)], 0.4, c=FAINT, dash="3 3")
        )
    for frac in (0.3, 0.52):
        b.append(poly([at(22.5 * i, rr * frac) for i in range(16)], 0.6))
    for i in range(16):
        tower = i % 2 == 0
        end = at(22.5 * i, (rr if tower else ri) * 0.94)
        b.append(line(*at(22.5 * i, 24), *end, 0.5 if tower else 0.9))
        px, py = at(22.5 * i, rr * 0.52)
        if tower:
            b.append(circle(px, py, 4.2, 0.8, PAPER))
            b.append(circle(*at(22.5 * i, rr), 5.5, 1.3, PAPER))
        else:
            b.append(rect(px - 4.5, py - 4.5, 9, 9, 0.8, PAPER))
            b.append(circle(*at(22.5 * i, ri), 3.2, 0, INK))
    b += [
        rect(cx - 21, cy - 11, 42, 22, 1.1, PAPER),
        rect(cx - 8, cy - 27, 16, 14, 0.9, PAPER),
        rect(cx - 8, cy + 13, 16, 14, 0.9, PAPER),
        rect(cx - 3, cy - 3, 6, 6, 0, ACCENT),
        note(566, 112, "Tower, at each point", at(45, rr)),
        note(566, 190, "Gate, at each angle", at(22.5, ri)),
        note(566, 330, "Moat", at(-33, rr + 6)),
        note(154, 112, "Sixteen radial streets", at(135, rr * 0.72), "end"),
        note(154, 300, "Market + parish squares", at(180, rr * 0.52), "end"),
        note(154, 392, "Central piazzas", (cx - 21, cy + 8), "end"),
        text(cx, cy + rr + 34, "House of Virtue and Vice at the centre", 6.5, "middle"),
        scale_bar(48, 440, 102, "1 km"),
    ]
    write("sforzinda", "Sforzinda — Filarete, 1457–1464", "plan", "", "".join(b))


def ideal_city() -> None:
    """Leonardo's two-level city, cut across a street and its canal."""
    deck, floor = 318.0, 404.0
    piers = [130.0, 200, 270, 320, 400, 450, 520, 590]
    b = [ground(floor, 112, 327), ground(floor, 393, 684)]

    # the far side of the street, seen in elevation beyond the cut
    for i in range(5):
        x = 284 + i * 38
        b.append(
            path(f"M{x - 13},{deck}V{deck - 30}a13,13 0 0 1 26,0V{deck}", 0.5, c=FAINT)
        )
        for y in (250, 214):
            b.append(rect(x - 5, y, 10, 16, 0.5, c=FAINT))
    b.append(line(270, 190, 450, 190, 0.5, FAINT))
    b.append(line(270, 268, 450, 268, 0.5, FAINT))

    # the cut structure: one slab of masonry, vaults scooped out of it
    slab = [(124, deck), (596, deck), (596, floor), (124, floor)]
    b += [poly(slab, 0, PAPER), hatch(slab, 3, 45, o=0.7), poly(slab, 1.4)]
    for xa, xb in itertools.pairwise(piers):
        x0, x1 = xa + 6, xb - 6
        rx = (x1 - x0) / 2
        b.append(
            path(f"M{x0},{floor}V372A{rx},{rx} 0 0 1 {x1},372V{floor}z", 1.2, PAPER)
        )
    b += [
        rect(327, floor, 66, 26, 0, PAPER),
        path(f"M327,{floor}v26h66v-26", 1.2),
        line(327, 412, 393, 412, 0.7),
        path("M333,417h10M352,420h12M372,417h9M340,424h8M366,425h10", 0.4, c=FAINT),
        path("M338,412q22,9 44,0z", 0.8, PAPER),
        person(371, 410, 17),
        line(378, 392, 388, 426, 0.6),
    ]

    # houses in section either side of the upper street
    for sx in (1, -1):

        def m(x: float, _sx: int = sx) -> float:
            return x if _sx == 1 else 720 - x

        b += [
            line(m(128), deck, m(128), 178, 3),
            line(m(226), deck, m(226), 178, 1.6),
            line(m(266), 264, m(266), 178, 3),
            line(m(266), deck, m(266), 270, 2.4),
            path(
                f"M{m(226)},{deck - 34}A20,20 0 0 {1 if sx == 1 else 0} {m(266)},{deck - 34}",
                1.0,
            ),
            rect(m(266) - 4, 264, 8, 6, 0.8, INK),
            poly([(m(118), 178), (m(197), 142), (m(276), 178)], 1.5, PAPER),
            hatch([(m(118), 178), (m(197), 142), (m(276), 178)], 3.5, 0, o=0.35),
        ]
        for y in (264, 221):
            b.append(line(m(128), y, m(266), y, 1.4))
        b.append(person(m(246), deck, 17))

    for x in (296, 306, 372, 418):
        b.append(person(x, deck, 17))
    b += [
        rect(150, 384, 30, 9, 0.9, PAPER),
        circle(158, 397, 6.5, 0.9, PAPER),
        line(180, 388, 194, 388, 0.8),
        person(188, floor, 17),
        circle(476, 398, 5.5, 0.8, PAPER),
        circle(488, 398, 5.5, 0.8, PAPER),
        circle(482, 388, 5.5, 0.8, PAPER),
        person(502, floor, 17),
        person(560, floor, 17),
        line(88, deck, 122, deck, 0.5, FAINT),
        text(40, deck - 5, "Upper level"),
        text(40, deck + 9, "on foot"),
        line(88, floor, 122, floor, 0.5, FAINT),
        text(40, floor - 5, "Lower level"),
        text(40, floor + 9, "carts, trade"),
        note(410, 446, "Service canal", (388, 424)),
    ]
    write(
        "ideal-city",
        "Ideal City — Leonardo da Vinci, c. 1487",
        "cross-section",
        "after Paris MS B",
        "".join(b),
    )


ALL = [babel, sforzinda, ideal_city]
