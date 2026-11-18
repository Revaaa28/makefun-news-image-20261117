#!/usr/bin/env python3
"""Compose the entry image for make.fun news-image-20261117.

A one-page broadsheet summing up Tuesday 17 November 2026: a dotted
world map with numbered story pins, one hero story, three pictured
panels and nine one-line briefs. Every letter is rendered by code
(DejaVu); every illustration is drawn with PIL shapes in this file.
No photos, no copied artwork.

Run: python3 compose.py  -> writes entry.png next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 30, 30)
NAVY = (28, 52, 88)
GREY = (90, 86, 78)
LIGHT = (255, 255, 255)
SKY = (168, 205, 232)
SEA = (62, 110, 150)
SAND = (226, 205, 160)
RULE = (180, 172, 155)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, max_w, lines, fnt, fill, leading=None):
    """Draw lines; returns y just below the last line."""
    lh = leading if leading is not None else int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- scenes
def scene_bridge(d, x, y, w, h):
    """Kerch bridge over the strait, explosion burst mid-span."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA)
    # sun
    d.ellipse([x + w - 52, y + 10, x + w - 22, y + 40], fill=(250, 214, 120))
    # bridge deck + arch
    deck = int(h * 0.52)
    d.rectangle([x, y + deck, x + w, y + deck + 8], fill=(60, 60, 66))
    d.arc([x + int(w * 0.18), y + deck - 44, x + int(w * 0.82), y + deck + 30],
          start=180, end=360, fill=(60, 60, 66), width=6)
    for px in (0.22, 0.38, 0.62, 0.78):
        px0 = x + int(w * px)
        d.rectangle([px0, y + deck + 8, px0 + 6, y + h], fill=(70, 70, 76))
    # explosion burst on the deck
    cx, cy = x + int(w * 0.55), y + deck - 6
    for r, col in ((26, (255, 170, 40)), (18, (255, 110, 30)), (10, (255, 220, 90))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x1 = cx + int(22 * math.cos(a))
        y1 = cy + int(22 * math.sin(a))
        x2 = cx + int(34 * math.cos(a))
        y2 = cy + int(34 * math.sin(a))
        d.line([x1, y1, x2, y2], fill=(255, 170, 40), width=4)
    # smoke puffs
    for sx, sy, sr in ((0.46, 0.26, 12), (0.55, 0.18, 15), (0.63, 0.26, 11)):
        d.ellipse([x + int(w * sx) - sr, y + int(h * sy) - sr,
                   x + int(w * sx) + sr, y + int(h * sy) + sr],
                  fill=(90, 90, 90))


def scene_radar(d, x, y, w, h):
    """Radar dish + drone over a desert base at dusk."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 196, 150))
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(198, 158, 110))
    # radar dish
    cx, cy = x + int(w * 0.32), y + int(h * 0.55)
    d.pieslice([cx - 42, cy - 42, cx + 42, cy + 42], start=200, end=340,
               fill=(240, 240, 235))
    d.line([cx, cy, cx + 26, cy - 40], fill=(90, 90, 90), width=4)
    d.line([cx, cy, cx, y + int(h * 0.72)], fill=(70, 70, 70), width=6)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    # signal arcs
    for r in (52, 66):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=250, end=330,
              fill=(176, 30, 30), width=3)
    # drone
    dx, dy = x + int(w * 0.74), y + int(h * 0.28)
    d.ellipse([dx - 22, dy - 6, dx - 10, dy + 6], fill=(50, 50, 50))
    d.ellipse([dx + 10, dy - 6, dx + 22, dy + 6], fill=(50, 50, 50))
    d.rectangle([dx - 12, dy - 3, dx + 12, dy + 5], fill=(40, 40, 40))
    d.line([dx - 26, dy - 10, dx - 6, dy - 10], fill=(60, 60, 60), width=2)
    d.line([dx + 6, dy - 10, dx + 26, dy - 10], fill=(60, 60, 60), width=2)
    d.line([dx, dy + 5, dx, dy + 22], fill=(60, 60, 60), width=2)


def scene_ballot(d, x, y, w, h):
    """Ballot box with a ballot paper and a red check."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    bx, by = x + int(w * 0.30), y + int(h * 0.42)
    bw, bh = int(w * 0.42), int(h * 0.42)
    d.rectangle([bx, by, bx + bw, by + bh], fill=(52, 84, 130))
    d.rectangle([bx - 6, by - 12, bx + bw + 6, by], fill=(36, 62, 98))
    d.rectangle([bx + int(bw * 0.36), by - 12, bx + int(bw * 0.64), by - 6],
                fill=(20, 20, 20))
    # ballot paper going in
    d.polygon([(bx + 8, by - 46), (bx + int(bw * 0.55), by - 58),
               (bx + int(bw * 0.62), by - 16), (bx + 16, by - 8)],
              fill=(255, 255, 255), outline=(120, 120, 120))
    # red check
    cx, cy = x + int(w * 0.76), y + int(h * 0.30)
    d.line([cx - 18, cy, cx - 4, cy + 16], fill=RED, width=7)
    d.line([cx - 4, cy + 16, cx + 22, cy - 18], fill=RED, width=7)


def scene_yemen(d, x, y, w, h):
    """Desert dunes, mountains and a road marker toward Aden."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 214, 170))
    d.ellipse([x + w - 46, y + 8, x + w - 16, y + 38], fill=(250, 214, 120))
    d.polygon([(x, y + h), (x + int(w * 0.35), y + int(h * 0.30)),
               (x + int(w * 0.62), y + h)], fill=(150, 110, 70))
    d.polygon([(x + int(w * 0.45), y + h), (x + int(w * 0.72), y + int(h * 0.42)),
               (x + w, y + h)], fill=(128, 92, 58))
    d.polygon([(x, y + int(h * 0.78)), (x + int(w * 0.5), y + int(h * 0.66)),
               (x + w, y + int(h * 0.82)), (x + w, y + h), (x, y + h)],
              fill=(206, 164, 108))
    # road + marker
    d.line([x + int(w * 0.12), y + h, x + int(w * 0.55), y + int(h * 0.66)],
           fill=(90, 70, 50), width=5)
    mx, my = x + int(w * 0.68), y + int(h * 0.52)
    d.line([mx, my, mx, my - 26], fill=(60, 60, 60), width=4)
    d.polygon([(mx, my - 26), (mx + 26, my - 19), (mx, my - 12)], fill=RED)


def scene_jet(d, x, y, w, h):
    """Fighter jet silhouette crossing a pale sky."""
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 238))
    for cx0, cy0, cr in ((0.18, 0.72, 26), (0.55, 0.80, 32), (0.85, 0.66, 22)):
        d.ellipse([x + int(w * cx0) - cr, y + int(h * cy0) - cr // 2,
                   x + int(w * cx0) + cr, y + int(h * cy0) + cr // 2],
                  fill=(255, 255, 255))
    jx, jy = x + int(w * 0.50), y + int(h * 0.42)
    d.polygon([(jx - 70, jy + 4), (jx + 10, jy - 6), (jx + 78, jy),
               (jx + 10, jy + 8)], fill=(52, 62, 78))
    d.polygon([(jx - 10, jy - 4), (jx + 22, jy - 34), (jx + 34, jy - 4)],
              fill=(52, 62, 78))
    d.polygon([(jx - 10, jy + 6), (jx + 22, jy + 36), (jx + 34, jy + 6)],
              fill=(52, 62, 78))
    d.polygon([(jx - 66, jy + 2), (jx - 40, jy - 16), (jx - 34, jy + 2)],
              fill=(52, 62, 78))
    d.line([jx - 72, jy + 4, jx - 96, jy + 4], fill=(255, 170, 40), width=4)


def scene_flags(d, x, y, w, h):
    """Two flags on poles: China and Canada, shaking hands below."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
    # China flag
    fx, fy, fw, fh = x + int(w * 0.10), y + int(h * 0.16), int(w * 0.34), int(h * 0.42)
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    d.polygon([(fx + 10, fy + 8), (fx + 14, fy + 16), (fx + 22, fy + 16),
               (fx + 16, fy + 21), (fx + 18, fy + 29), (fx + 10, fy + 24),
               (fx + 2, fy + 29), (fx + 4, fy + 21), (fx - 2, fy + 16),
               (fx + 6, fy + 16)], fill=(255, 222, 0))
    d.line([fx, fy, fx, fy + fh + 26], fill=(70, 70, 70), width=4)
    # Canada flag
    gx = x + int(w * 0.56)
    d.rectangle([gx, fy, gx + fw, fy + fh], fill=(255, 255, 255),
                outline=(200, 0, 0), width=2)
    d.rectangle([gx, fy, gx + int(fw * 0.25), fy + fh], fill=(255, 0, 0))
    d.rectangle([gx + int(fw * 0.75), fy, gx + fw, fy + fh], fill=(255, 0, 0))
    d.ellipse([gx + int(fw * 0.38), fy + int(fh * 0.30),
               gx + int(fw * 0.62), fy + int(fh * 0.72)], fill=(255, 0, 0))
    d.line([gx, fy, gx, fy + fh + 26], fill=(70, 70, 70), width=4)
    # handshake arc
    d.arc([x + int(w * 0.30), y + int(h * 0.66), x + int(w * 0.70), y + h + 8],
          start=180, end=360, fill=(52, 84, 130), width=5)


def scene_chip(d, x, y, w, h):
    """A microchip on a circuit board."""
    d.rectangle([x, y, x + w, y + h], fill=(26, 46, 66))
    for i in range(5):
        yy = y + int(h * (0.16 + i * 0.17))
        d.line([x + 8, yy, x + w - 8, yy], fill=(58, 96, 130), width=2)
    cx, cy = x + w // 2, y + h // 2
    cw, ch = int(w * 0.44), int(h * 0.52)
    for i in range(4):
        px = cx - cw // 2 + int((i + 0.5) * cw / 4)
        d.line([px, cy - ch // 2 - 12, px, cy - ch // 2], fill=(200, 200, 200), width=3)
        d.line([px, cy + ch // 2, px, cy + ch // 2 + 12], fill=(200, 200, 200), width=3)
    d.rectangle([cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2],
                fill=(40, 40, 44), outline=(180, 180, 180), width=3)
    d.rectangle([cx - cw // 4, cy - ch // 4, cx + cw // 4, cy + ch // 4],
                fill=(80, 140, 190))
    d.text((cx - 5, cy - 8), "AI", font=font(SANS_B, 16), fill=LIGHT)


def scene_magnifier(d, x, y, w, h):
    """Magnifying glass over a document."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 230, 216))
    dx, dy, dw, dh = x + int(w * 0.14), y + int(h * 0.12), int(w * 0.72), int(h * 0.76)
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=(255, 255, 255),
                outline=(150, 140, 120), width=2)
    for i in range(4):
        yy = dy + 14 + i * 16
        d.line([dx + 12, yy, dx + dw - 12, yy], fill=(170, 165, 150), width=4)
    cx, cy = x + int(w * 0.58), y + int(h * 0.46)
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(190, 220, 240),
              outline=(40, 40, 40), width=5)
    d.line([cx + 24, cy + 24, cx + 52, cy + 52], fill=(40, 40, 40), width=7)
    d.text((cx - 8, cy - 12), "?", font=font(SANS_B, 26), fill=NAVY)


def scene_bus(d, x, y, w, h):
    """Mountain road with a bus on a cliff edge."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 232))
    d.polygon([(x, y + h), (x + int(w * 0.30), y + int(h * 0.18)),
               (x + int(w * 0.58), y + h)], fill=(110, 130, 110))
    d.polygon([(x + int(w * 0.42), y + h), (x + int(w * 0.74), y + int(h * 0.28)),
               (x + w, y + h)], fill=(90, 110, 92))
    d.polygon([(x, y + int(h * 0.74)), (x + int(w * 0.45), y + int(h * 0.62)),
               (x + w, y + int(h * 0.70)), (x + w, y + h), (x, y + h)],
              fill=(140, 130, 100))
    # winding road
    d.line([x + int(w * 0.08), y + int(h * 0.78), x + int(w * 0.45), y + int(h * 0.66),
            x + int(w * 0.80), y + int(h * 0.74)], fill=(70, 66, 60), width=7)
    # bus
    bx, by = x + int(w * 0.34), y + int(h * 0.44)
    d.rectangle([bx, by, bx + 74, by + 26], fill=(222, 160, 40))
    d.rectangle([bx + 8, by + 5, bx + 66, by + 14], fill=(180, 220, 240))
    d.ellipse([bx + 12, by + 24, bx + 24, by + 34], fill=(30, 30, 30))
    d.ellipse([bx + 52, by + 24, bx + 64, by + 34], fill=(30, 30, 30))


def scene_stamp(d, x, y, w, h):
    """A red sanction stamp over a document."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 230, 216))
    dx, dy, dw, dh = x + int(w * 0.16), y + int(h * 0.10), int(w * 0.68), int(h * 0.80)
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=(255, 255, 255),
                outline=(150, 140, 120), width=2)
    for i in range(3):
        yy = dy + 14 + i * 15
        d.line([dx + 12, yy, dx + dw - 12, yy], fill=(170, 165, 150), width=4)
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], outline=RED, width=5)
    d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], outline=RED, width=2)
    d.text((cx - 34, cy - 9), "BANNED", font=font(SANS_B, 15), fill=RED)


SCENES = {
    "bridge": scene_bridge, "radar": scene_radar, "ballot": scene_ballot,
    "yemen": scene_yemen, "jet": scene_jet, "flags": scene_flags,
    "chip": scene_chip, "magnifier": scene_magnifier, "bus": scene_bus,
    "stamp": scene_stamp,
}

# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "EUROPE  ·  WAR",
    "headline": "Kyiv hits the Crimea bridge again",
    "summary": ("Ukraine struck the Kerch bridge for a second day running, "
                "severely damaging the span, Kyiv says."),
    "scene": "bridge",
}

PANELS = [
    {"kicker": "MIDDLE EAST  ·  GULF", "headline": "Iran fires drones at US radar in Bahrain",
     "summary": ("Tehran says it hit a US radar in Bahrain; Bahrain says "
                  "it was intercepted, with no casualties."),
     "scene": "radar"},
    {"kicker": "MIDDLE EAST  ·  POLITICS", "headline": "Netanyahu aides 'tipped police' before vote",
     "summary": ("A TV probe says the PM's chief of staff tipped police "
                  "before the dawn arrests of Arab activists."),
     "scene": "ballot"},
    {"kicker": "MIDDLE EAST  ·  WAR", "headline": "Houthis close in on Aden",
     "summary": ("Houthi rebels are reported within 60 km of Aden after "
                  "government forces fell back from the coast."),
     "scene": "yemen"},
]

BRIEFS = [
    {"num": 5, "place": "JAPAN",
     "text": "Jets scrambled as two suspected Russian aircraft enter Japanese airspace; Tokyo protests."},
    {"num": 6, "place": "CHINA–CANADA",
     "text": "Xi and Carney pledge further tariff cuts and closer ties in leaders' talks today."},
    {"num": 7, "place": "SOUTHEAST ASIA",
     "text": "US tightens AI-chip sales to regional data centres; Singapore seeks trusted access."},
    {"num": 8, "place": "UNITED STATES",
     "text": "Forensic expert concludes Epstein's prison death was homicide, not suicide."},
    {"num": 9, "place": "INDIA",
     "text": "Bus plunges into a ravine in Uttarakhand; at least six dead and 20 hurt."},
    {"num": 10, "place": "BRITAIN",
     "text": "London sanctions eight firms building West Bank settlements, and a group blocking aid to Gaza."},
    {"num": 11, "place": "GAZA",
     "text": "UK, Australia, Canada and Italy press Israel to open crossings for aid."},
    {"num": 12, "place": "JERICHO",
     "text": "Israeli settlers kill a 72-year-old woman, Palestinians say."},
    {"num": 13, "place": "KYIV",
     "text": "Russia answers the bridge strike with attacks on the capital's river crossings."},
]

# ------------------------------------------------------------- world map
# Dotted world map: a 72 x 28 ASCII landmask, '#' is land, '.' is sea.
# Equirectangular: column c spans longitude -180+5c .. -175+5c; row r
# spans latitude 82-5.07r .. 82-5.07(r+1). Continents are drawn a touch
# tall to offset the wide, short panel.
MAP_LAT_TOP, MAP_LAT_BOT = 82.0, -60.0
LANDMASK = [
    "............" "......###..." "...####....." ".##......##." "......##...." "............",
    "............" "..###.####.." "..######...." ".##.......##" "##...#####.." "........##..",
    "########..##" "#########..." ".######....." "..##########" "############" "###########.",
    "########.###" "#####...####" "..####..##.." ".###########" "############" "############",
    "..##########" "######..####" "#..##......#" ".###########" "############" "##########..",
    "..........##" "#####..#####" "##........##" "############" "############" "#######.....",
    ".........###" "############" "#.........##" "############" "############" "####........",
    "..........##" "###########." ".........###" "##########.." "############" "####........",
    "..........##" "##########.." ".........###" "#######.####" "############" "###.........",
    "..........##" "#########..." "........####" "############" "##########.#" ".##.........",
    "..........##" "###....##..." "........####" "############" "############" "............",
    "..........##" "##.........." "........####" "###########." ".####.####.#" "#...........",
    "..........##" "#..........." "........####" "###.#####..." "..###.####.#" "#...........",
    "............" "........###." "........####" "##########.." "..##..####.." "#...........",
    "............" ".......#####" "###.......##" "##########.." "......#....." "............",
    "............" ".......#####" "##.........#" "########...." ".....#######" ".#####......",
    "............" ".......#####" "##.........." "########...." ".....######." ".######.....",
    "............" "......######" "#..........." "########...." ".......###.#" "#.#####.....",
    "............" "......######" "#..........." "##########.." "..........##" "##.###......",
    "............" ".......#####" "###........." "##########.." ".........###" "######......",
    "............" "........####" "##.........." ".####...##.." ".........###" "######......",
    "............" "........####" "............" ".###........" "..........##" "#####.......",
    "............" "........####" "............" "............" "............" ".####.....##",
    "............" "........###." "............" "............" "............" ".........###",
    "............" "........##.." "............" "............" "............" "........###.",
    "............" "........##.." "............" "............" "............" "............",
    "............" "........##.." "............" "............" "............" "............",
    "............" "........##.." "............" "............" "............" "............",
]

# Story pins: num, story lon/lat, label lon/lat. The label sits on the
# story unless it is a callout — the three Levant stories (3, 11, 12)
# share one dot, so their labels fan out around it with leader lines,
# and pin 1 labels east so it clears Kyiv (13) and the Levant fan.
PINS = [
    (1, 36.5, 45.2, 44.0, 48.0),      # Kerch bridge, Crimea — callout east
    (2, 50.6, 26.2, 50.6, 26.2),      # Bahrain
    (3, 35.2, 31.8, 28.5, 36.5),      # Israel — callout west
    (4, 45.0, 12.8, 45.0, 12.8),      # Aden, Yemen
    (5, 140.0, 40.0, 140.0, 40.0),    # Japan
    (6, 116.4, 39.9, 116.4, 39.9),    # Beijing
    (7, 103.8, 1.4, 103.8, 1.4),      # Singapore
    (8, -74.0, 40.7, -74.0, 40.7),    # New York
    (9, 79.0, 30.3, 79.0, 30.3),      # Uttarakhand, India
    (10, -0.1, 51.5, -0.1, 51.5),     # London
    (11, 34.3, 31.4, 24.5, 25.5),     # Gaza — callout south-west
    (12, 35.5, 31.9, 52.0, 44.0),     # Jericho — callout east
    (13, 30.5, 50.4, 30.5, 50.4),     # Kyiv
]


def kicker_chip(d, x, y, text, fnt):
    tw = d.textlength(text, font=fnt)
    d.rectangle([x, y, x + tw + 12, y + fnt.size + 10], fill=RED)
    d.text((x + 6, y + 5), text, font=fnt, fill=LIGHT)
    return tw + 12


def story_cell(d, x, y, w, h, story, head_size, sum_size, art_h, art=True,
               num=None):
    """One story: optional illustration strip, kicker chip, headline, summary."""
    ty = y
    if art:
        SCENES[story["scene"]](d, x, y, w, art_h)
        d.rectangle([x, y + art_h, x + w, y + art_h + 2], fill=RULE)
        ty = y + art_h + 10
    kf = font(SANS_B, 11)
    if num is not None:
        num_badge(d, x + 9, ty + 10, num, 9)
        kicker_chip(d, x + 24, ty, story["kicker"], kf)
    else:
        kicker_chip(d, x, ty, story["kicker"], kf)
    ty += 26
    hf = font(SERIF, head_size)
    lines = wrap(d, story["headline"], hf, w - 4)
    ty = draw_text_block(d, x, ty, w - 4, lines, hf, INK)
    ty += 3
    sf = font(SANS, sum_size)
    lines = wrap(d, story["summary"], sf, w - 4)
    draw_text_block(d, x, ty, w - 4, lines, sf, (52, 50, 46))


def num_badge(d, cx, cy, num, r):
    """A red pin/badge: filled circle, white ring, white number."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
              outline=(255, 255, 255), width=2)
    f = font(SANS_B, 11 if num < 10 else 10)
    d.text((cx, cy), str(num), font=f, fill=(255, 255, 255), anchor="mm")


def map_xy(x0, y0, w, h, lon, lat):
    """Equirectangular projection onto the map panel."""
    fx = (lon + 180.0) / 360.0
    fy = (MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT)
    return x0 + fx * w, y0 + fy * h


def draw_map(d, x0, y0, w, h):
    """Dotted continents from LANDMASK, then the numbered story pins."""
    cols, rows = 72, 28
    dx, dy = w / cols, h / rows
    r = 3.1
    for ri, row in enumerate(LANDMASK):
        for ci, ch in enumerate(row):
            if ch == "#":
                cx, cy = x0 + (ci + 0.5) * dx, y0 + (ri + 0.5) * dy
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    for num, lon, lat, llon, llat in PINS:
        tx, ty = map_xy(x0, y0, w, h, lon, lat)
        if (llon, llat) != (lon, lat):
            lx, ly = map_xy(x0, y0, w, h, llon, llat)
            d.line([lx, ly, tx, ty], fill=RED, width=1)
            d.ellipse([tx - 3.5, ty - 3.5, tx + 3.5, ty + 3.5], fill=RED)
            num_badge(d, lx, ly, num, 9)
        else:
            num_badge(d, tx, ty, num, 9)


def draw_brief(d, x, y, w, brief):
    """One brief: red number, bold place name, one-liner wrapped under it."""
    nf = font(SANS_B, 12)
    pf = font(SANS_B, 12)
    tf = font(SANS, 12)
    head = f"{brief['num']}."
    d.text((x, y), head, font=nf, fill=RED)
    hx = x + d.textlength(head, font=nf) + 5
    d.text((hx, y), brief["place"], font=pf, fill=INK)
    px = hx + d.textlength(brief["place"], font=pf) + 5
    words = brief["text"].split()
    lines, cur, avail = [], "", w - (px - x)
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=tf) <= avail:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur, avail = word, w - int(d.textlength(head, font=nf)) - 5
    if cur:
        lines.append(cur)
    for i, line in enumerate(lines[:3]):
        lx = px if i == 0 else hx
        d.text((lx, y + i * 15), line, font=tf, fill=(52, 50, 46))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead
    d.rectangle([M, 14, W - M, 15], fill=INK)
    title_f = font(SERIF, 54)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 20), title, font=title_f, fill=INK)
    date_f = font(SANS_B, 28)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 84), date, font=date_f, fill=RED)
    sub_f = font(SANS, 14)
    sub = "The world's news, in one image — every story happened or was first reported today."
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 122), sub, font=sub_f, fill=GREY)
    d.rectangle([M, 144, W - M, 147], fill=INK)
    d.rectangle([M, 150, W - M, 152], fill=INK)

    # ---- world map band: dotted continents, numbered pins per story
    mh_f = font(SANS_B, 15)
    d.text((M, 162), "THE DAY ON THE MAP", font=mh_f, fill=NAVY)
    note_f = font(SANS, 11)
    note = "Red pins mark where each story happened — numbers match the stories below."
    nw = d.textlength(note, font=note_f)
    d.text((W - M - nw, 165), note, font=note_f, fill=GREY)
    map_y, map_h = 188, 216
    d.rectangle([M, map_y, W - M, map_y + map_h], fill=(233, 238, 243))
    d.rectangle([M, map_y, W - M, map_y + map_h], outline=RULE, width=1)
    draw_map(d, M, map_y, W - 2 * M, map_h)
    d.rectangle([M, map_y + map_h + 8, W - M, map_y + map_h + 10], fill=INK)

    # ---- hero lead story
    hy, hh = 420, 128
    SCENES[LEAD["scene"]](d, M, hy, 300, hh)
    d.rectangle([M, hy, M + 300, hy + hh], outline=RULE, width=2)
    tx = M + 318
    tw_ = W - M - tx
    kf = font(SANS_B, 13)
    num_badge(d, tx + 10, hy + 16, 1, 10)
    kicker_chip(d, tx + 26, hy + 6, LEAD["kicker"], kf)
    hf = font(SERIF, 27)
    lines = wrap(d, LEAD["headline"], hf, tw_)
    ty = draw_text_block(d, tx, hy + 40, tw_, lines, hf, INK)
    sf = font(SANS, 14)
    lines = wrap(d, LEAD["summary"], sf, tw_)
    draw_text_block(d, tx, ty + 10, tw_, lines, sf, (52, 50, 46))
    d.rectangle([M, hy + hh + 10, W - M, hy + hh + 12], fill=INK)

    # ---- three pictured panels
    py, ph = 566, 190
    pw = (W - 2 * M - 2 * 16) // 3
    for i, story in enumerate(PANELS):
        px = M + i * (pw + 16)
        story_cell(d, px, py, pw, ph, story, 17, 12, 64, num=i + 2)
        if i < 2:
            d.line([px + pw + 8, py, px + pw + 8, py + ph], fill=RULE, width=1)
    d.rectangle([M, py + ph + 6, W - M, py + ph + 8], fill=INK)

    # ---- around the world in brief: nine one-liners, two columns
    by = 772
    bf = font(SANS_B, 16)
    d.text((M, by), "AROUND THE WORLD IN BRIEF", font=bf, fill=INK)
    d.rectangle([M, by + 24, W - M, by + 26], fill=RED)
    col_w = (W - 2 * M - 16) // 2
    rows_y = by + 38
    for i, brief in enumerate(BRIEFS):
        col = 0 if i < 5 else 1
        row = i if i < 5 else i - 5
        bx = M + col * (col_w + 16)
        draw_brief(d, bx, rows_y + row * 36, col_w, brief)

    # ---- footer
    foot_f = font(SANS, 10)
    foot = "Sources: Reuters, AP, AFP, Al Jazeera, Just Security  •  make.fun news-image-20261117"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 996), foot, font=foot_f, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
