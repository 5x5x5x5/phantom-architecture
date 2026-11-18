"""Shared drawing kit: canvas, palette, SVG primitives, true-scale references.

Every helper returns an SVG fragment as a string. Coordinates are canvas
pixels; where a drawing is to scale, ``s`` is pixels per metre.
"""

from __future__ import annotations

import logging
import math
from html import escape
from itertools import count
from pathlib import Path
from xml.etree import ElementTree

log = logging.getLogger(__name__)

OUT = Path(__file__).resolve().parents[2] / "docs" / "assets" / "illustrations"

W, H = 720, 500

# Palette: ink on paper.
INK = "#1f1a14"
PAPER = "#f4ecd8"
FAINT = "#8a7f67"
ACCENT = "#8b3a2e"

MONO = "'IBM Plex Mono', ui-monospace, Menlo, Consolas, monospace"

Pt = tuple[float, float]

_clip_ids = count()


def n(v: float) -> str:
    """Format a coordinate compactly."""
    return f"{v:.1f}".removesuffix(".0")


def pts(p: list[Pt]) -> str:
    return " ".join(f"{n(x)},{n(y)}" for x, y in p)


def _attrs(w: float, c: str, fill: str, o: float, dash: str) -> str:
    out = f' fill="{fill}"'
    out += f' stroke="{c}" stroke-width="{w:g}"' if w else ' stroke="none"'
    if o != 1:
        out += f' opacity="{o:g}"'
    if dash:
        out += f' stroke-dasharray="{dash}"'
    return out


# --- primitives -----------------------------------------------------------


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    w: float = 1.0,
    c: str = INK,
    o: float = 1.0,
    dash: str = "",
) -> str:
    return (
        f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}"'
        f"{_attrs(w, c, 'none', o, dash)}/>\n"
    )


def poly(
    p: list[Pt],
    w: float = 1.0,
    fill: str = "none",
    c: str = INK,
    o: float = 1.0,
    close: bool = True,
    dash: str = "",
) -> str:
    tag = "polygon" if close else "polyline"
    return f'<{tag} points="{pts(p)}"{_attrs(w, c, fill, o, dash)}/>\n'


def path(
    d: str,
    w: float = 1.0,
    fill: str = "none",
    c: str = INK,
    o: float = 1.0,
    dash: str = "",
) -> str:
    return f'<path d="{d}"{_attrs(w, c, fill, o, dash)}/>\n'


def rect(
    x: float,
    y: float,
    rw: float,
    rh: float,
    w: float = 1.0,
    fill: str = "none",
    c: str = INK,
    o: float = 1.0,
    dash: str = "",
) -> str:
    return (
        f'<rect x="{n(x)}" y="{n(y)}" width="{n(rw)}" height="{n(rh)}"'
        f"{_attrs(w, c, fill, o, dash)}/>\n"
    )


def circle(
    cx: float,
    cy: float,
    r: float,
    w: float = 1.0,
    fill: str = "none",
    c: str = INK,
    o: float = 1.0,
    dash: str = "",
) -> str:
    return (
        f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}"{_attrs(w, c, fill, o, dash)}/>\n'
    )


def text(
    x: float,
    y: float,
    s: str,
    size: float = 7.0,
    anchor: str = "start",
    c: str = FAINT,
    rot: float = 0.0,
) -> str:
    turn = f' transform="rotate({rot:g} {n(x)} {n(y)})"' if rot else ""
    return (
        f'<text x="{n(x)}" y="{n(y)}" font-family="{MONO}" font-size="{size:g}"'
        f' fill="{c}" text-anchor="{anchor}" letter-spacing="1"{turn}>'
        f"{escape(s.upper(), quote=False)}</text>\n"
    )


def tone(p: list[Pt], o: float = 0.08, c: str = INK) -> str:
    """A flat wash of ink over a polygon."""
    return f'<polygon points="{pts(p)}" fill="{c}" fill-opacity="{o:g}"/>\n'


def hatch(
    p: list[Pt],
    gap: float = 4.0,
    angle: float = 45.0,
    w: float = 0.4,
    c: str = INK,
    o: float = 0.55,
) -> str:
    """Parallel-line hatching clipped to a polygon."""
    xs, ys = [x for x, _ in p], [y for _, y in p]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    r = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 1
    a = math.radians(angle)
    dx, dy, nx, ny = math.cos(a), -math.sin(a), math.sin(a), math.cos(a)
    d = ""
    k = -r
    while k <= r:
        mx, my = cx + k * nx, cy + k * ny
        d += f"M{n(mx - r * dx)},{n(my - r * dy)}L{n(mx + r * dx)},{n(my + r * dy)}"
        k += gap
    i = next(_clip_ids)
    return (
        f'<clipPath id="h{i}"><polygon points="{pts(p)}"/></clipPath>\n'
        f'<path d="{d}" clip-path="url(#h{i})"{_attrs(w, c, "none", o, "")}/>\n'
    )


# --- geometry -------------------------------------------------------------


def arc(
    cx: float, cy: float, rx: float, ry: float, a0: float, a1: float, k: int = 24
) -> list[Pt]:
    """Points along an ellipse arc. Degrees; 0 is east, 90 is up."""
    out = []
    for i in range(k + 1):
        t = math.radians(a0 + (a1 - a0) * i / k)
        out.append((cx + rx * math.cos(t), cy - ry * math.sin(t)))
    return out


def quad(p0: Pt, c: Pt, p1: Pt, t: float) -> Pt:
    """A point on a quadratic Bézier."""
    u = 1 - t
    return (
        u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0],
        u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1],
    )


def box(cx: float, cy: float, bw: float, bh: float, ang: float = 0.0) -> list[Pt]:
    """A rectangle centred on (cx, cy), rotated ``ang`` degrees anticlockwise."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [
        (cx + u * ca + v * sa, cy - u * sa + v * ca)
        for u, v in (
            (-bw / 2, -bh / 2),
            (bw / 2, -bh / 2),
            (bw / 2, bh / 2),
            (-bw / 2, bh / 2),
        )
    ]


def profile(cx: float, gy: float, s: float, prof: list[Pt]) -> list[Pt]:
    """Mirror a (height m, half-width m) profile into a silhouette polygon."""
    left = [(cx - hw * s, gy - z * s) for z, hw in prof]
    right = [(cx + hw * s, gy - z * s) for z, hw in reversed(prof)]
    return left + right


# --- drafting conventions -------------------------------------------------


def ground(y: float, x1: float = 36, x2: float = W - 36) -> str:
    """A ground line with earth ticks beneath it."""
    d = "".join(f"M{n(x)},{n(y)}l-7,5.5" for x in range(int(x1) + 12, int(x2), 13))
    return line(x1, y, x2, y, 0.9) + path(d, 0.4, o=0.8)


def water(y: float, x1: float, x2: float, rows: int = 3) -> str:
    """A water surface: a level line with broken ripple strokes below."""
    out = line(x1, y, x2, y, 0.8)
    for r in range(1, rows + 1):
        d = ""
        x = x1 + 9 * r
        while x < x2 - 14:
            d += f"M{n(x)},{n(y + 4.5 * r)}h{12 - 2 * r}"
            x += 31 + 6 * r
        out += path(d, 0.4, c=FAINT)
    return out


def dim_v(x: float, y1: float, y2: float, label: str, side: int = 1) -> str:
    """A vertical dimension line with end ticks and a rotated label."""
    return (
        line(x, y1, x, y2, 0.5, FAINT)
        + line(x - 3, y1, x + 3, y1, 0.5, FAINT)
        + line(x - 3, y2, x + 3, y2, 0.5, FAINT)
        + text(
            x + (9 if side > 0 else -4), (y1 + y2) / 2, label, 6.5, "middle", rot=-90
        )
    )


def dim_h(x1: float, x2: float, y: float, label: str) -> str:
    return (
        line(x1, y, x2, y, 0.5, FAINT)
        + line(x1, y - 3, x1, y + 3, 0.5, FAINT)
        + line(x2, y - 3, x2, y + 3, 0.5, FAINT)
        + text((x1 + x2) / 2, y - 4, label, 6.5, "middle")
    )


def note(
    x: float,
    y: float,
    label: str,
    to: Pt | None = None,
    anchor: str = "start",
) -> str:
    """A small annotation, optionally with a leader line to a point."""
    out = ""
    if to:
        wd = len(label) * 4.9  # monospace advance at this size
        lo, hi = (x, x + wd) if anchor == "start" else (x - wd, x)
        sx = hi + 3 if to[0] > hi else lo - 3 if to[0] < lo else (lo + hi) / 2
        sy = y - 2.5 if not lo <= to[0] <= hi else (y + 3 if to[1] > y else y - 8)
        out += line(sx, sy, to[0], to[1], 0.4, FAINT)
        out += circle(to[0], to[1], 1.1, 0, FAINT)
    return out + text(x, y, label, 6.5, anchor)


def scale_bar(x: float, y: float, px: float, label: str) -> str:
    return (
        rect(x, y, px / 2, 3, 0.5, FAINT, FAINT)
        + rect(x + px / 2, y, px / 2, 3, 0.5, "none", FAINT)
        + text(x, y - 4, label, 6.5)
    )


# --- scale references -----------------------------------------------------

# (height m, half-width m) silhouettes of things a reader already knows.
EIFFEL: list[Pt] = [
    (0, 62.5), (20, 50), (40, 40), (57, 33), (57, 36), (62, 36), (62, 30),
    (90, 22), (115, 16), (115, 19), (120, 19), (120, 14), (160, 9.5),
    (200, 6.5), (240, 4.5), (276, 3.2), (276, 5.5), (282, 5.5), (282, 2.5),
    (300, 1.6), (330, 0.4),
]  # fmt: skip
EMPIRE: list[Pt] = [
    (0, 64), (25, 64), (25, 52), (95, 52), (95, 44), (290, 44), (290, 38),
    (320, 38), (320, 26), (365, 26), (365, 15), (381, 15), (381, 6),
    (410, 6), (425, 3), (443, 0.5),
]  # fmt: skip
ST_PETERS: list[Pt] = [
    (0, 57), (46, 57), (46, 30), (52, 30), (52, 25), (76, 25), (78, 23.5),
    (90, 21.5), (102, 17), (112, 11), (119, 5), (128, 4.5), (136, 0.5),
]  # fmt: skip


def reference(
    cx: float, gy: float, s: float, prof: list[Pt], *labels: str, fill: str = PAPER
) -> str:
    """A known building drawn at the drawing's scale, labelled above."""
    out = poly(profile(cx, gy, s, prof), 0.7, fill, FAINT)
    top = gy - prof[-1][0] * s
    for i, label in enumerate(reversed(labels)):
        out += text(cx, top - 5 - 8 * i, label, 6, "middle")
    return out


def person(x: float, gy: float, h: float = 10.0, c: str = INK) -> str:
    """A standing figure ``h`` pixels tall (1.8 m at the drawing's scale)."""
    r = h * 0.09
    body = [
        (x - h * 0.13, gy - h * 0.8), (x + h * 0.13, gy - h * 0.8),
        (x + h * 0.09, gy - h * 0.42), (x + h * 0.1, gy), (x + h * 0.02, gy),
        (x, gy - h * 0.38), (x - h * 0.02, gy), (x - h * 0.1, gy),
        (x - h * 0.09, gy - h * 0.42),
    ]  # fmt: skip
    return circle(x, gy - h + r, r, 0, c) + poly(body, 0, c)


def cypress(x: float, gy: float, h: float, o: float = 0.8) -> str:
    wd = h * 0.2
    crown = [
        (x, gy - h), (x + wd / 2, gy - h * 0.45), (x + wd * 0.35, gy - h * 0.1),
        (x - wd * 0.35, gy - h * 0.1), (x - wd / 2, gy - h * 0.45),
    ]  # fmt: skip
    return line(x, gy, x, gy - h * 0.1, 0.5) + poly(crown, 0, INK, o=o)


# --- sheet ----------------------------------------------------------------


def write(slug: str, title: str, right: str, left: str, body: str) -> None:
    """Wrap a drawing in the common sheet frame and write it to disk."""
    global _clip_ids
    sheet = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" stroke-linejoin="round" stroke-linecap="round">\n'
        + rect(0, 0, W, H, 0, PAPER)
        + body
        + rect(18, 18, W - 36, H - 36, 0.6, o=0.6)
        + text(36, 44, title, 11, c=INK).replace('spacing="1"', 'spacing="2"')
        + line(36, 54, W - 36, 54, 0.5)
        + text(W - 36, H - 26, right, 9, "end")
        + text(36, H - 26, left, 9)
        + "</svg>\n"
    )
    ElementTree.fromstring(sheet)  # refuse to write malformed SVG
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{slug}.svg").write_text(sheet, encoding="utf-8")
    _clip_ids = count()  # ids only need to be unique within one file
    log.info("wrote %s.svg", slug)
