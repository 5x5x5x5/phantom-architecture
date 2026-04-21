"""Generate schematic blueprint-style SVG elevations for each phantom entry.

Each SVG is a one-off: a simple, recognizable silhouette of the building
rendered in a unified aesthetic — warm ink on paper, a 1.8 m human figure
for scale, and a height caption. Not photographic; evocative.

Run:
    uv run python scripts/generate_illustrations.py

Output: docs/assets/illustrations/<slug>.svg (twenty-five files).
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "illustrations"
OUT.mkdir(parents=True, exist_ok=True)

# Canvas size for every illustration. Wider than tall so the scale
# reference reads cleanly alongside the building silhouette.
W, H = 720, 500

# Palette: ink on paper.
INK = "#1f1a14"
PAPER = "#f4ecd8"
FAINT = "#8a7f67"
ACCENT = "#8b3a2e"


def frame(title: str, height_label: str, extra_note: str = "") -> str:
    """The outer frame common to every entry."""
    return f"""
  <!-- paper -->
  <rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>

  <!-- margin rule -->
  <rect x="18" y="18" width="{W - 36}" height="{H - 36}"
        fill="none" stroke="{INK}" stroke-width="0.6" opacity="0.6"/>

  <!-- top title strip -->
  <text x="36" y="44" font-family="IBM Plex Mono, monospace"
        font-size="11" fill="{INK}" letter-spacing="2">
    {title.upper()}
  </text>
  <line x1="36" y1="54" x2="{W - 36}" y2="54"
        stroke="{INK}" stroke-width="0.5"/>

  <!-- height caption -->
  <text x="{W - 36}" y="{H - 26}" font-family="IBM Plex Mono, monospace"
        font-size="9" fill="{FAINT}" text-anchor="end" letter-spacing="1.5">
    {height_label.upper()}
  </text>

  <!-- optional note at lower-left -->
  <text x="36" y="{H - 26}" font-family="IBM Plex Mono, monospace"
        font-size="9" fill="{FAINT}" letter-spacing="1.5">
    {extra_note.upper()}
  </text>
"""


def human_figure(x: float, y: float, scale: float = 1.0) -> str:
    """A 1.8 m stick figure at (x, y), where y is ground level.

    Used for scale reference. At scale=1, figure is ~30 px tall.
    """
    s = scale
    head_r = 3 * s
    body_h = 18 * s
    return f"""
  <g stroke="{INK}" stroke-width="1" fill="none"
     transform="translate({x},{y - body_h - head_r * 2})">
    <circle cx="0" cy="{head_r}" r="{head_r}"/>
    <line x1="0" y1="{head_r * 2}" x2="0" y2="{head_r * 2 + body_h * 0.55}"/>
    <line x1="0" y1="{head_r * 2 + body_h * 0.3}"
          x2="{-head_r * 1.5}" y2="{head_r * 2 + body_h * 0.5}"/>
    <line x1="0" y1="{head_r * 2 + body_h * 0.3}"
          x2="{head_r * 1.5}" y2="{head_r * 2 + body_h * 0.5}"/>
    <line x1="0" y1="{head_r * 2 + body_h * 0.55}"
          x2="{-head_r * 1.5}" y2="{head_r * 2 + body_h}"/>
    <line x1="0" y1="{head_r * 2 + body_h * 0.55}"
          x2="{head_r * 1.5}" y2="{head_r * 2 + body_h}"/>
  </g>
"""


def ground(y: float) -> str:
    """A ground line across the canvas at y."""
    return (
        f'  <line x1="36" y1="{y}" x2="{W - 36}" y2="{y}" '
        f'stroke="{INK}" stroke-width="0.8"/>\n'
        + "".join(
            f'  <line x1="{x}" y1="{y}" x2="{x - 8}" y2="{y + 6}" '
            f'stroke="{INK}" stroke-width="0.4"/>\n'
            for x in range(60, W - 36, 14)
        )
    )


def svg(body: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
{body}
</svg>
"""


def write(slug: str, body: str) -> None:
    path = OUT / f"{slug}.svg"
    path.write_text(svg(body))
    print(f"wrote {path.relative_to(OUT.parents[1])}")


# ===========================================================================
# Individual illustrations — one function per entry.
# Each aims for a recognizable silhouette, not photographic accuracy.
# ===========================================================================


def babel() -> None:
    """Bruegel's Tower of Babel — a stepped spiral drum."""
    body = [frame("THE TOWER OF BABEL — BRUEGEL, 1563", "≈ 500 M AS DEPICTED")]
    gy = 440
    body.append(ground(gy))
    # seven stepped drums
    base_w = 420
    step = 8
    for i in range(7):
        w = base_w - i * 30
        h = 38
        x = W / 2 - w / 2
        y = gy - (i + 1) * h
        body.append(
            f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
        )
        # spiral ramp
        body.append(
            f'  <path d="M {x + step} {y + h} L {x + w - step} {y}" '
            f'stroke="{INK}" stroke-width="0.4" fill="none" opacity="0.6"/>\n'
        )
    # broken top (it's unfinished, famously)
    body.append(
        f'  <path d="M {W / 2 - 40} {gy - 7 * 38} L {W / 2 - 20} {gy - 7 * 38 - 15} '
        f"L {W / 2 + 5} {gy - 7 * 38 - 8} L {W / 2 + 30} {gy - 7 * 38 - 18} "
        f'L {W / 2 + 40} {gy - 7 * 38}" fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(human_figure(620, gy, 1.2))
    write("babel", "".join(body))


def sforzinda() -> None:
    """Filarete's Sforzinda — an eight-pointed star plan in elevation-ish."""
    body = [frame("SFORZINDA — FILARETE, 1457–1464", "IDEAL CITY, 8-POINT STAR PLAN")]
    gy = 430
    body.append(ground(gy))
    cx, cy = W / 2, 250
    r_outer = 160
    import math

    # eight-pointed star
    points = []
    for i in range(16):
        a = i * (360 / 16) - 90
        r = r_outer if i % 2 == 0 else r_outer * 0.55
        px = cx + r * math.cos(math.radians(a))
        py = cy + r * math.sin(math.radians(a))
        points.append(f"{px:.1f},{py:.1f}")
    body.append(
        f'  <polygon points="{" ".join(points)}" fill="none" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # central circle (piazza)
    body.append(
        f'  <circle cx="{cx}" cy="{cy}" r="32" fill="none" '
        f'stroke="{INK}" stroke-width="0.8"/>\n'
    )
    # radial roads
    for i in range(8):
        a = i * 45 - 90
        x2 = cx + r_outer * math.cos(math.radians(a))
        y2 = cy + r_outer * math.sin(math.radians(a))
        body.append(
            f'  <line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{INK}" stroke-width="0.4" opacity="0.7"/>\n'
        )
    write("sforzinda", "".join(body))


def ideal_city() -> None:
    """Da Vinci's ideal city — two-level urban section."""
    body = [frame("IDEAL CITY — LEONARDO DA VINCI, C. 1487", "DOUBLE-LEVEL SECTION")]
    gy = 430
    body.append(ground(gy))
    # upper level — nobles — and lower level — service
    upper_y = 200
    level_h = 100
    # archway arcade
    for i in range(8):
        x = 80 + i * 75
        # ground-level arch
        body.append(
            f'  <path d="M {x} {gy} L {x} {gy - 50} Q {x + 30} {gy - 85} {x + 60} {gy - 50} '
            f'L {x + 60} {gy}" fill="none" stroke="{INK}" stroke-width="1"/>\n'
        )
        # upper archway
        body.append(
            f'  <path d="M {x + 5} {upper_y + level_h} L {x + 5} {upper_y + 60} '
            f"Q {x + 30} {upper_y + 40} {x + 55} {upper_y + 60} "
            f'L {x + 55} {upper_y + level_h}" fill="none" stroke="{INK}" stroke-width="0.7"/>\n'
        )
    # upper level line
    body.append(
        f'  <line x1="50" y1="{upper_y + level_h}" x2="{W - 50}" y2="{upper_y + level_h}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # roof cornice
    body.append(
        f'  <line x1="50" y1="{upper_y + 30}" x2="{W - 50}" y2="{upper_y + 30}" '
        f'stroke="{INK}" stroke-width="0.8"/>\n'
    )
    body.append(human_figure(660, gy, 1.0))
    write("ideal-city", "".join(body))


def newton_cenotaph() -> None:
    """Boullée's Newton cenotaph — a colossal sphere on a stepped base."""
    body = [frame("CENOTAPH FOR NEWTON — BOULLÉE, 1784", "SPHERE: ≈ 150 M DIAMETER")]
    gy = 440
    body.append(ground(gy))
    cx, cy, r = W / 2, 255, 155
    # cypress trees around base (Boullée's signature)
    for x in (180, 220, 500, 540):
        body.append(
            f'  <path d="M {x} {gy} L {x} {gy - 80} M {x - 10} {gy - 30} '
            f'Q {x} {gy - 70} {x + 10} {gy - 30}" fill="none" '
            f'stroke="{INK}" stroke-width="0.6"/>\n'
        )
    # stepped base
    for i, w in enumerate([440, 380, 320]):
        h = 14
        x = cx - w / 2
        y = gy - (i + 1) * h
        body.append(
            f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
        )
    # sphere
    body.append(
        f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
        f'stroke="{INK}" stroke-width="1.4"/>\n'
    )
    # equatorial band
    body.append(
        f'  <ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.25}" fill="none" '
        f'stroke="{INK}" stroke-width="0.4" opacity="0.5"/>\n'
    )
    # arched portal
    body.append(
        f'  <path d="M {cx - 22} {gy - 3 * 14} L {cx - 22} {gy - 3 * 14 - 30} '
        f"Q {cx} {gy - 3 * 14 - 52} {cx + 22} {gy - 3 * 14 - 30} "
        f'L {cx + 22} {gy - 3 * 14}" fill="{INK}" opacity="0.85"/>\n'
    )
    body.append(human_figure(640, gy, 1.2))
    write("newton-cenotaph", "".join(body))


def chaux() -> None:
    """Ledoux's Saltworks at Chaux — a sliced circle in plan/elevation hybrid."""
    body = [
        frame("ROYAL SALTWORKS AT CHAUX — LEDOUX, 1775", "IDEAL CITY, PARTIAL BUILD")
    ]
    gy = 430
    body.append(ground(gy))
    cx, cy = W / 2, 240
    r = 160
    import math

    # upper half-circle plan
    body.append(
        f'  <path d="M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy}" '
        f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(
        f'  <line x1="{cx - r}" y1="{cy}" x2="{cx + r}" y2="{cy}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # director's house at center
    body.append(
        f'  <rect x="{cx - 28}" y="{cy - 30}" width="56" height="30" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    # colonnade entrance
    for i, x in enumerate([cx - 20, cx - 10, cx, cx + 10, cx + 20]):
        body.append(
            f'  <line x1="{x}" y1="{cy}" x2="{x}" y2="{cy + 20}" '
            f'stroke="{INK}" stroke-width="0.5"/>\n'
        )
    # radial workshops
    for i in range(11):
        a = -180 + i * 18
        x2 = cx + r * 0.85 * math.cos(math.radians(a))
        y2 = cy + r * 0.85 * math.sin(math.radians(a))
        body.append(
            f'  <line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{INK}" stroke-width="0.3" opacity="0.6"/>\n'
        )
    # small buildings along the arc
    import math

    for i in range(11):
        a = -170 + i * 16
        bx = cx + r * 0.95 * math.cos(math.radians(a))
        by = cy + r * 0.95 * math.sin(math.radians(a))
        body.append(
            f'  <rect x="{bx - 6:.1f}" y="{by - 6:.1f}" width="12" height="12" '
            f'fill="none" stroke="{INK}" stroke-width="0.5"/>\n'
        )
    write("chaux", "".join(body))


def soane_royal_palace() -> None:
    """Soane's Royal Palace — stripped neoclassical mass, portico."""
    body = [
        frame("ROYAL PALACE AT WESTMINSTER — SOANE, 1779", "ACADEMIC THESIS PROJECT")
    ]
    gy = 440
    body.append(ground(gy))
    # central block with portico
    main_w, main_h = 340, 110
    cx = W / 2
    body.append(
        f'  <rect x="{cx - main_w / 2}" y="{gy - main_h}" width="{main_w}" height="{main_h}" '
        f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    # portico columns — six
    for i in range(6):
        x = cx - main_w / 2 + 40 + i * 50
        body.append(
            f'  <line x1="{x}" y1="{gy}" x2="{x}" y2="{gy - 80}" '
            f'stroke="{INK}" stroke-width="1.2"/>\n'
        )
    # pediment
    body.append(
        f'  <polygon points="{cx - main_w / 2 + 10},{gy - 80} '
        f'{cx},{gy - main_h - 20} {cx + main_w / 2 - 10},{gy - 80}" '
        f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    # wings
    for side in (-1, 1):
        wx = cx + side * (main_w / 2 + 10)
        ww = 90
        wh = 70
        x = wx - ww / 2 if side == -1 else wx + (ww / 2 - ww)
        body.append(
            f'  <rect x="{x if side == 1 else wx - ww}" y="{gy - wh}" '
            f'width="{ww}" height="{wh}" fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
        )
    # dome above central block
    body.append(
        f'  <path d="M {cx - 50} {gy - main_h - 20} Q {cx} {gy - main_h - 70} '
        f'{cx + 50} {gy - main_h - 20}" fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(human_figure(640, gy, 1.1))
    write("soane-royal-palace", "".join(body))


def citta_nuova() -> None:
    """Sant'Elia's Città Nuova — setback industrial towers with diagonal elements."""
    body = [frame("CITTÀ NUOVA — SANT'ELIA, 1914", "FUTURIST CITY SKETCH")]
    gy = 440
    body.append(ground(gy))
    # tall setback tower
    cx = 260
    tw = 90
    # base slab
    body.append(
        f'  <rect x="{cx - tw / 2 - 30}" y="{gy - 100}" width="{tw + 60}" height="100" '
        f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    # setback stages
    stages = [(0, 280), (-10, 220), (-20, 160), (-30, 100)]
    for dx, h in stages:
        body.append(
            f'  <rect x="{cx - tw / 2 + dx}" y="{gy - h}" width="{tw - 2 * dx}" height="40" '
            f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
        )
    # mullioned windows
    for h in [120, 180, 240]:
        for x in range(int(cx - tw / 2 + 8), int(cx + tw / 2 - 8), 10):
            body.append(
                f'  <line x1="{x}" y1="{gy - h}" x2="{x}" y2="{gy - h + 15}" '
                f'stroke="{INK}" stroke-width="0.3" opacity="0.7"/>\n'
            )
    # diagonal elevator shaft (Sant'Elia's signature)
    body.append(
        f'  <line x1="{cx + tw / 2}" y1="{gy}" x2="{cx + tw / 2 + 80}" y2="{gy - 280}" '
        f'stroke="{INK}" stroke-width="1.2"/>\n'
    )
    body.append(
        f'  <line x1="{cx + tw / 2 + 15}" y1="{gy}" x2="{cx + tw / 2 + 95}" y2="{gy - 280}" '
        f'stroke="{INK}" stroke-width="1.2"/>\n'
    )
    # second tower with stepped profile
    cx2 = 540
    for i, (w, h) in enumerate([(80, 100), (70, 80), (60, 70), (48, 50)]):
        body.append(
            f'  <rect x="{cx2 - w / 2}" y="{gy - sum([100, 80, 70, 50][: i + 1])}" '
            f'width="{w}" height="{[100, 80, 70, 50][i]}" fill="none" '
            f'stroke="{INK}" stroke-width="0.9"/>\n'
        )
    # elevated roadway
    body.append(
        f'  <line x1="36" y1="{gy - 80}" x2="{W - 36}" y2="{gy - 80}" '
        f'stroke="{INK}" stroke-width="0.6" stroke-dasharray="6 4" opacity="0.5"/>\n'
    )
    write("citta-nuova", "".join(body))


def hotel_attraction() -> None:
    """Gaudí's Hotel Attraction — a bullet-shaped tower with parabolic crown."""
    body = [frame("HOTEL ATTRACTION — GAUDÍ, 1908", "NEW YORK: 360 M")]
    gy = 440
    body.append(ground(gy))
    cx = W / 2
    # main parabolic body
    base_w = 160
    top_w = 24
    base_y = gy
    tip_y = 90
    body.append(
        f'  <path d="M {cx - base_w / 2} {base_y} '
        f"Q {cx - base_w / 2} {tip_y + 50} {cx - top_w / 2} {tip_y} "
        f"L {cx + top_w / 2} {tip_y} "
        f'Q {cx + base_w / 2} {tip_y + 50} {cx + base_w / 2} {base_y} Z" '
        f'fill="none" stroke="{INK}" stroke-width="1.2"/>\n'
    )
    # parabolic crown
    body.append(
        f'  <path d="M {cx - top_w / 2} {tip_y} Q {cx} {tip_y - 40} {cx + top_w / 2} {tip_y}" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(
        f'  <line x1="{cx}" y1="{tip_y - 30}" x2="{cx}" y2="{tip_y - 60}" '
        f'stroke="{INK}" stroke-width="0.8"/>\n'
    )
    # horizontal striation rings (Gaudí's tiered elevations)
    for y in range(130, int(base_y), 40):
        # parabolic width at this y
        t = (y - tip_y) / (base_y - tip_y)
        w = top_w + (base_w - top_w) * (t**0.8)
        body.append(
            f'  <line x1="{cx - w / 2}" y1="{y}" x2="{cx + w / 2}" y2="{y}" '
            f'stroke="{INK}" stroke-width="0.3" opacity="0.55"/>\n'
        )
    # projecting terraces at intervals
    for y in [220, 300, 380]:
        t = (y - tip_y) / (base_y - tip_y)
        w = top_w + (base_w - top_w) * (t**0.8)
        body.append(
            f'  <path d="M {cx - w / 2 - 8} {y} L {cx - w / 2} {y - 6} '
            f'L {cx + w / 2} {y - 6} L {cx + w / 2 + 8} {y}" '
            f'fill="none" stroke="{INK}" stroke-width="0.6"/>\n'
        )
    body.append(human_figure(620, gy, 1.2))
    write("hotel-attraction", "".join(body))


def tribune_column() -> None:
    """Adolf Loos's Chicago Tribune column — a doric column as skyscraper."""
    body = [frame("CHICAGO TRIBUNE COLUMN — LOOS, 1922", "COMPETITION ENTRY: ≈ 122 M")]
    gy = 440
    body.append(ground(gy))
    cx = W / 2
    # plinth (office block base)
    body.append(
        f'  <rect x="{cx - 100}" y="{gy - 90}" width="200" height="90" '
        f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    # plinth details
    for y in [gy - 90, gy - 60, gy - 30]:
        body.append(
            f'  <line x1="{cx - 100}" y1="{y}" x2="{cx + 100}" y2="{y}" '
            f'stroke="{INK}" stroke-width="0.4" opacity="0.6"/>\n'
        )
    # column shaft
    shaft_top = gy - 90
    shaft_h = 280
    # fluting — 20 vertical lines
    for i in range(13):
        x = cx - 60 + i * 10
        body.append(
            f'  <line x1="{x}" y1="{shaft_top}" x2="{x}" y2="{shaft_top - shaft_h}" '
            f'stroke="{INK}" stroke-width="0.45"/>\n'
        )
    # outer shaft edges
    body.append(
        f'  <line x1="{cx - 62}" y1="{shaft_top}" x2="{cx - 62}" y2="{shaft_top - shaft_h}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(
        f'  <line x1="{cx + 62}" y1="{shaft_top}" x2="{cx + 62}" y2="{shaft_top - shaft_h}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # doric capital
    cap_y = shaft_top - shaft_h
    body.append(
        f'  <rect x="{cx - 70}" y="{cap_y - 20}" width="140" height="20" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(
        f'  <rect x="{cx - 76}" y="{cap_y - 28}" width="152" height="8" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(human_figure(620, gy, 1.2))
    write("tribune-column", "".join(body))


def tatlin() -> None:
    """Tatlin's Monument — a leaning double helix."""
    body = [
        frame("MONUMENT TO THE THIRD INTERNATIONAL — TATLIN, 1919", "400 M, LEANING"),
    ]
    gy = 440
    body.append(ground(gy))
    import math

    cx = W / 2
    # Axis of the leaning tower. Base at ground-left, tip up-and-right.
    ax0 = (cx - 80, gy)
    ax1 = (cx + 80, 90)
    # two interlocking helices wound around the axis
    helix_pts_1 = []
    helix_pts_2 = []
    turns = 4
    # axis direction and perpendicular (in 2D, rotated 90°)
    dx_axis = ax1[0] - ax0[0]
    dy_axis = ax1[1] - ax0[1]
    axis_len = math.sqrt(dx_axis * dx_axis + dy_axis * dy_axis)
    # perpendicular unit vector
    perp = (-dy_axis / axis_len, dx_axis / axis_len)
    for i in range(240):
        t = i / 240
        # along axis (taper slightly to emphasize conicity)
        x = ax0[0] + t * (ax1[0] - ax0[0])
        y = ax0[1] + t * (ax1[1] - ax0[1])
        # radius shrinks as we go up
        r = 130 * (1 - t * 0.75)
        phase1 = t * turns * 2 * math.pi
        phase2 = phase1 + math.pi
        # oscillation along perpendicular + small vertical flattening
        px1 = r * math.sin(phase1) * perp[0]
        py1 = r * math.sin(phase1) * perp[1] + r * 0.28 * math.cos(phase1)
        px2 = r * math.sin(phase2) * perp[0]
        py2 = r * math.sin(phase2) * perp[1] + r * 0.28 * math.cos(phase2)
        helix_pts_1.append(f"{x + px1:.1f},{y + py1:.1f}")
        helix_pts_2.append(f"{x + px2:.1f},{y + py2:.1f}")
    body.append(
        f'  <polyline points="{" ".join(helix_pts_1)}" fill="none" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(
        f'  <polyline points="{" ".join(helix_pts_2)}" fill="none" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # tilted axis (dashed)
    body.append(
        f'  <line x1="{ax0[0]}" y1="{ax0[1]}" x2="{ax1[0]:.1f}" y2="{ax1[1]:.1f}" '
        f'stroke="{INK}" stroke-width="0.6" stroke-dasharray="4 4" opacity="0.6"/>\n'
    )

    # interior volumes — cube, pyramid, cylinder — sit at 1/4, 1/2, 3/4
    # along the leaning axis (Tatlin's legislative / executive / propaganda triad).
    def pt(t: float) -> tuple[float, float]:
        return (ax0[0] + t * (ax1[0] - ax0[0]), ax0[1] + t * (ax1[1] - ax0[1]))

    # cube (bottom, legislative)
    cx1, cy1 = pt(0.20)
    body.append(
        f'  <rect x="{cx1 - 36:.1f}" y="{cy1 - 40:.1f}" width="72" height="60" '
        f'fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    # pyramid (middle, executive)
    cx2, cy2 = pt(0.50)
    body.append(
        f'  <polygon points="{cx2 - 30:.1f},{cy2 + 10:.1f} '
        f'{cx2:.1f},{cy2 - 40:.1f} {cx2 + 30:.1f},{cy2 + 10:.1f}" '
        f'fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    # cylinder (upper, propaganda — radio transmitter)
    cx3, cy3 = pt(0.78)
    body.append(
        f'  <ellipse cx="{cx3:.1f}" cy="{cy3 + 24:.1f}" rx="20" ry="6" '
        f'fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(
        f'  <line x1="{cx3 - 20:.1f}" y1="{cy3 + 24:.1f}" '
        f'x2="{cx3 - 20:.1f}" y2="{cy3 - 18:.1f}" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(
        f'  <line x1="{cx3 + 20:.1f}" y1="{cy3 + 24:.1f}" '
        f'x2="{cx3 + 20:.1f}" y2="{cy3 - 18:.1f}" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(
        f'  <ellipse cx="{cx3:.1f}" cy="{cy3 - 18:.1f}" rx="20" ry="6" '
        f'fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(human_figure(620, gy, 1.4))
    write("tatlin", "".join(body))


def ferriss() -> None:
    """Ferriss's Metropolis of Tomorrow — stepped setback pyramidal skyscrapers."""
    body = [
        frame("THE METROPOLIS OF TOMORROW — FERRISS, 1929", "VISIONARY CITY DRAWINGS")
    ]
    gy = 440
    body.append(ground(gy))

    # three massive stepped towers
    def stepped(cx_: float, base_w: float, base_h: float, levels: int) -> list[str]:
        parts = []
        cur_w = base_w
        cur_h = 0
        for i in range(levels):
            h = base_h * (0.9 - i * 0.1)
            parts.append(
                f'  <rect x="{cx_ - cur_w / 2}" y="{gy - cur_h - h}" '
                f'width="{cur_w}" height="{h}" fill="none" '
                f'stroke="{INK}" stroke-width="1"/>\n'
            )
            cur_h += h
            cur_w *= 0.78
        return parts

    body.extend(stepped(200, 160, 90, 4))
    body.extend(stepped(W / 2, 200, 110, 5))
    body.extend(stepped(540, 150, 85, 4))
    # window hatching — just on central tower
    for y in range(160, 380, 14):
        for x in range(int(W / 2 - 70), int(W / 2 + 70), 10):
            body.append(
                f'  <line x1="{x}" y1="{y}" x2="{x + 5}" y2="{y}" '
                f'stroke="{INK}" stroke-width="0.3" opacity="0.5"/>\n'
            )
    body.append(human_figure(640, gy, 1.2))
    write("ferriss", "".join(body))


def plan_voisin() -> None:
    """Le Corbusier's Plan Voisin — eighteen identical cruciform towers."""
    body = [frame("PLAN VOISIN — LE CORBUSIER, 1925", "PARIS, 18 CRUCIFORM TOWERS")]
    gy = 440
    body.append(ground(gy))
    # six cruciform tower silhouettes in elevation (representing the 18)
    tower_w = 60
    tower_h = 240
    spacing = 100
    start_x = 90
    for i in range(6):
        cx = start_x + i * spacing
        # central vertical mass
        body.append(
            f'  <rect x="{cx - tower_w / 2}" y="{gy - tower_h}" '
            f'width="{tower_w}" height="{tower_h}" fill="none" '
            f'stroke="{INK}" stroke-width="1"/>\n'
        )
        # projecting wings (cruciform plan read in elevation)
        body.append(
            f'  <line x1="{cx - tower_w / 2 - 8}" y1="{gy - tower_h}" '
            f'x2="{cx - tower_w / 2 - 8}" y2="{gy}" '
            f'stroke="{INK}" stroke-width="0.5" opacity="0.6"/>\n'
        )
        body.append(
            f'  <line x1="{cx + tower_w / 2 + 8}" y1="{gy - tower_h}" '
            f'x2="{cx + tower_w / 2 + 8}" y2="{gy}" '
            f'stroke="{INK}" stroke-width="0.5" opacity="0.6"/>\n'
        )
        # horizontal window bands
        for y in range(int(gy - tower_h + 15), int(gy), 22):
            body.append(
                f'  <line x1="{cx - tower_w / 2 + 3}" y1="{y}" '
                f'x2="{cx + tower_w / 2 - 3}" y2="{y}" '
                f'stroke="{INK}" stroke-width="0.35" opacity="0.55"/>\n'
            )
    # suggestion of park below
    for x in range(50, W - 50, 18):
        body.append(
            f'  <path d="M {x} {gy + 4} Q {x + 3} {gy - 4} {x + 6} {gy + 4}" '
            f'fill="none" stroke="{INK}" stroke-width="0.3" opacity="0.5"/>\n'
        )
    write("plan-voisin", "".join(body))


def broadacre() -> None:
    """Wright's Broadacre City — distributed low-rise schema."""
    body = [frame("BROADACRE CITY — FRANK LLOYD WRIGHT, 1932", "DISTRIBUTED PLAN")]
    gy = 430
    body.append(ground(gy))
    # horizon with scattered low buildings
    for x in [90, 160, 230, 310, 390, 470, 550, 630]:
        # each household/unit at one acre
        body.append(
            f'  <rect x="{x}" y="{gy - 35}" width="30" height="35" '
            f'fill="none" stroke="{INK}" stroke-width="0.8"/>\n'
        )
        body.append(
            f'  <polygon points="{x - 3},{gy - 35} {x + 15},{gy - 48} {x + 33},{gy - 35}" '
            f'fill="none" stroke="{INK}" stroke-width="0.7"/>\n'
        )
    # central civic spire (the one vertical moment Wright permitted)
    cx = W / 2
    body.append(
        f'  <line x1="{cx}" y1="{gy - 160}" x2="{cx}" y2="{gy - 30}" '
        f'stroke="{INK}" stroke-width="1.2"/>\n'
    )
    body.append(
        f'  <line x1="{cx - 4}" y1="{gy - 160}" x2="{cx + 4}" y2="{gy - 160}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(
        f'  <path d="M {cx - 12} {gy - 140} L {cx} {gy - 160} L {cx + 12} {gy - 140}" '
        f'fill="none" stroke="{INK}" stroke-width="0.8"/>\n'
    )
    # crossing roads
    body.append(
        f'  <line x1="36" y1="{gy}" x2="{W - 36}" y2="{gy}" '
        f'stroke="{INK}" stroke-width="0.8"/>\n'
    )
    body.append(
        f'  <line x1="{cx}" y1="{gy + 10}" x2="{cx}" y2="{gy - 10}" '
        f'stroke="{INK}" stroke-width="0.6"/>\n'
    )
    # dashed crop-grid behind
    for i, x in enumerate(range(80, W - 50, 60)):
        body.append(
            f'  <line x1="{x}" y1="{gy + 10}" x2="{x}" y2="{H - 60}" '
            f'stroke="{INK}" stroke-width="0.25" stroke-dasharray="3 4" opacity="0.4"/>\n'
        )
    write("broadacre", "".join(body))


def mile_high() -> None:
    """Wright's Mile-High Illinois — a single tall needle."""
    body = [
        frame(
            "THE ILLINOIS / MILE-HIGH — WRIGHT, 1956", "CHICAGO: 1,609 M / 528 FLOORS"
        )
    ]
    gy = 450
    body.append(ground(gy))
    cx = W / 2
    base_w = 80
    top_w = 8
    body.append(
        f'  <path d="M {cx - base_w / 2} {gy} L {cx - top_w / 2} {60} '
        f'L {cx + top_w / 2} {60} L {cx + base_w / 2} {gy} Z" '
        f'fill="none" stroke="{INK}" stroke-width="1.2"/>\n'
    )
    # tripod bracing
    body.append(
        f'  <path d="M {cx - base_w / 2 - 10} {gy} L {cx} {gy - 80} L {cx + base_w / 2 + 10} {gy}" '
        f'fill="none" stroke="{INK}" stroke-width="0.7"/>\n'
    )
    # horizontal tick marks for floors
    for y in range(80, int(gy), 12):
        # interpolated width
        t = (y - 60) / (gy - 60)
        w = top_w + (base_w - top_w) * t
        body.append(
            f'  <line x1="{cx - w / 2}" y1="{y}" x2="{cx + w / 2}" y2="{y}" '
            f'stroke="{INK}" stroke-width="0.2" opacity="0.5"/>\n'
        )
    # antenna / spire
    body.append(
        f'  <line x1="{cx}" y1="{60}" x2="{cx}" y2="{40}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # a tiny skyline of "normal" skyscrapers beside it for scale comparison
    for i, h in enumerate([40, 55, 70, 60, 45]):
        x = 80 + i * 30
        body.append(
            f'  <rect x="{x}" y="{gy - h}" width="22" height="{h}" '
            f'fill="none" stroke="{INK}" stroke-width="0.5" opacity="0.6"/>\n'
        )
    body.append(human_figure(640, gy, 1.1))
    write("mile-high", "".join(body))


def palace_of_soviets() -> None:
    """Iofan's Palace of the Soviets — massive tiered base with colossal Lenin."""
    body = [frame("PALACE OF THE SOVIETS — IOFAN, 1933", "MOSCOW: 415 M WITH LENIN")]
    gy = 450
    body.append(ground(gy))
    cx = W / 2
    # tiered wedding-cake base
    tiers = [(360, 70), (300, 60), (240, 55), (180, 50), (140, 45), (100, 40), (60, 35)]
    cur_h = 0
    for w, h in tiers:
        body.append(
            f'  <rect x="{cx - w / 2}" y="{gy - cur_h - h}" width="{w}" height="{h}" '
            f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
        )
        # each tier gets vertical pilaster ticks
        for i in range(1, int(w // 15)):
            x = cx - w / 2 + i * 15
            body.append(
                f'  <line x1="{x}" y1="{gy - cur_h - h}" x2="{x}" y2="{gy - cur_h}" '
                f'stroke="{INK}" stroke-width="0.3" opacity="0.55"/>\n'
            )
        cur_h += h
    # Lenin silhouette on top (simplified)
    lenin_y = gy - cur_h
    body.append(
        f'  <circle cx="{cx}" cy="{lenin_y - 14}" r="8" fill="none" '
        f'stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(
        f'  <path d="M {cx - 14} {lenin_y - 5} L {cx - 14} {lenin_y - 40} '
        f"L {cx + 20} {lenin_y - 40} L {cx + 40} {lenin_y - 30} "
        f'L {cx + 14} {lenin_y - 5} Z" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    # raised arm gesturing
    body.append(
        f'  <line x1="{cx + 6}" y1="{lenin_y - 22}" x2="{cx + 44}" y2="{lenin_y - 55}" '
        f'stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(human_figure(640, gy, 1.2))
    write("palace-of-soviets", "".join(body))


def volkshalle() -> None:
    """Speer's Volkshalle — colossal dome."""
    body = [frame("VOLKSHALLE / GERMANIA — SPEER, 1937", "BERLIN: 290 M DOME")]
    gy = 440
    body.append(ground(gy))
    cx = W / 2
    # massive drum
    drum_w = 380
    drum_h = 80
    body.append(
        f'  <rect x="{cx - drum_w / 2}" y="{gy - drum_h}" width="{drum_w}" height="{drum_h}" '
        f'fill="none" stroke="{INK}" stroke-width="1.1"/>\n'
    )
    # portico columns on the drum
    for i in range(10):
        x = cx - drum_w / 2 + 30 + i * 36
        body.append(
            f'  <line x1="{x}" y1="{gy}" x2="{x}" y2="{gy - drum_h + 8}" '
            f'stroke="{INK}" stroke-width="1"/>\n'
        )
    # cornice
    body.append(
        f'  <rect x="{cx - drum_w / 2 - 6}" y="{gy - drum_h}" width="{drum_w + 12}" height="6" '
        f'fill="none" stroke="{INK}" stroke-width="0.8"/>\n'
    )
    # colossal dome
    dome_r = 170
    body.append(
        f'  <path d="M {cx - dome_r} {gy - drum_h} A {dome_r} {dome_r} 0 0 1 {cx + dome_r} {gy - drum_h}" '
        f'fill="none" stroke="{INK}" stroke-width="1.4"/>\n'
    )
    # dome ribs
    import math

    for a in range(15, 180, 20):
        x = cx + dome_r * math.cos(math.radians(a))
        y = (gy - drum_h) - dome_r * math.sin(math.radians(a))
        body.append(
            f'  <line x1="{cx}" y1="{gy - drum_h}" x2="{x:.1f}" y2="{y:.1f}" '
            f'stroke="{INK}" stroke-width="0.3" opacity="0.5"/>\n'
        )
    # oculus
    body.append(
        f'  <circle cx="{cx}" cy="{gy - drum_h - dome_r + 20}" r="12" '
        f'fill="none" stroke="{INK}" stroke-width="0.8"/>\n'
    )
    body.append(human_figure(640, gy, 0.9))
    write("volkshalle", "".join(body))


def dome_over_manhattan() -> None:
    """Fuller's Dome over Manhattan — a hemispherical grid over tall buildings."""
    body = [frame("DOME OVER MANHATTAN — BUCKMINSTER FULLER, 1960", "≈ 3 KM DIAMETER")]
    gy = 430
    body.append(ground(gy))
    cx = W / 2
    dome_r = 290
    # dome outline
    body.append(
        f'  <path d="M {cx - dome_r} {gy} A {dome_r} {dome_r * 0.75} 0 0 1 {cx + dome_r} {gy}" '
        f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    # geodesic grid — horizontal arcs and vertical meridians
    import math

    for i in range(1, 5):
        ry = dome_r * 0.75 * (i / 5)
        rx = dome_r * (math.sqrt(1 - (i / 5) ** 2))
        body.append(
            f'  <path d="M {cx - rx:.1f} {gy - dome_r * 0.75 + ry:.1f} '
            f'A {rx:.1f} {ry * 0.3:.1f} 0 0 1 {cx + rx:.1f} {gy - dome_r * 0.75 + ry:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="0.35" opacity="0.6"/>\n'
        )
    for a in range(-70, 71, 14):
        x = cx + dome_r * math.sin(math.radians(a))
        y_top = gy - dome_r * 0.75 * math.cos(math.radians(a))
        body.append(
            f'  <path d="M {cx} {gy - dome_r * 0.75} Q {x * 0.5 + cx * 0.5:.1f} {(y_top + gy - dome_r * 0.75) / 2:.1f} {x:.1f} {gy}" '
            f'fill="none" stroke="{INK}" stroke-width="0.35" opacity="0.55"/>\n'
        )
    # skyscrapers inside
    skyline = [
        (100, 90),
        (150, 130),
        (200, 110),
        (260, 160),
        (320, 180),
        (380, 150),
        (440, 170),
        (500, 140),
        (560, 120),
    ]
    for x, h in skyline:
        body.append(
            f'  <rect x="{x}" y="{gy - h}" width="28" height="{h}" '
            f'fill="none" stroke="{INK}" stroke-width="0.7"/>\n'
        )
    write("dome-over-manhattan", "".join(body))


def tokyo_bay() -> None:
    """Tange's Tokyo Bay Plan — linear spine over water with branching residential."""
    body = [frame("TOKYO BAY PLAN — KENZŌ TANGE, 1960", "METABOLIST MEGASTRUCTURE")]
    gy = 440
    body.append(ground(gy))
    # water line
    for x in range(40, W - 40, 16):
        body.append(
            f'  <path d="M {x} {gy + 5} Q {x + 4} {gy + 1} {x + 8} {gy + 5} '
            f'T {x + 16} {gy + 5}" fill="none" stroke="{INK}" stroke-width="0.3" opacity="0.5"/>\n'
        )
    # central highway spine (two parallel lines)
    body.append(
        f'  <line x1="60" y1="{gy - 70}" x2="{W - 60}" y2="{gy - 70}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(
        f'  <line x1="60" y1="{gy - 90}" x2="{W - 60}" y2="{gy - 90}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # support piers
    for x in range(90, W - 60, 60):
        body.append(
            f'  <line x1="{x}" y1="{gy - 90}" x2="{x}" y2="{gy}" '
            f'stroke="{INK}" stroke-width="0.8"/>\n'
        )
    # A-frame residential bridges above the spine
    for x in [120, 240, 360, 480, 600]:
        body.append(
            f'  <line x1="{x - 40}" y1="{gy - 90}" x2="{x}" y2="{gy - 250}" '
            f'stroke="{INK}" stroke-width="1"/>\n'
        )
        body.append(
            f'  <line x1="{x + 40}" y1="{gy - 90}" x2="{x}" y2="{gy - 250}" '
            f'stroke="{INK}" stroke-width="1"/>\n'
        )
        # cross-bars (residential decks)
        for y in range(int(gy - 230), int(gy - 90), 25):
            t = ((gy - 90) - y) / 160
            w = 40 * (1 - t)
            body.append(
                f'  <line x1="{x - w:.1f}" y1="{y}" x2="{x + w:.1f}" y2="{y}" '
                f'stroke="{INK}" stroke-width="0.4" opacity="0.7"/>\n'
            )
    write("tokyo-bay", "".join(body))


def fun_palace() -> None:
    """Cedric Price's Fun Palace — steel frame with cranes."""
    body = [frame("FUN PALACE — CEDRIC PRICE, 1961", "LONDON: UNBUILT INDETERMINATE")]
    gy = 440
    body.append(ground(gy))
    # steel gantry frame
    frame_x0, frame_x1 = 80, W - 80
    frame_y_top = 140
    frame_y_bot = gy - 40
    # uprights
    for x in [frame_x0, 240, 360, 480, frame_x1]:
        body.append(
            f'  <line x1="{x}" y1="{frame_y_top}" x2="{x}" y2="{gy}" '
            f'stroke="{INK}" stroke-width="1"/>\n'
        )
    # top chord
    body.append(
        f'  <line x1="{frame_x0}" y1="{frame_y_top}" x2="{frame_x1}" y2="{frame_y_top}" '
        f'stroke="{INK}" stroke-width="1.2"/>\n'
    )
    # bottom chord
    body.append(
        f'  <line x1="{frame_x0}" y1="{frame_y_bot}" x2="{frame_x1}" y2="{frame_y_bot}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # diagonal bracing
    for x0, x1 in [(80, 240), (240, 360), (360, 480), (480, 560), (560, 640)]:
        body.append(
            f'  <line x1="{x0}" y1="{frame_y_bot}" x2="{x1}" y2="{frame_y_top}" '
            f'stroke="{INK}" stroke-width="0.45" opacity="0.6"/>\n'
        )
        body.append(
            f'  <line x1="{x0}" y1="{frame_y_top}" x2="{x1}" y2="{frame_y_bot}" '
            f'stroke="{INK}" stroke-width="0.45" opacity="0.6"/>\n'
        )
    # gantry crane on top (the signature of Price's indeterminate plan)
    crane_x = 360
    body.append(
        f'  <rect x="{crane_x - 30}" y="{frame_y_top - 30}" width="60" height="18" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(
        f'  <line x1="{crane_x}" y1="{frame_y_top - 30}" x2="{crane_x}" y2="{frame_y_top - 65}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(
        f'  <line x1="{crane_x - 80}" y1="{frame_y_top - 65}" x2="{crane_x + 80}" y2="{frame_y_top - 65}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(
        f'  <line x1="{crane_x - 80}" y1="{frame_y_top - 65}" x2="{crane_x - 60}" y2="{frame_y_top - 20}" '
        f'stroke="{INK}" stroke-width="0.6" opacity="0.7"/>\n'
    )
    body.append(
        f'  <line x1="{crane_x + 80}" y1="{frame_y_top - 65}" x2="{crane_x + 60}" y2="{frame_y_top - 20}" '
        f'stroke="{INK}" stroke-width="0.6" opacity="0.7"/>\n'
    )
    # suspended activity modules inside (ambiguous rectangles hanging)
    for i, (x, y, w, h) in enumerate(
        [
            (150, frame_y_top + 30, 90, 50),
            (280, frame_y_top + 60, 80, 70),
            (410, frame_y_top + 40, 100, 60),
            (550, frame_y_top + 80, 70, 40),
        ]
    ):
        body.append(
            f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="none" stroke="{INK}" stroke-width="0.7"/>\n'
        )
        # suspension lines
        body.append(
            f'  <line x1="{x + 10}" y1="{y}" x2="{x + 10}" y2="{frame_y_top}" '
            f'stroke="{INK}" stroke-width="0.3" opacity="0.6" stroke-dasharray="3 3"/>\n'
        )
        body.append(
            f'  <line x1="{x + w - 10}" y1="{y}" x2="{x + w - 10}" y2="{frame_y_top}" '
            f'stroke="{INK}" stroke-width="0.3" opacity="0.6" stroke-dasharray="3 3"/>\n'
        )
    write("fun-palace", "".join(body))


def walking_city() -> None:
    """Archigram's Walking City — insectoid capsules on telescoping legs."""
    body = [
        frame("WALKING CITY — ARCHIGRAM / HERRON, 1964", "AMBULATORY MEGASTRUCTURE")
    ]
    gy = 440
    body.append(ground(gy))

    # two walking creatures
    def creature(cx: float, scale: float = 1.0) -> list[str]:
        s = scale
        parts = []
        body_w = 160 * s
        body_h = 100 * s
        cy = 230
        # rounded ovoid body
        parts.append(
            f'  <ellipse cx="{cx}" cy="{cy}" rx="{body_w / 2}" ry="{body_h / 2}" '
            f'fill="none" stroke="{INK}" stroke-width="1.2"/>\n'
        )
        # windows/portholes — grid across the belly
        for ix in range(-3, 4):
            for iy in range(-1, 2):
                x = cx + ix * 18 * s
                y = cy + iy * 18 * s
                parts.append(
                    f'  <circle cx="{x}" cy="{y}" r="{4 * s:.1f}" '
                    f'fill="none" stroke="{INK}" stroke-width="0.5" opacity="0.8"/>\n'
                )
        # chimneys / comms on top
        for i in range(3):
            x = cx - 30 * s + i * 30 * s
            parts.append(
                f'  <line x1="{x}" y1="{cy - body_h / 2 - 8 * s}" x2="{x}" y2="{cy - body_h / 2 + 4 * s}" '
                f'stroke="{INK}" stroke-width="1"/>\n'
            )
        # legs (telescoping) — four
        for i, off in enumerate([-50, -20, 20, 50]):
            lx0 = cx + off * s
            ly0 = cy + body_h / 2 * 0.8
            # joint halfway
            lx1 = lx0 + (i - 1.5) * 12 * s
            ly1 = ly0 + 60 * s
            parts.append(
                f'  <line x1="{lx0}" y1="{ly0}" x2="{lx1}" y2="{ly1}" '
                f'stroke="{INK}" stroke-width="1.4"/>\n'
            )
            parts.append(
                f'  <line x1="{lx1}" y1="{ly1}" x2="{lx0 + (i - 1.5) * 24 * s}" y2="{gy}" '
                f'stroke="{INK}" stroke-width="1.4"/>\n'
            )
            # telescoping rings on legs
            for t in (0.3, 0.55, 0.8):
                tx = lx0 + t * ((lx1) - lx0)
                ty = ly0 + t * (ly1 - ly0)
                parts.append(
                    f'  <line x1="{tx - 4}" y1="{ty}" x2="{tx + 4}" y2="{ty}" '
                    f'stroke="{INK}" stroke-width="0.6"/>\n'
                )
        return parts

    body.extend(creature(220, 0.9))
    body.extend(creature(520, 1.0))
    # distant city — small blocks on horizon
    for i, (x, h) in enumerate([(330, 40), (360, 50), (390, 45), (420, 55)]):
        body.append(
            f'  <rect x="{x}" y="{gy - h}" width="20" height="{h}" '
            f'fill="none" stroke="{INK}" stroke-width="0.5" opacity="0.5"/>\n'
        )
    write("walking-city", "".join(body))


def plug_in_city() -> None:
    """Archigram's Plug-in City — lattice of capsules with crane rails."""
    body = [frame("PLUG-IN CITY — ARCHIGRAM / COOK, 1964", "CAPSULE METABOLISM")]
    gy = 440
    body.append(ground(gy))
    # diagonal megastructure grid
    top_y = 90
    # big diagonal frames
    for i in range(5):
        x_start = 80 + i * 130
        body.append(
            f'  <line x1="{x_start}" y1="{gy}" x2="{x_start + 80}" y2="{top_y}" '
            f'stroke="{INK}" stroke-width="1.1"/>\n'
        )
        body.append(
            f'  <line x1="{x_start}" y1="{top_y}" x2="{x_start + 80}" y2="{gy}" '
            f'stroke="{INK}" stroke-width="1.1"/>\n'
        )
    # horizontal service decks
    for y in [gy - 60, gy - 160, gy - 260]:
        body.append(
            f'  <line x1="80" y1="{y}" x2="{W - 80}" y2="{y}" '
            f'stroke="{INK}" stroke-width="0.9"/>\n'
        )
    # capsules plugged in at various cells
    import random

    random.seed(42)
    for row_y in (gy - 50, gy - 150, gy - 250):
        for i in range(12):
            if random.random() < 0.75:
                x = 90 + i * 45
                cw = random.choice([30, 40])
                ch = random.choice([26, 32])
                body.append(
                    f'  <rect x="{x}" y="{row_y - ch}" width="{cw}" height="{ch}" '
                    f'fill="none" stroke="{INK}" stroke-width="0.6"/>\n'
                )
                # porthole
                body.append(
                    f'  <circle cx="{x + cw * 0.3:.1f}" cy="{row_y - ch * 0.5:.1f}" r="2.5" '
                    f'fill="none" stroke="{INK}" stroke-width="0.4"/>\n'
                )
    # crane rail on top
    body.append(
        f'  <line x1="80" y1="{top_y}" x2="{W - 80}" y2="{top_y}" '
        f'stroke="{INK}" stroke-width="1.2"/>\n'
    )
    # a crane
    body.append(
        f'  <rect x="300" y="{top_y - 30}" width="50" height="15" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    body.append(
        f'  <line x1="325" y1="{top_y - 30}" x2="325" y2="{top_y - 80}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    body.append(
        f'  <line x1="280" y1="{top_y - 80}" x2="420" y2="{top_y - 80}" '
        f'stroke="{INK}" stroke-width="1"/>\n'
    )
    # hanging capsule (being lowered into place)
    body.append(
        f'  <line x1="400" y1="{top_y - 80}" x2="400" y2="{top_y - 30}" '
        f'stroke="{INK}" stroke-width="0.4" stroke-dasharray="3 3"/>\n'
    )
    body.append(
        f'  <rect x="390" y="{top_y - 30}" width="22" height="18" '
        f'fill="none" stroke="{INK}" stroke-width="0.6"/>\n'
    )
    write("plug-in-city", "".join(body))


def continuous_monument() -> None:
    """Superstudio's Continuous Monument — infinite gridded monolith over landscape."""
    body = [frame("CONTINUOUS MONUMENT — SUPERSTUDIO, 1969", "GLOBAL GRID")]
    gy = 440
    body.append(ground(gy))
    # continuous monolith extending off both edges
    bar_y_top = 140
    bar_y_bot = gy - 50
    # left edge off-canvas, right edge off-canvas
    body.append(
        f'  <rect x="0" y="{bar_y_top}" width="{W}" height="{bar_y_bot - bar_y_top}" '
        f'fill="none" stroke="{INK}" stroke-width="1.2"/>\n'
    )
    # grid inside — horizontal lines
    for y in range(bar_y_top + 20, int(bar_y_bot), 20):
        body.append(
            f'  <line x1="0" y1="{y}" x2="{W}" y2="{y}" '
            f'stroke="{INK}" stroke-width="0.3" opacity="0.6"/>\n'
        )
    # vertical lines with perspective feel
    for x in range(0, W, 36):
        body.append(
            f'  <line x1="{x}" y1="{bar_y_top}" x2="{x}" y2="{bar_y_bot}" '
            f'stroke="{INK}" stroke-width="0.3" opacity="0.6"/>\n'
        )
    # arrows at edges suggesting continuation
    for x_edge, direction in [(4, -1), (W - 4, 1)]:
        body.append(
            f'  <path d="M {x_edge} {(bar_y_top + bar_y_bot) / 2} '
            f'l {direction * 12} -8 l 0 16 Z" fill="{INK}"/>\n'
        )
    # landscape beneath — tiny trees and mountains
    for x in [80, 150, 280, 380, 540, 620]:
        body.append(
            f'  <path d="M {x - 6} {gy} L {x} {gy - 12} L {x + 6} {gy}" '
            f'fill="none" stroke="{INK}" stroke-width="0.5" opacity="0.7"/>\n'
        )
    # distant mountains
    body.append(
        f'  <path d="M 40 {gy - 20} L 120 {gy - 50} L 200 {gy - 30} '
        f"L 280 {gy - 60} L 360 {gy - 35} L 440 {gy - 65} "
        f'L 520 {gy - 30} L 600 {gy - 55} L 680 {gy - 25}" '
        f'fill="none" stroke="{INK}" stroke-width="0.5" opacity="0.6"/>\n'
    )
    write("continuous-monument", "".join(body))


def mega_city_pyramid() -> None:
    """Shimizu's Mega-City Pyramid — octahedron or truss-pyramid over Tokyo Bay."""
    body = [frame("MEGA-CITY PYRAMID / TRY 2004 — SHIMIZU, 1989", "TOKYO BAY: 2,004 M")]
    gy = 440
    body.append(ground(gy))
    cx = W / 2
    # triangular pyramid outline
    base_w = 440
    apex_y = 80
    body.append(
        f'  <path d="M {cx - base_w / 2} {gy} L {cx} {apex_y} L {cx + base_w / 2} {gy} Z" '
        f'fill="none" stroke="{INK}" stroke-width="1.2"/>\n'
    )
    # interior tetrahedral lattice — simplified as triangular grid
    # horizontal levels
    levels = 6
    for i in range(1, levels):
        t = i / levels
        left_x = cx - base_w / 2 + t * (base_w / 2)
        right_x = cx + base_w / 2 - t * (base_w / 2)
        y = gy - t * (gy - apex_y)
        body.append(
            f'  <line x1="{left_x:.1f}" y1="{y:.1f}" x2="{right_x:.1f}" y2="{y:.1f}" '
            f'stroke="{INK}" stroke-width="0.4" opacity="0.5"/>\n'
        )
        # zigzag inner bracing
        segments = 6 - i
        for j in range(segments):
            x0 = left_x + j * (right_x - left_x) / segments
            x1 = left_x + (j + 1) * (right_x - left_x) / segments
            body.append(
                f'  <line x1="{x0:.1f}" y1="{y:.1f}" x2="{(x0 + x1) / 2:.1f}" y2="{y - (gy - apex_y) / levels:.1f}" '
                f'stroke="{INK}" stroke-width="0.3" opacity="0.5"/>\n'
            )
            body.append(
                f'  <line x1="{x1:.1f}" y1="{y:.1f}" x2="{(x0 + x1) / 2:.1f}" y2="{y - (gy - apex_y) / levels:.1f}" '
                f'stroke="{INK}" stroke-width="0.3" opacity="0.5"/>\n'
            )
    # internal spherical modules (cities) at lattice nodes
    for i in range(1, 4):
        t = i / 4
        y = gy - t * (gy - apex_y) - 30
        xs = [cx - (base_w / 2) * (1 - t) * 0.6, cx, cx + (base_w / 2) * (1 - t) * 0.6]
        for x in xs:
            body.append(
                f'  <circle cx="{x}" cy="{y}" r="12" fill="{PAPER}" '
                f'stroke="{INK}" stroke-width="0.8"/>\n'
            )
    # water base
    for x in range(50, W - 50, 15):
        body.append(
            f'  <path d="M {x} {gy + 5} Q {x + 4} {gy + 1} {x + 8} {gy + 5}" '
            f'fill="none" stroke="{INK}" stroke-width="0.3" opacity="0.5"/>\n'
        )
    body.append(human_figure(660, gy, 0.8))
    write("mega-city-pyramid", "".join(body))


def cardiff_opera() -> None:
    """Hadid's Cardiff Bay Opera House — angular crystalline volumes."""
    body = [
        frame(
            "CARDIFF BAY OPERA HOUSE — ZAHA HADID, 1994", "COMPETITION-WINNING, UNBUILT"
        )
    ]
    gy = 440
    body.append(ground(gy))
    # a collision of sharp wedges, Hadid's deconstructivist signature
    # main opera volume — tilted prism
    body.append(
        f'  <polygon points="140,{gy} 260,{gy - 180} 400,{gy - 200} 460,{gy - 120} 420,{gy}" '
        f'fill="none" stroke="{INK}" stroke-width="1.2"/>\n'
    )
    # wedge roof planes
    body.append(
        f'  <polygon points="260,{gy - 180} 400,{gy - 200} 380,{gy - 240} 290,{gy - 220}" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    # foyer / entry block
    body.append(
        f'  <polygon points="420,{gy} 460,{gy - 120} 560,{gy - 80} 580,{gy}" '
        f'fill="none" stroke="{INK}" stroke-width="1"/>\n'
    )
    # sharp cantilevered fin
    body.append(
        f'  <polygon points="560,{gy - 80} 640,{gy - 140} 620,{gy - 150} 540,{gy - 100}" '
        f'fill="none" stroke="{INK}" stroke-width="0.9"/>\n'
    )
    # internal suggestions — glazing lines
    for x0, y0, x1, y1 in [
        (160, gy - 20, 250, gy - 170),
        (180, gy - 40, 260, gy - 160),
        (200, gy - 60, 270, gy - 150),
        (280, gy - 190, 390, gy - 205),
        (300, gy - 170, 400, gy - 190),
    ]:
        body.append(
            f'  <line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" '
            f'stroke="{INK}" stroke-width="0.4" opacity="0.55"/>\n'
        )
    # plaza ground markings
    for x in range(60, 140, 15):
        body.append(
            f'  <line x1="{x}" y1="{gy}" x2="{x + 8}" y2="{gy - 3}" '
            f'stroke="{INK}" stroke-width="0.3" opacity="0.45"/>\n'
        )
    body.append(human_figure(670, gy, 1.0))
    write("cardiff-opera", "".join(body))


def crystal_island() -> None:
    """Foster's Crystal Island Moscow — a tented conical glass envelope."""
    body = [
        frame("CRYSTAL ISLAND — FOSTER + PARTNERS, 2007", "MOSCOW: 450 M, 2.5 M² FLOOR")
    ]
    gy = 440
    body.append(ground(gy))
    cx = W / 2
    # conical/tented envelope
    apex_y = 70
    base_w = 400
    body.append(
        f'  <path d="M {cx - base_w / 2} {gy} Q {cx - base_w / 4} {gy - 280} {cx} {apex_y} '
        f'Q {cx + base_w / 4} {gy - 280} {cx + base_w / 2} {gy}" '
        f'fill="none" stroke="{INK}" stroke-width="1.3"/>\n'
    )
    # grid pattern on the envelope
    import math

    for i in range(1, 12):
        t = i / 12
        left_x = cx - base_w / 2 * (1 - t)
        right_x = cx + base_w / 2 * (1 - t)
        y = gy - t * (gy - apex_y) * 1.0
        # curved horizontal band (ellipse segment)
        body.append(
            f'  <path d="M {left_x:.1f} {y:.1f} Q {cx} {y - 10:.1f} {right_x:.1f} {y:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="0.3" opacity="0.55"/>\n'
        )
    # vertical spokes
    for a in range(-70, 71, 12):
        x_base = cx + (base_w / 2) * math.sin(math.radians(a))
        body.append(
            f'  <path d="M {x_base:.1f} {gy} Q {cx + (x_base - cx) * 0.4:.1f} {(gy + apex_y) / 2:.1f} {cx} {apex_y}" '
            f'fill="none" stroke="{INK}" stroke-width="0.3" opacity="0.5"/>\n'
        )
    # human settlement inside suggested as small blocks
    for i, (x, h) in enumerate([(280, 35), (320, 55), (360, 45), (400, 40), (440, 50)]):
        body.append(
            f'  <rect x="{x}" y="{gy - h}" width="24" height="{h}" '
            f'fill="none" stroke="{INK}" stroke-width="0.5" opacity="0.75"/>\n'
        )
    body.append(human_figure(660, gy, 1.0))
    write("crystal-island", "".join(body))


# ===========================================================================
# Main entry point
# ===========================================================================

ALL = [
    babel,
    sforzinda,
    ideal_city,
    newton_cenotaph,
    chaux,
    soane_royal_palace,
    citta_nuova,
    hotel_attraction,
    tribune_column,
    tatlin,
    ferriss,
    plan_voisin,
    broadacre,
    mile_high,
    palace_of_soviets,
    volkshalle,
    dome_over_manhattan,
    tokyo_bay,
    fun_palace,
    walking_city,
    plug_in_city,
    continuous_monument,
    mega_city_pyramid,
    cardiff_opera,
    crystal_island,
]


if __name__ == "__main__":
    for f in ALL:
        f()
    print(f"\n{len(ALL)} illustrations written to {OUT}")
