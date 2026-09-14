#!/usr/bin/env python3
"""Generate minified, self-contained Gravity Linux logo source SVGs.

Requires fontTools on PYTHONPATH when rebuilding the outlined Manrope wordmark.
"""

from pathlib import Path
import re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

HERE = Path(__file__).resolve().parent
DRAFTS = HERE.parent.parent / "gravity_artwork_drafts"
SOURCE = HERE / "src"

RED_FACET = "#F21E1B"
PURPLE_FACET = "#8F4BBE"


def paths_from(name):
    raw = (DRAFTS / "apple-variants" / name).read_text(encoding="utf-8")
    return re.findall(r'<path fill="(#[0-9A-Fa-f]{6})" d="([^"]+)"', raw)


color_paths = paths_from("pal_08.svg")
color_paths[38] = (RED_FACET, color_paths[38][1])
color_paths[33] = (PURPLE_FACET, color_paths[33][1])
mono_paths = [d for _, d in paths_from("pal_00.svg")]


def color_definition():
    paths = "".join(f'<path fill="{fill}" d="{d}"/>' for fill, d in color_paths)
    return f'<g id="color-mark">{paths}</g>'


def mono_definition():
    path_defs = "".join(f'<path id="m{i}" d="{d}"/>' for i, d in enumerate(mono_paths))
    uses = "".join(f'<use href="#m{i}"/>' for i in range(len(mono_paths)))
    # These tiny highlight patches were intentionally removed during review.
    visible = "".join(f'<use href="#m{i}"/>' for i in range(len(mono_paths)) if i < 39 or i in {39, 43})
    return (
        f'<g id="mono-paths">{path_defs}</g>'
        f'<clipPath id="mono-clip">{uses}</clipPath>'
        f'<g id="mono-mark"><g fill="#000">{uses}</g>'
        f'<g fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" '
        f'stroke-linejoin="round" clip-path="url(#mono-clip)">{visible}</g></g>'
    )


font = TTFont(DRAFTS / "fonts" / "Manrope-Variable.ttf")
glyph_set = font.getGlyphSet()
cmap = font.getBestCmap()
units = font["head"].unitsPerEm
advances = font["hmtx"].metrics


def wordmark(text, font_size, x, baseline, fill, centered=False, tracking=1):
    glyphs = [cmap[ord(char)] for char in text]
    scale = font_size / units
    width = sum(advances[glyph][0] * scale for glyph in glyphs) + tracking * (len(glyphs) - 1)
    cursor = x - width / 2 if centered else x
    result = []
    for glyph in glyphs:
        pen = SVGPathPen(glyph_set)
        glyph_set[glyph].draw(pen)
        d = pen.getCommands()
        if d:
            result.append(f'<path fill="{fill}" d="{d}" transform="translate({cursor:.4f} {baseline}) scale({scale:.8f} {-scale:.8f})"/>')
        cursor += advances[glyph][0] * scale + tracking
    return "".join(result)


def svg(width, height, title, defs, content, viewbox=None):
    viewbox = viewbox or f"0 0 {width} {height}"
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{viewbox}"><title>{title}</title><defs>{defs}</defs>{content}</svg>'


COLOR = color_definition()
MONO = mono_definition()


def color_mark(x, y, size):
    scale = size / 1254
    return f'<use href="#color-mark" transform="translate({x} {y}) scale({scale:.9f})"/>'


def mono_mark(x, y, size):
    scale = size / 1254
    return f'<use href="#mono-mark" transform="translate({x} {y}) scale({scale:.9f})"/>'


square_color = color_mark(177, -10, 900)
square_mono = mono_mark(177, -10, 900)
horizontal_color = color_mark(40, 100, 400)
horizontal_mono = mono_mark(40, 100, 400)

assets = {
    "GravityLinux_logo.svg": svg(1254, 1254, "Gravity Linux logo", COLOR,
        f'<rect width="1254" height="1254" fill="#fff"/>{square_color}'
        f'{wordmark("Gravity Linux", 112, 627, 1000, "#000", centered=True)}'),
    "GravityLinux_logo_darkbg.svg": svg(1254, 1254, "Gravity Linux logo for dark backgrounds", COLOR,
        f'<rect width="1254" height="1254" fill="#000"/>{square_color}'
        f'{wordmark("Gravity Linux", 112, 627, 1000, "#fff", centered=True)}'),
    "GravityLinux_logo_horizontal.svg": svg(1600, 600, "Gravity Linux horizontal logo", COLOR,
        f'<rect width="1600" height="600" fill="#fff"/>{horizontal_color}'
        f'{wordmark("Gravity Linux", 160, 500, 355, "#000")}'),
    "GravityLinux_logo_horizontal_darkbg.svg": svg(1600, 600, "Gravity Linux horizontal logo for dark backgrounds", COLOR,
        f'<rect width="1600" height="600" fill="#000"/>{horizontal_color}'
        f'{wordmark("Gravity Linux", 160, 500, 355, "#fff")}'),
    "GravityLinux_logo_mono.svg": svg(1254, 1254, "Gravity Linux monochrome logo", MONO,
        f'<rect width="1254" height="1254" fill="#fff"/>{square_mono}'
        f'{wordmark("Gravity Linux", 112, 627, 1000, "#000", centered=True)}'),
    "GravityLinux_logo_horizontal_mono.svg": svg(1600, 600, "Gravity Linux monochrome horizontal logo", MONO,
        f'<rect width="1600" height="600" fill="#fff"/>{horizontal_mono}'
        f'{wordmark("Gravity Linux", 160, 500, 355, "#000")}'),
    "GravityLinux_logomark.svg": svg(1254, 1254, "Gravity Linux color logomark", COLOR,
        color_mark(0, 0, 1254), "-8 -11.5 1254 1254"),
    "GravityLinux_logomark_mono.svg": svg(1254, 1254, "Gravity Linux monochrome logomark", MONO,
        mono_mark(0, 0, 1254), "-8 -11.5 1254 1254"),
}

for name, contents in assets.items():
    (SOURCE / name).write_text(contents, encoding="utf-8")
