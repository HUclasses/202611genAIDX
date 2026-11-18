"""DESIGN.md の全色を HEX → マンセル値に逆変換し、
金沢市景観計画の「禁止色」ルールに収まっているかを検査する。

ルール: R・YR 系は彩度6以下、Y 系は彩度4以下、それ以外の色相は彩度2以下。
使い方: python3 check_kinshi.py DESIGN.md
"""
import re
import sys
import warnings
import numpy as np
import colour

warnings.filterwarnings("ignore")
C = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"]


def hex_to_munsell(h: str) -> str:
    rgb = np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    XYZ = colour.sRGB_to_XYZ(rgb, illuminant=C, chromatic_adaptation_transform="CAT02")
    xyY = colour.XYZ_to_xyY(XYZ)
    return colour.xyY_to_munsell_colour(xyY, hue_decimals=1, value_decimals=1, chroma_decimals=1)


def limit_for(hue_family: str) -> float:
    if hue_family in ("R", "YR"):
        return 6
    if hue_family == "Y":
        return 4
    return 2


text = open(sys.argv[1], encoding="utf-8").read()
block = text[text.index("```yaml\ncolors:"):]
block = block[:block.index("```", 8)]
ok_all = True
print("| トークン | HEX | 逆変換マンセル | 上限彩度 | 判定 |\n|---|---|---|---|---|")
for name, h in re.findall(r'^\s+([\w-]+):\s+"(#[0-9A-Fa-f]{6})"', block, re.M):
    if h.upper() == "#FFFFFF":
        print(f"| {name} | {h} | N10 | - | ○（無彩色） |")
        continue
    m = hex_to_munsell(h)
    if m.startswith("N"):
        print(f"| {name} | {h} | {m} | - | ○（無彩色） |")
        continue
    hue, vc = m.split(" ")
    family = re.sub(r"[\d.]", "", hue)
    chroma = float(vc.split("/")[1])
    lim = limit_for(family)
    ok = chroma <= lim + 0.15  # 変換の丸め誤差を許容
    ok_all &= ok
    print(f"| {name} | {h} | {m} | {lim} | {'○' if ok else '× 禁止色'} |")
print("\n結果:", "すべて禁止色ルール内" if ok_all else "ルール外の色があります")
