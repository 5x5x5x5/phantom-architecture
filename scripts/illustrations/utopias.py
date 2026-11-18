"""Part VII — post-war utopias."""

from __future__ import annotations

import math
import random

from .kit import (
    EMPIRE,
    FAINT,
    INK,
    PAPER,
    Pt,
    arc,
    box,
    circle,
    dim_h,
    dim_v,
    ground,
    hatch,
    line,
    n,
    note,
    path,
    person,
    poly,
    profile,
    quad,
    rect,
    scale_bar,
    text,
    tone,
    water,
    write,
)  # fmt: skip

CHRYSLER: list[Pt] = [
    (0, 30), (200, 30), (200, 24), (258, 18), (290, 8), (319, 0.5),
]  # fmt: skip


def dome_over_manhattan() -> None:
    """Fuller's two-mile dome, drawn river to river over Midtown."""
    cx, gy, s = 360.0, 428.0, 0.2
    rx, ry = 290.0, 320.0
    rng = random.Random(1960)
    b = [ground(gy, 70, 650), water(gy, 36, 70, 2), water(gy, 650, 684, 2)]

    x = 78.0
    while x < 640:
        wd = rng.uniform(6, 13)
        reach = max(0.0, 1 - abs(x - cx) / 290)
        hgt = rng.uniform(0.25, 1) * (55 + 200 * reach**1.4) * s
        b.append(rect(x, gy - hgt, wd, hgt, 0.6, PAPER))
        x += wd + rng.uniform(-1, 2.5)
    b.append(poly(profile(cx - 46, gy, s, EMPIRE), 0.9, PAPER))
    b.append(poly(profile(cx + 62, gy, s, CHRYSLER), 0.9, PAPER))

    # geodesic net: ring k from the apex carries 6k nodes
    rings = 11

    def node(k: int, j: int) -> tuple[float, float, float]:
        if k == 0:
            return (cx, gy - ry, 1.0)
        th = math.radians(90 * k / rings)
        lon = math.tau * j / (6 * k) + 0.3
        return (
            cx + rx * math.sin(th) * math.cos(lon),
            gy - ry * math.cos(th),
            math.sin(lon),
        )

    d = ""

    def edge(p: tuple[float, float, float], q: tuple[float, float, float]) -> str:
        if p[2] < -0.02 or q[2] < -0.02:
            return ""
        return f"M{n(p[0])},{n(p[1])}L{n(q[0])},{n(q[1])}"

    for j in range(6):
        d += edge(node(0, 0), node(1, j))
    for k in range(1, rings + 1):
        for j in range(6 * k):
            d += edge(node(k, j), node(k, (j + 1) % (6 * k)))
        if k == rings:
            break
        for m in range(6):
            for i in range(k):
                up = node(k, m * k + i)
                d += edge(up, node(k + 1, m * (k + 1) + i))
                d += edge(up, node(k + 1, m * (k + 1) + i + 1))
            d += edge(node(k, (m * k + k) % (6 * k)), node(k + 1, m * (k + 1) + k))
    b.append(path(d, 0.35, o=0.6))
    b.append(poly(arc(cx, gy, rx, ry, 180, 0, 64), 1.7, close=False))

    b += [
        dim_h(cx - rx, cx + rx, gy + 27, "c. 3 km, river to river"),
        dim_v(672, gy - ry, gy, "1.6 km", side=-1),
        note(52, 100, "Empire State, 443 m", (cx - 46, gy - 443 * s)),
        text(34, gy + 15, "Hudson", 6),
        text(686, gy + 15, "East River", 6, "end"),
    ]
    write(
        "dome-over-manhattan",
        "Dome over Manhattan — Buckminster Fuller, 1960",
        "elevation",
        "",
        "".join(b),
    )


def _a_frame(x: float, by: float, wd: float, h: float, bed: float, near: bool) -> str:
    """One of Tange's tent-roofed housing frames, standing in the bay."""
    c = INK if near else FAINT

    def side(sx: int, k: float) -> list[Pt]:
        ctrl = (
            (x, by - h * k),
            (x + sx * wd * 0.1 * k, by - h * 0.34 * k),
            (x + sx * wd / 2 * k, by),
        )
        return [quad(*ctrl, i / 12) for i in range(13)]

    out = ""
    for px in (-0.44, -0.15, 0.15, 0.44):
        out += rect(x + px * wd - 2, by, 4, bed - by, 0.7, PAPER, c)
    out += poly(side(-1, 1) + side(1, 1)[::-1], 1.4 if near else 0.7, PAPER, c)
    out += rect(x - wd / 2 - 6, by, wd + 12, 4, 0.9 if near else 0.6, PAPER, c)
    if not near:
        return out
    out += poly(side(-1, 0.6) + side(1, 0.6)[::-1], 0.7, PAPER)
    out += hatch(side(1, 1) + side(1, 0.6)[::-1], 2.8, 62, o=0.4)
    for sx in (-1, 1):
        for px, py in side(sx, 1)[2:-1]:
            out += line(px, py, px - sx * 1, py, 0.5)
            out += rect(px + (0 if sx == 1 else -6), py - 3.5, 6, 3.5, 0, INK, o=0.75)
            out += line(px - sx * 7, py, px + sx * 6, py, 0.5)
    for frac in (0.3, 0.55):
        half = wd / 2 * 0.6 * (1 - frac) * 0.8
        out += line(x - half, by - h * 0.6 * frac, x + half, by - h * 0.6 * frac, 0.6)
    return out


def tokyo_bay() -> None:
    """Tange's plan in section: a civic spine, and housing out over the water."""
    wl, bed, cx = 386.0, 428.0, 360.0
    b = [ground(bed)]
    for x in (84, 206, 514, 636):
        b.append(_a_frame(x, wl - 6, 104, 112, bed, near=False))
    b.append(water(wl, 36, 684, 2))
    for x in (140, 580):
        b.append(_a_frame(x, wl - 8, 150, 158, bed, near=True))

    # the civic axis: service cores with office slabs bridging between them
    for x in (250, 470):
        b.append(rect(x - 2.5, 356, 5, bed - 356, 0.8, PAPER))
    for x in (292, 360, 428):
        b.append(rect(x - 7, 196, 14, bed - 196, 1.3, PAPER))
        b.append(
            hatch(
                [(x + 1, 196), (x + 7, 196), (x + 7, bed), (x + 1, bed)],
                2.6,
                62,
                o=0.45,
            )
        )
        b.append(rect(x - 9, 190, 18, 6, 1.0, PAPER))
    for x0, x1, y, h in (
        (299, 353, 228, 30),
        (367, 421, 266, 30),
        (299, 353, 304, 22),
        (367, 421, 312, 20),
    ):
        b.append(rect(x0, y, x1 - x0, h, 1.1, PAPER))
        for i in range(1, int((x1 - x0) / 4.5)):
            b.append(line(x0 + i * 4.5, y + 3, x0 + i * 4.5, y + h - 3, 0.35))
        b.append(line(x0, y + h / 2, x1, y + h / 2, 0.4))
    for y, x0, x1 in ((350, 226, 494), (366, 244, 476)):
        b.append(rect(x0, y, x1 - x0, 5.5, 1.1, PAPER))
        for i in range(7):
            b.append(rect(x0 + 14 + i * (x1 - x0 - 30) / 6, y - 2.6, 5, 2.6, 0, INK))
    for sx in (-1, 1):
        b.append(line(cx + sx * 134, 353, cx + sx * 147, wl - 8, 1.0))
        b.append(line(cx + sx * 134, 358, cx + sx * 141, wl - 8, 0.6))
    for x, k in ((48, 1.0), (668, 0.8)):
        b.append(path(f"M{x - 10 * k},{wl - 2}q{10 * k},7 {20 * k},0z", 0.7, PAPER))
        b.append(path(f"M{x},{wl - 2}v{-16 * k}l{8 * k},{11 * k}h{-8 * k}", 0.6))
    b += [
        note(52, 96, "Housing frames: terraced without,", (140 - 46, 300)),
        note(52, 105, "hollow within"),
        note(470, 96, "Civic axis: service cores, with", (435, 214)),
        note(470, 105, "offices bridging between them"),
        note(470, 150, "Looped motorway, on piers", (486, 351)),
        text(304, 414, "Tokyo Bay", 6.5),
        scale_bar(48, 446, 100, "100 m"),
    ]
    write(
        "tokyo-bay",
        "Tokyo Bay Plan — Kenzō Tange, 1960",
        "cross-section",
        "",
        "".join(b),
    )


def fun_palace() -> None:
    """Price's kit of parts: a frame, a crane, and floors hung wherever wanted."""
    gy, top, bay = 432.0, 200.0, 96.0
    xs = [90 + k * bay for k in range(6)]
    brk = 652.0
    b = [ground(gy)]

    # floors, each hung from the roof beams on rods
    decks = [
        (90, 186, 362),
        (90, 150, 292),
        (186, 282, 332),
        (282, 378, 382),
        (378, 474, 372),
        (378, 474, 302),
        (474, 570, 342),
        (522, 570, 246),
        (570, brk, 362),
    ]
    for x0, x1, y in decks:
        for hx in (x0 + 12, x1 - 12):
            b.append(line(hx, top, hx, y, 0.35, o=0.7))
        b.append(rect(x0, y, x1 - x0, 4, 1.0, PAPER))
    # what happens to be plugged in this week
    b += [
        rect(104, 328, 56, 34, 1.0, PAPER),
        hatch([(104, 328), (160, 328), (160, 362), (104, 362)], 3.2, 62, o=0.35),
        poly([(194, 332), (274, 300), (274, 332)], 1.0, PAPER),
        rect(192, 268, 86, 64, 0.7, dash="4 3"),
        line(198, 280, 198, 322, 1.6),
        poly(
            [(318, 382), *arc(348, 382, 30, 24, 180, 0, 16), (378, 382)],
            0.9,
            PAPER,
            dash="2 2.5",
        ),
        rect(398, 262, 56, 40, 1.0, PAPER),
        hatch([(398, 262), (454, 262), (454, 302), (398, 302)], 3.2, 118, o=0.35),
        path("M388,372L462,302M394,372L468,302", 1.0),
        rect(488, 262, 6, 76, 0.8, PAPER),
        hatch([(488, 262), (494, 262), (494, 338), (488, 338)], 2.2, 0, o=0.6),
        path("M580,362L640,300M586,362L646,300", 1.0),
    ]
    for i in range(1, 7):
        b.append(
            line(
                274 - i * 11.4,
                332 - i * 4.6,
                274 - i * 11.4 + 3,
                332 - i * 4.6 - 5,
                0.8,
            )
        )
    for x0 in (378, 474):
        b.append(
            path(
                f"M{x0 + 8},{top + 5}q{bay / 2 - 8},15 {bay - 16},0",
                0.6,
                c=FAINT,
                dash="5 3",
            )
        )

    # the frame
    b.append(rect(90, top, brk - 90, 5, 1.2, PAPER))
    b.append(line(90, top - 6, brk, top - 6, 0.9))
    for x in xs:
        b.append(rect(x - 7, top, 14, gy - top, 1.1, PAPER))
        y = gy
        while y - 19.3 >= top - 0.5:
            b.append(
                path(
                    f"M{x - 7},{y}L{x + 7},{y - 19.3}M{x + 7},{y}L{x - 7},{y - 19.3}M{x - 7},{y - 19.3}h14",
                    0.4,
                )
            )
            y -= 19.3
    b.append(rect(brk - 4, top - 14, 60, gy - top + 14, 0, PAPER))
    b.append(path(f"M{brk - 4},{top - 12}V280l-6,9l12,10l-6,9V{gy}", 0.8))

    # the gantry crane, moving a room
    b += [
        rect(300, top - 22, 60, 13, 1.2, PAPER),
        circle(308, top - 8, 2.4, 0.8, PAPER),
        circle(352, top - 8, 2.4, 0.8, PAPER),
        rect(344, top - 9, 13, 10, 0.9, PAPER),
        line(318, top - 9, 318, 236, 0.5),
        line(340, top - 9, 340, 236, 0.5),
        rect(306, 236, 46, 30, 1.2, PAPER),
        tone([(306, 236), (352, 236), (352, 266), (306, 266)], 0.14),
        path("M358,250h30m-5,-3.5l5,3.5l-5,3.5", 0.6, c=FAINT, dash="3 2"),
        rect(520, top - 18, 30, 9, 1.0, PAPER),
        line(535, top - 9, 535, 226, 0.5),
    ]
    for x, y in (
        (112, 292),
        (132, 292),
        (172, 362),
        (178, 362),
        (210, 332),
        (300, 382),
        (360, 382),
        (420, 372),
        (446, 372),
        (410, 302),
        (506, 342),
        (552, 342),
        (540, 246),
        (600, 362),
        (60, gy),
        (140, gy),
        (150, gy),
        (236, gy),
        (330, gy),
        (430, gy),
        (440, gy),
        (520, gy),
        (604, gy),
        (672, gy),
        (425, 337),
        (613, 331),
    ):
        b.append(person(x, y, 8.1))
    b += [
        dim_v(64, top, gy, "15 storeys", side=-1),
        note(52, 96, "Gantry crane, running the full length", (304, top - 18)),
        note(52, 134, "Floors hung on rods, re-hung to order", (102, 250)),
        note(470, 96, "Frame runs on: c. 200 m in all", (brk - 2, 262)),
        note(470, 134, "A room in transit", (354, 240)),
    ]
    write(
        "fun-palace",
        "Fun Palace — Cedric Price, 1961",
        "elevation, part",
        "",
        "".join(b),
    )


def _leg(top: Pt, foot: Pt, widths: tuple[float, float, float], c: str = INK) -> str:
    """A telescoping leg: three tubes of shrinking bore, a collar at each joint."""
    out = ""
    cuts = (0.0, 0.38, 0.72, 1.0)
    ang = math.degrees(math.atan2(-(foot[1] - top[1]), foot[0] - top[0]))
    for i, wd in enumerate(widths):
        p = (
            top[0] + (foot[0] - top[0]) * cuts[i],
            top[1] + (foot[1] - top[1]) * cuts[i],
        )
        q = (
            top[0] + (foot[0] - top[0]) * cuts[i + 1],
            top[1] + (foot[1] - top[1]) * cuts[i + 1],
        )
        ln = math.hypot(q[0] - p[0], q[1] - p[1])
        out += poly(
            box((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, ln, wd, ang), 1.1, PAPER, c
        )
        out += poly(box(q[0], q[1], 4, wd + 4, ang), 0.9, PAPER, c)
    out += poly(arc(foot[0], foot[1], 13, 4, 0, 180, 10), 1.1, PAPER, c)
    return out


def _walker() -> str:
    """One walking city, drawn about its own origin: hull centre (0, 0), ground at 174."""
    rx, up, dn, gy = 150.0, 62.0, 46.0, 174.0
    hull = arc(0, 0, rx, up, 0, 180, 30) + arc(0, 0, rx, dn, 180, 360, 30)
    out = ""
    for (ax, ay), fx in (
        ((-92, 26), -112),
        ((-30, 38), -22),
        ((44, 38), 82),
        ((100, 26), 168),
    ):
        out += _leg((ax + 14, ay), (fx + 14, gy), (11, 8, 5), FAINT)
    # service tubes let down from the belly
    for x, reach in ((-58, 60), (8, 128), (70, 46)):
        out += rect(x - 4, 30, 8, reach * 0.5, 0.8, PAPER)
        out += rect(x - 2.5, 30 + reach * 0.5, 5, reach * 0.5, 0.8, PAPER)
    # pop-up units and masts on the back
    for x, h in ((-64, 14), (-18, 20), (34, 16)):
        y = -up * math.sqrt(1 - (x / rx) ** 2)
        out += poly(
            [
                (x - 9, y + 4),
                (x - 9, y - h + 5),
                *arc(x, y - h + 5, 9, 6, 180, 0, 8),
                (x + 9, y - h + 5),
                (x + 9, y + 4),
            ],
            1.0,
            PAPER,
        )
        out += line(x, y - h - 1, x, y - h - 18, 0.7)
    out += path("M-18,-99l26,-9M8,-108v9", 0.7)
    out += poly(hull, 1.6, PAPER)
    out += hatch(
        arc(0, 0, rx, dn, 180, 360, 30) + arc(0, -16, rx, dn - 12, 360, 180, 30),
        3,
        62,
        o=0.42,
    )
    out += path(f"M{-rx},0Q0,20 {rx},0", 0.8)
    for f in (-0.78, -0.52, -0.24, 0.06, 0.36, 0.62):
        x = rx * f
        k = math.sqrt(1 - f * f)
        out += path(
            f"M{n(x)},{n(-up * k)}Q{n(x + 9 * f + 4)},0 {n(x)},{n(dn * k)}", 0.6
        )
    for i in range(19):
        x = -126 + i * 12.4
        if x < 78:
            y = 20 * (1 - (x / rx) ** 2) * 0.5
            out += circle(x, y - 14, 2.6, 0.7, PAPER)
            if abs(x) < 104:
                out += circle(x + 6, y - 31, 1.9, 0.6, PAPER)
    out += (
        circle(110, -6, 14, 1.1, PAPER)
        + circle(110, -6, 8.5, 0.7)
        + tone(arc(110, -6, 8.5, 8.5, 0, 360, 16), 0.3)
    )
    out += circle(132, 14, 5, 0.8, PAPER) + circle(86, 20, 4, 0.8, PAPER)
    for (ax, ay), fx in (
        ((-92, 26), -150),
        ((-30, 38), -60),
        ((44, 38), 52),
        ((100, 26), 142),
    ):
        out += _leg((ax, ay), (fx, gy), (15, 11, 7))
        out += circle(ax, ay, 8.5, 1.2, PAPER) + circle(ax, ay, 3, 0, INK)
    return out


def walking_city() -> None:
    """Herron's ambulant cities: hulls on telescoping legs, passing New York."""
    gy = 432.0
    b = []
    rng = random.Random(1964)
    x = 40.0
    while x < 676:
        wd = rng.uniform(8, 18)
        hgt = rng.uniform(14, 62) + (58 if 300 < x < 318 else 0)
        b.append(tone([(x, gy), (x, gy - hgt), (x + wd, gy - hgt), (x + wd, gy)], 0.1))
        x += wd + rng.uniform(-2, 3)
    b.append(ground(gy))
    walker = _walker()
    b.append(
        f'<g transform="translate(128 {gy - 174 * 0.42:.1f}) scale(0.42)" opacity="0.7">\n{walker}</g>\n'
    )
    b.append(f'<g transform="translate(430 {gy - 174})">\n{walker}</g>\n')
    b += [
        dim_h(280, 580, 140, "hull c. 200 m"),
        note(52, 96, "A second city, further off", (128, gy - 104)),
        note(52, 190, "Telescoping legs", (300, 350)),
        note(596, 196, "Pop-up units", (466, 182)),
    ]
    write(
        "walking-city",
        "Walking City — Archigram / Herron, 1964",
        "elevation",
        "skyline not to scale",
        "".join(b),
    )


def plug_in_city() -> None:
    """Cook's megastructure: a lattice of tubes, with everything else plugged in."""
    gy, top, mod, x0, x1 = 432.0, 168.0, 116.0, 70.0, 650.0
    run = (gy - top) / math.tan(math.radians(60))
    rng = random.Random(1964)
    b = [ground(gy)]

    def clip(p: Pt, q: Pt) -> tuple[Pt, Pt] | None:
        """Trim a diagonal to the width of the structure."""
        (ax, ay), (bx, by) = p, q
        ts = sorted(((x0 - ax) / (bx - ax), (x1 - ax) / (bx - ax)))
        t0, t1 = max(0.0, ts[0]), min(1.0, ts[1])
        if t0 >= t1:
            return None
        return (
            (ax + (bx - ax) * t0, ay + (by - ay) * t0),
            (ax + (bx - ax) * t1, ay + (by - ay) * t1),
        )

    tubes = []
    for i in range(-2, 8):
        for sx in (1, -1):
            seg = clip((x0 + i * mod, gy), (x0 + i * mod + sx * run, top))
            if seg:
                tubes.append((seg, sx))
    lv1 = gy - (mod / 2) / run * (gy - top)
    lv2 = gy - mod / run * (gy - top)

    # capsule towers, behind the lattice
    for x, ttop in ((244.0, 92.0), (534.0, 124.0)):
        b.append(rect(x - 8, ttop, 16, gy - ttop, 1.2, PAPER))
        y = ttop + 6
        while y < top - 4:
            for sx in (-1, 1):
                b.append(
                    rect(
                        x + sx * 14 - 6,
                        y,
                        12,
                        6.5,
                        0.8,
                        INK if rng.random() < 0.35 else PAPER,
                        o=0.85,
                    )
                )
            y += 9
        b.append(rect(x - 11, ttop - 5, 22, 5, 1.0, PAPER))

    for wt, col in ((7.5, INK), (5.3, PAPER)):
        for (p, q), _ in tubes:
            b.append(line(*p, *q, wt, col))
        for y in (lv1, lv2, top):
            b.append(line(x0, y, x1, y, wt * 0.8, col))

    # capsules, stepped up the diagonals; some bays stand empty
    for (p, q), sx in tubes:
        for lo, hi in ((0.06, 0.34), (0.44, 0.72)):
            if rng.random() < 0.3:
                continue
            steps = 6
            for i in range(steps):
                t = lo + (hi - lo) * i / (steps - 1)
                cxp = p[0] + (q[0] - p[0]) * t - sx * 13
                cyp = p[1] + (q[1] - p[1]) * t
                if not x0 + 8 < cxp < x1 - 8 or rng.random() < 0.18:
                    continue
                dark = rng.random() < 0.3
                b.append(
                    rect(
                        cxp - 7,
                        cyp - 4.5,
                        14,
                        9,
                        0.8,
                        INK if dark else PAPER,
                        o=0.85 if dark else 1,
                    )
                )
                b.append(circle(cxp, cyp, 1.5, 0.5, PAPER))
    # larger units at the nodes, and a train in the tube
    for x, y, wd in ((186, lv1, 40), (418, lv2, 46), (360, lv1, 34), (592, lv1, 38)):
        b.append(rect(x - wd / 2, y - 22, wd, 18, 1.0, PAPER))
        b.append(
            hatch(
                [
                    (x - wd / 2, y - 22),
                    (x + wd / 2, y - 22),
                    (x + wd / 2, y - 4),
                    (x - wd / 2, y - 4),
                ],
                3,
                62,
                o=0.4,
            )
        )
    for i in range(4):
        b.append(rect(452 + i * 15, lv1 - 2, 13, 4, 0, INK))

    # the craneway on top
    b += [
        line(x0, top - 8, x1, top - 8, 0.9),
        rect(392, top - 60, 8, 52, 1.0, PAPER),
        path(
            f"M396,{top - 60}v-10l44,10M396,{top - 70}l-26,10M352,{top - 60}H454", 0.9
        ),
        line(440, top - 60, 440, top - 36, 0.5),
        rect(432, top - 36, 16, 10, 0.9, PAPER),
        path(f"M468,{top - 8}q34,-44 76,0", 0.7, c=FAINT, dash="4 3"),
        dim_v(668, top, gy, "c. 130 m", side=-1),
        note(52, 84, "Capsule tower", (236, 110)),
        note(52, 118, "Craneway: units lifted in and out", (372, top - 60)),
        note(52, 152, "Capsule homes, replaceable", (110, lv2 + 20)),
        note(470, 84, "Inflatable roof, for bad weather", (506, top - 30)),
    ]
    write(
        "plug-in-city",
        "Plug-in City — Archigram / Cook, 1964",
        "elevation",
        "",
        "".join(b),
    )


def continuous_monument() -> None:
    """Superstudio's single building, in one-point perspective, running off the sheet."""
    vx, vy = 96.0, 338.0
    nx, ntop, nbot = 760.0, 60.0, 452.0
    far = 152.0

    def on(x: float, edge: float) -> float:
        """Height at x of the line from the near edge down to the vanishing point."""
        return vy + (edge - vy) * (x - vx) / (nx - vx)

    b = [
        '<clipPath id="sheet"><rect x="19" y="55" width="682" height="415"/></clipPath>\n<g clip-path="url(#sheet)">\n'
    ]
    hills = [
        (36, 334),
        (70, 316),
        (104, 326),
        (150, 298),
        (196, 322),
        (250, 306),
        (300, 330),
        (360, 338),
    ]
    b.append(poly(hills, 0.6, c=FAINT, close=False))
    b.append(line(36, vy, 684, vy, 0.7))
    for x, y, wd in ((60, 110, 70), (176, 150, 54), (96, 196, 40)):
        b.append(
            path(
                f"M{x},{y}q{wd / 4},-7 {wd / 2},-1q{wd / 4},-6 {wd / 2},1", 0.5, c=FAINT
            )
        )

    face = [(far, on(far, ntop)), (nx, ntop), (nx, nbot), (far, on(far, nbot))]
    b.append(
        tone(
            [
                (far, on(far, nbot)),
                (nx, nbot),
                (nx, nbot + 26),
                (far + 60, on(far, nbot) + 3),
            ],
            0.1,
        )
    )
    b.append(poly(face, 0, PAPER))
    b.append(tone(face, 0.03))
    b.append(
        tone(
            [
                (far, on(far, ntop)),
                (290, on(290, ntop)),
                (290, on(290, nbot)),
                (far, on(far, nbot)),
            ],
            0.1,
        )
    )
    b.append(line(vx + 6, on(vx + 6, ntop), far, on(far, ntop), 0.5, FAINT))
    b.append(line(vx + 6, on(vx + 6, nbot), far, on(far, nbot), 0.5, FAINT))
    d = ""
    for i in range(1, 12):
        edge = ntop + (nbot - ntop) * i / 12
        d += f"M{nx},{n(edge)}L{far},{n(on(far, edge))}"
    k = 1
    while True:
        x = vx + (nx - vx) / (1 + k * 0.036)
        if x < 268:
            break
        d += f"M{n(x)},{n(on(x, ntop))}V{n(on(x, nbot))}"
        k += 1
    b.append(path(d, 0.45, o=0.75))
    b.append(poly(face, 1.5))

    # a town in the foreground, for scale
    gl = [(36, 442), (120, 436), (230, 440), (330, 432), (420, 446)]
    b.append(poly(gl, 0.7, close=False))
    for x, wd, h in (
        (120, 13, 9),
        (136, 11, 12),
        (150, 14, 8),
        (196, 12, 10),
        (210, 15, 9),
        (228, 11, 12),
        (244, 13, 8),
        (270, 12, 10),
    ):
        y = 438.0
        b.append(
            poly(
                [
                    (x, y),
                    (x, y - h),
                    (x + wd / 2, y - h - 5),
                    (x + wd, y - h),
                    (x + wd, y),
                ],
                0.7,
                PAPER,
            )
        )
    b.append(
        poly([(170, 438), (170, 414), (176, 392), (182, 414), (182, 438)], 0.8, PAPER)
    )
    b.append(rect(182, 420, 14, 18, 0.7, PAPER))
    for x in (106, 262, 290, 304):
        b.append(line(x, 438, x, 432, 0.5))
        b.append(circle(x, 428, 4.5, 0.6, PAPER))
    b.append("</g>\n")
    b += [
        note(52, 84, "It does not end: it leaves the sheet", (640, 96)),
        note(52, 250, "Grid closes to grey with distance", (236, 300)),
        note(52, 404, "A town, and its church", (176, 400)),
    ]
    write(
        "continuous-monument",
        "Continuous Monument — Superstudio, 1969",
        "perspective",
        "c. 200 m high, without end",
        "".join(b),
    )


ALL = [
    dome_over_manhattan,
    tokyo_bay,
    fun_palace,
    walking_city,
    plug_in_city,
    continuous_monument,
]
