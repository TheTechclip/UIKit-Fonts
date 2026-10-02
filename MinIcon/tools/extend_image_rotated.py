#!/usr/bin/env python3
"""Build Musecat's iImageRotated from existing MinIcon variable glyphs."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import (
    Glyph,
    GlyphComponent,
    UNSCALED_COMPONENT_OFFSET,
)


FONT_PATH = Path(__file__).resolve().parents[1] / "MinIconVF.woff2"
CODEPOINT = 0xEC3C
BASE_NAME = "musecat_image_rotated"
FILL_NAME = "musecat_image_rotated.ss09"

IMAGE_CODEPOINT = 0xE094
FORWARD_CODEPOINT = 0xE0E4

# Discord's rotate-image affordance reads as a small bent forward arrow in the
# upper-left and an image tile in the lower-right. Keep both as components so
# MinIcon's wght/rond/edpt interpolation remains native to the source glyphs.
IMAGE_SCALE = 0.60
IMAGE_OFFSET = (270, 45)
ARROW_SCALE = 0.30
ARROW_OFFSET = (233, 485)
ARROW_NAME = "musecat_image_rotated.arrow"
HEAD_SCALE = 0.65


def unicode_cmap(font: TTFont) -> dict[int, str]:
    result: dict[int, str] = {}
    for table in font["cmap"].tables:
        if table.isUnicode():
            result.update(table.cmap)
    return result


def single_substitutions(font: TTFont, feature_tag: str) -> dict[str, str]:
    gsub = font["GSUB"].table
    for record in gsub.FeatureList.FeatureRecord:
        if record.FeatureTag != feature_tag:
            continue
        for lookup_index in record.Feature.LookupListIndex:
            lookup = gsub.LookupList.Lookup[lookup_index]
            if lookup.LookupType != 1:
                continue
            for subtable in lookup.SubTable:
                mapping = getattr(subtable, "mapping", None)
                if mapping is not None:
                    return mapping
    raise RuntimeError(f"Missing {feature_tag} SingleSubst mapping")


def component(name: str, scale: float, offset: tuple[int, int]) -> GlyphComponent:
    value = GlyphComponent()
    value.flags = UNSCALED_COMPONENT_OFFSET
    value.glyphName = name
    value.x, value.y = offset
    value.transform = [[scale, 0], [0, scale]]
    return value


def composite(image: str, arrow: str) -> Glyph:
    glyph = Glyph()
    glyph.numberOfContours = -1
    glyph.components = [
        component(image, IMAGE_SCALE, IMAGE_OFFSET),
        component(arrow, ARROW_SCALE, ARROW_OFFSET),
    ]
    return glyph


def main() -> None:
    font = TTFont(FONT_PATH, recalcTimestamp=False)

    # Load glyph-indexed tables before changing glyph order.
    gvar = font["gvar"]
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    gdef = font["GDEF"].table
    _ = font["post"]

    cmap = unicode_cmap(font)
    image = cmap[IMAGE_CODEPOINT]
    source_arrow = cmap[FORWARD_CODEPOINT]
    # The arrow is half the image scale, so double its stroke around the
    # centerline before composition. Shrink only the chevron's centerline.
    arrow = ARROW_NAME
    source = glyf[source_arrow]
    derived = deepcopy(source)
    head_start = source.endPtsOfContours[0] + 1

    def project(point, points):
        candidates = []
        x, y = point
        for (ax, ay), (bx, by) in zip(points, points[1:]):
            dx, dy = bx - ax, by - ay
            projection = ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)
            t = max(0, min(1, projection))
            px, py = ax + t * dx, ay + t * dy
            candidates.append(((x - px) ** 2 + (y - py) ** 2, px, py))
        _, px, py = min(candidates)
        return px, py

    for index, (x, y) in enumerate(source.coordinates):
        head = index >= head_start
        centerline = (
            [(593, 727), (800, 520), (593, 313)]
            if head
            else [(160, 230), (160, 520), (800, 520)]
        )
        px, py = project((x, y), centerline)
        cx = 800 + (px - 800) * HEAD_SCALE if head else px
        cy = 520 + (py - 520) * HEAD_SCALE if head else py
        derived.coordinates[index] = (round(cx + (x - px) * 2), round(cy + (y - py) * 2))
    glyf.glyphs[arrow] = derived
    hmtx.metrics[arrow] = hmtx.metrics[source_arrow]
    variations = deepcopy(gvar.variations[source_arrow])
    for variation in variations:
        for index in range(len(source.coordinates)):
            delta = variation.coordinates[index]
            if delta is not None:
                variation.coordinates[index] = tuple(value * 2 for value in delta)
    gvar.variations[arrow] = variations
    ss09 = single_substitutions(font, "ss09")
    filled_image = ss09.get(image)
    if not filled_image:
        raise RuntimeError("iImage must retain an ss09 filled alternate")

    glyph_order = [
        name
        for name in font.getGlyphOrder()
        if name not in {BASE_NAME, FILL_NAME, ARROW_NAME}
    ]
    glyph_order.extend([ARROW_NAME, BASE_NAME, FILL_NAME])
    font.setGlyphOrder(glyph_order)

    glyf.glyphs[BASE_NAME] = composite(image, arrow)
    glyf.glyphs[FILL_NAME] = composite(filled_image, arrow)
    glyf.glyphOrder = glyph_order
    for name in (BASE_NAME, FILL_NAME):
        glyf.glyphs[name].recalcBounds(glyf)
        hmtx.metrics[name] = (960, glyf.glyphs[name].xMin)

    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap[CODEPOINT] = BASE_NAME

    glyph_classes = gdef.GlyphClassDef.classDefs
    glyph_classes[BASE_NAME] = glyph_classes.get(image, 2)
    glyph_classes[FILL_NAME] = glyph_classes.get(filled_image, 2)
    ss09[BASE_NAME] = FILL_NAME

    # Composite components inherit variation from their source glyphs.
    gvar.variations[BASE_NAME] = []
    gvar.variations[FILL_NAME] = []

    font.save(FONT_PATH)


if __name__ == "__main__":
    main()
