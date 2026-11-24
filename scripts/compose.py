#!/usr/bin/env python3
"""Compose the news front page for 24 November 2026.

A cream broadsheet front page, not a plain list: a masthead, one LEAD
feature (Nvidia reinstates Huang) with a deck and a stat strip, then a 2x2
grid of the other four stories, and a footer with the date and the sources.
Everything is drawn procedurally with PIL from the STORIES data below, so
the output is fully deterministic: no network, no timestamps, no
randomness.

Every headline, number and claim below was verified against a primary
outlet on 24 Nov 2026 (see README.md for the source links). Nothing on
this page is invented: if a lead could not be verified, it was dropped.

Run:  python3 scripts/compose.py   (writes entry.png next to this script's dir)
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN  # 952

# --- palette: cream broadsheet ---------------------------------------------
BG = (242, 236, 220)       # cream paper
DOT = (232, 224, 203)      # faint dot texture
PANEL = (252, 250, 244)    # story panels (near-white)
PANEL_EDGE = (168, 158, 136)  # panel outline (warm grey)
INK = (24, 24, 22)         # headline black
BODY = (58, 56, 50)        # body dark grey
MUTED = (122, 114, 96)     # kickers / footer
RED = (178, 34, 34)        # masthead red / lead accent
TEAL = (0, 110, 105)
ORANGE = (180, 90, 20)
BLUE = (30, 80, 140)
RULE = (24, 24, 22)        # black rules
ARC = (226, 216, 192)      # faint circles behind masthead

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width, max_lines, label):
    """Greedy word wrap by pixel width. Hard-fails if it needs more lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if not cur:
                raise AssertionError(
                    "%s: single word %r too wide for %d px" % (label, word, max_width)
                )
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        raise AssertionError(
            "%s: body needs %d lines (max %d): %r -> %r"
            % (label, len(lines), max_lines, text, lines)
        )
    return lines


def fit_headline(draw, text, max_width, start_size, min_size, label):
    """Shrink a one-line serif headline until it fits; hard-fail below min_size."""
    for size in range(start_size, min_size - 1, -1):
        fnt = font(SERIF_BOLD, size)
        if draw.textlength(text, font=fnt) <= max_width:
            return fnt
    raise AssertionError(
        "%s: headline %r still too wide at %d pt for %d px"
        % (label, text, min_size, max_width)
    )


def center(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


# --- the five stories (all verified 24 Nov 2026, see README for sources) ---
# Numbers below are exact quotes of the cited outlets:
#  +31% NVDA / +6% Nasdaq / +5% S&P 500 (Reuters Trading Day, 24 Nov)
#  2 killed, 22 wounded incl. 2 children (Reuters, 24 Nov)
#  $43.9B, 1.135 shares, 34% premium (Reuters / WSJ, 23 Nov)
#  8th U.S.-Qatar Strategic Dialogue (U.S. Dept. of State, 23 Nov)
#  return Dec 16 after 2+ years of exile in India (Reuters, 24 Nov)
LEAD = {
    "num": "01",
    "kicker": "MARKETS  —  LEAD STORY",
    "headline": ["HUANG IS BACK", "AT NVIDIA"],
    "body": "Board reinstates Jensen Huang as CEO 11 days after he resigned; "
            "shares +31%, Nasdaq +6%.",
    "stat": "11 DAYS AFTER RESIGNING  •  SHARES +31%  •  NASDAQ +6%",
    "accent": RED,
}

GRID = [
    {
        "num": "02",
        "kicker": "WAR IN UKRAINE",
        "headline": "RUSSIA HITS ZAPORIZHZHIA",
        "body": "Overnight attack kills 2, wounds 22, including 2 children "
                "— ZAPORIZHZHIA",
        "accent": RED,
    },
    {
        "num": "03",
        "kicker": "CYBERSECURITY",
        "headline": "CROWDSTRIKE BUYS ZSCALER",
        "body": "$43.9B all-stock deal; 1.135 shares per share, a 34% premium "
                "— NEW YORK",
        "accent": TEAL,
    },
    {
        "num": "04",
        "kicker": "DIPLOMACY",
        "headline": "QATAR PUSHES IRAN TALKS",
        "body": "Rubio and Vance meet Qatar's PM; 8th Strategic "
                "Dialogue — WASHINGTON",
        "accent": ORANGE,
    },
    {
        "num": "05",
        "kicker": "SOUTH ASIA",
        "headline": "HASINA TO RETURN DEC 16",
        "body": "Ousted PM plans return from 2+ years of exile in India on "
                "Dec 16 — DHAKA",
        "accent": BLUE,
    },
]


def draw_background(img, draw):
    draw.rectangle([0, 0, W, H], fill=BG)
    # faint circles behind the masthead
    for r in (150, 210, 270):
        draw.ellipse([512 - r, 118 - r, 512 + r, 118 + r], outline=ARC, width=2)
    # dotted texture over the whole canvas
    for y in range(7, H, 14):
        for x in range(7, W, 14):
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=DOT)


def draw_masthead(draw):
    # top black rule + thin red rule
    draw.rectangle([MARGIN, 36, W - MARGIN, 39], fill=RULE)
    draw.rectangle([MARGIN, 42, W - MARGIN, 44], fill=RED)
    center(draw, 512, 54, "WORLD NEWS", font(SERIF_BOLD, 96), INK)
    center(draw, 512, 162, "TUESDAY  •  24 NOVEMBER 2026",
           font(SANS_BOLD, 27), RED)
    draw.rectangle([MARGIN, 200, W - MARGIN, 202], fill=RULE)
    draw.rectangle([MARGIN, 205, W - MARGIN, 206], fill=RED)


def draw_lead(draw):
    x0, y0, x1, y1 = MARGIN, 218, W - MARGIN, 458
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=PANEL_EDGE, width=1)
    draw.rectangle([x0, y0, x0 + 8, y1], fill=RED)
    pad = 26
    tx = x0 + pad
    # kicker + number chip
    draw.text((tx, y0 + 18), LEAD["kicker"], font=font(SANS_BOLD, 19), fill=RED)
    chip = (x1 - 78, y0 + 14, x1 - 22, y0 + 50)
    draw.rounded_rectangle(chip, radius=6, fill=RED)
    center(draw, (chip[0] + chip[2]) / 2, y0 + 19, LEAD["num"],
           font(SANS_BOLD, 22), PANEL)
    # two-line serif headline
    hy = y0 + 52
    for line in LEAD["headline"]:
        draw.text((tx, hy), line, font=font(SERIF_BOLD, 44), fill=INK)
        hy += 52
    # body, at most two lines, then the stat strip below it (never overlapping)
    body_lines = wrap(draw, LEAD["body"], font(SANS, 22), x1 - tx - pad, 2, "lead body")
    by = y0 + 158
    for line in body_lines:
        draw.text((tx, by), line, font=font(SANS, 22), fill=BODY)
        by += 28
    draw.text((tx, y0 + 218), LEAD["stat"], font=font(SANS_BOLD, 16), fill=MUTED)


def draw_grid(draw):
    gx, gy = MARGIN, 472
    cw, ch, gap = 470, 228, 12
    positions = [(gx, gy), (gx + cw + gap, gy),
                 (gx, gy + ch + gap), (gx + cw + gap, gy + ch + gap)]
    for story, (x0, y0) in zip(GRID, positions):
        x1, y1 = x0 + cw, y0 + ch
        draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=PANEL_EDGE, width=1)
        draw.rectangle([x0, y0, x0 + 6, y1], fill=story["accent"])
        # number chip + kicker
        chip = (x0 + 20, y0 + 18, x0 + 64, y0 + 52)
        draw.rounded_rectangle(chip, radius=6, fill=story["accent"])
        center(draw, (chip[0] + chip[2]) / 2, y0 + 22, story["num"],
               font(SANS_BOLD, 20), (255, 255, 255))
        draw.text((x0 + 76, y0 + 24), story["kicker"],
                  font=font(SANS_BOLD, 16), fill=story["accent"])
        # one-line serif headline, shrunk to fit
        hfnt = fit_headline(draw, story["headline"], cw - 40, 30, 18,
                            "story %s headline" % story["num"])
        draw.text((x0 + 20, y0 + 62), story["headline"], font=hfnt, fill=INK)
        draw.rectangle([x0 + 20, y0 + 102, x1 - 20, y0 + 103], fill=PANEL_EDGE)
        # body, at most two lines (19 pt so ~76 chars fit the 430 px column)
        body_lines = wrap(draw, story["body"], font(SANS, 19), cw - 40, 2,
                          "story %s body" % story["num"])
        by = y0 + 116
        for line in body_lines:
            draw.text((x0 + 20, by), line, font=font(SANS, 19), fill=BODY)
            by += 27


def draw_footer(draw):
    draw.rectangle([MARGIN, 950, W - MARGIN, 951], fill=RULE)
    center(draw, 512, 962, "THE DAY IN FIVE STORIES  •  24 NOVEMBER 2026",
           font(SANS_BOLD, 20), INK)
    center(draw, 512, 988, "Sources: Reuters  •  AP  •  WSJ  •  CNN  •  U.S. Dept. of State",
           font(SANS, 15), MUTED)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_background(img, draw)
    draw_masthead(draw)
    draw_lead(draw)
    draw_grid(draw)
    draw_footer(draw)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
    out = os.path.normpath(out)
    img.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    assert len(data) <= 1048576, "entry.png %d bytes exceeds 1 MiB" % len(data)
    assert Image.open(out).size == (1024, 1024), "entry.png is not 1024x1024"
    print("wrote %s (%d bytes, sha256 %s)"
          % (out, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
