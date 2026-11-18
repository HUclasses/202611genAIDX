"""金沢市景観計画の色彩基準（マンセル値）を sRGB / HEX に変換し、
Web 用トークン候補とコントラスト比を計算するスクリプト。

使い方: python3 munsell.py > munsell_out.md
"""
import warnings
import numpy as np
import colour

warnings.filterwarnings("ignore")

C = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"]


def munsell_to_hex(spec: str) -> str:
    """マンセル表記 (例 '7.5YR 5/3') → '#RRGGBB'。Munsell は C 光源基準なので CAT02 で D65 へ順応。"""
    xyY = colour.munsell_colour_to_xyY(spec)
    XYZ = colour.xyY_to_XYZ(xyY)
    rgb = colour.XYZ_to_sRGB(XYZ, illuminant=C, chromatic_adaptation_transform="CAT02")
    out_of_gamut = bool(np.any(rgb < -0.002) or np.any(rgb > 1.002))
    rgb = np.clip(rgb, 0, 1)
    h = "#" + "".join(f"{int(round(v * 255)):02X}" for v in rgb)
    return h + (" (gamut外→clip)" if out_of_gamut else "")


def rel_lum(hexstr: str) -> float:
    hexstr = hexstr[:7]
    rgb = np.array([int(hexstr[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2])


def contrast(a: str, b: str) -> float:
    la, lb = sorted([rel_lum(a), rel_lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


if __name__ == "__main__":
    print("## 1. 推奨色（木色）の範囲 = 景観計画の数値そのもの\n")
    print("| 色相 | 明度 | 彩度2 | 彩度3 | 彩度4 |\n|---|---|---|---|---|")
    for hue in ["5YR", "7.5YR", "10YR", "2.5Y"]:
        for v in [4, 5, 6, 7]:
            row = [munsell_to_hex(f"{hue} {v}/{c}") for c in (2, 3, 4)]
            print(f"| {hue} | {v} | " + " | ".join(row) + " |")

    print("\n## 2. Web 用トークン候補（推奨色を軸に明度方向へ拡張）\n")
    candidates = {
        # name: (munsell, 根拠)
        "mokujiki-950": ("7.5YR 9.6/0.5", "紙・背景。推奨色と同じ色相で彩度を落とした生成り"),
        "mokujiki-900": ("7.5YR 9.2/1", "面の背景（カード下地）"),
        "mokujiki-800": ("7.5YR 8.5/1.5", "区切り面・無効状態"),
        "mokujiki-700": ("7.5YR 7/2", "推奨色範囲の上端（明度7・彩度2）"),
        "mokujiki-500": ("7.5YR 5/3", "推奨色範囲の中心＝『木色』代表色"),
        "mokujiki-400": ("7.5YR 4/3", "推奨色範囲の下端（明度4）"),
        "sumi-700": ("7.5YR 3/1.5", "副次テキスト。禁止色ルール内（YR彩度≤6）"),
        "sumi-900": ("7.5YR 2/1", "本文テキスト（墨）"),
        "bengara-600": ("10R 3/6", "アクセント：紅殻格子。R系の上限彩度6ちょうど"),
        "bengara-700": ("10R 2.5/5", "アクセントの押下状態"),
        "kinpaku-400": ("2.5Y 7/4", "金箔：Y系の上限彩度4ちょうど。装飾・強調の下地"),
        "ai-700": ("5PB 3/2", "藍：その他色相の上限彩度2。情報・リンク補助"),
        "koke-700": ("5GY 3.5/2", "苔：成功状態。その他色相の上限彩度2"),
    }
    print("| トークン | マンセル | HEX | 対 mokujiki-950 | 根拠 |\n|---|---|---|---|---|")
    hexes = {}
    for name, (spec, why) in candidates.items():
        h = munsell_to_hex(spec)
        hexes[name] = h[:7]
        print(f"| {name} | {spec} | {h} | {{c}} | {why} |".replace("{c}", "-"))
    bg = hexes["mokujiki-950"]
    print("\n## 3. コントラスト比（WCAG 2.x）\n")
    print("| 前景 | 背景 | 比 | AA本文(4.5) | AA大文字/UI(3.0) |\n|---|---|---|---|---|")
    pairs = [
        ("sumi-900", "mokujiki-950"), ("sumi-700", "mokujiki-950"),
        ("sumi-900", "mokujiki-900"), ("sumi-700", "mokujiki-900"),
        ("bengara-600", "mokujiki-950"), ("ai-700", "mokujiki-950"),
        ("koke-700", "mokujiki-950"), ("mokujiki-400", "mokujiki-950"),
        ("mokujiki-500", "mokujiki-950"), ("mokujiki-950", "bengara-600"),
        ("mokujiki-950", "sumi-900"), ("sumi-900", "kinpaku-400"),
        ("sumi-900", "mokujiki-700"),
    ]
    for f, b in pairs:
        r = contrast(hexes[f], hexes[b])
        print(f"| {f} {hexes[f]} | {b} {hexes[b]} | {r:.2f} | {'○' if r >= 4.5 else '×'} | {'○' if r >= 3 else '×'} |")
    import json
    json.dump(hexes, open("tokens_hex.json", "w"), indent=1)
