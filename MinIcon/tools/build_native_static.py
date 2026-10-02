#!/usr/bin/env python3
"""Build packaged Native MinIcon static faces from the canonical variable font."""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


FONT_PATH = Path(__file__).resolve().parents[1] / "MinIconVF.woff2"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    for weight in range(100, 1000, 100):
        font = TTFont(FONT_PATH, recalcTimestamp=False)
        instantiateVariableFont(
            font,
            {"wght": weight, "rond": 2, "edpt": 1},
            inplace=True,
            optimize=True,
        )
        font.flavor = None
        font.save(args.output / f"MinIcon{weight}.ttf")


if __name__ == "__main__":
    main()
