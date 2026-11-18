---
version: alpha
name: Kanazawa Mokujiki
description: >-
  金沢市景観計画の色彩基準（推奨色「木色」と禁止色の彩度上限）をWebに翻訳した、
  非公式の試作デザインシステム。構造はデジタル庁デザインシステム（DADS）に倣う。
---

# 金沢版 DESIGN.md「木色（もくじき）」— 非公式試作

> これは金沢市の公式デザインシステムではありません。金沢市が公開している景観計画の色彩基準などを材料に、
> 講演「画像生成AIでDX」のデモとして作った試作です。

## Overview

金沢の街並みのように、**背景に溶け込み、長く使っても疲れない**画面を目指す。主役は情報で、色は街の「地」として控えめに支える。

- 発想の元：金沢市景観計画は、伝統的な街並みの「地」になる色を **木色（もくじき）** とし、外壁の基調色の推奨範囲をマンセル値で定めている（色相 5YR〜2.5Y、明度 4〜7、彩度 2〜4）。
- 同じ計画の **禁止色**（R・YR 系は彩度6超、Y 系は彩度4超、その他の色相は彩度2超、蛍光色）を、この画面では **アクセントを含むすべての色の上限** として自主的に守る。
- 屋外広告物ガイドラインの考え方（「いかに他より目立つか」ではなく「いかに地域に溶け込むか」）を、UI でも採る。目立たせたいときは、彩度を上げるのではなく、余白・太さ・配置で目立たせる。
- 想定する利用者：市民、観光客、事業者。年齢も端末もさまざまなので、読みやすさとアクセシビリティ（WCAG 2.2 AA）を最優先する。
- 雰囲気：落ち着いている、温かい、きちんとしている。派手さ・ポップさは避ける。

## Colors

すべての色はマンセル値で定め、sRGB に変換している（Munsell Renotation → C光源 → CAT02 で D65 へ順応、colour-science 0.4.7 で計算）。HEX が正、マンセル値は由来を示す。

- **木色 / Mokujiki（#90745E = 7.5YR 5/3）**：推奨色範囲のちょうど中央。ブランドの「顔」だが、本文の背景より暗いため文字色には使わない。大きな面・装飾・境界線に使う。
- **木色・濃 / Mokujiki Deep（#775B44 = 7.5YR 4/3）**：推奨範囲の下端（明度4）。小さめの見出しや、アイコンなど文字に準じる要素に使える（背景に対して 5.65:1）。
- **生成り / Kinari（#F6F3F1 = 7.5YR 9.6/0.5）**：ページの背景。真っ白より柔らかく、木色と同じ色相。
- **墨 / Sumi（#382F2A = 7.5YR 2/1）**：本文。純黒ではなく、木色の色相を残した墨色（背景に対して 11.82:1）。
- **紅殻 / Bengara（#733529 = 10R 3/6）**：唯一のアクセント。紅殻格子から取った色で、R 系の上限（彩度6）ちょうど。主要ボタン・現在地表示など **1画面に1〜2か所** だけに使う。
- **金箔 / Kinpaku（#C3AB7B = 2.5Y 7/4）**：Y 系の上限（彩度4）ちょうど。お知らせ帯などの **面** として、墨の文字と組み合わせる。背景とのコントラストが 2.02:1 しかないので、線や文字の色には使わない。
- **藍 / Ai（#404857 = 5PB 3/2）**：その他の色相は彩度2までなので、ほぼ灰青。リンクと情報表示に使い、色だけでなく下線で区別する。
- **苔 / Koke（#505642 = 5GY 3.5/2）**：成功・完了の状態。
- **弁柄朱 / Error（#8F4D4C = 5R 4/6）**：エラー。紅殻と色味が近いので、必ずアイコンと文言を添える。

```yaml
colors:
  mokujiki-950: "#F6F3F1"
  mokujiki-900: "#F0E7DF"
  mokujiki-800: "#E2D3C5"
  mokujiki-700: "#BEAA99"
  mokujiki-500: "#90745E"
  mokujiki-400: "#775B44"
  sumi-700: "#53453B"
  sumi-900: "#382F2A"
  bengara-600: "#733529"
  bengara-700: "#612C26"
  kinpaku-400: "#C3AB7B"
  ai-700: "#404857"
  koke-700: "#505642"
  shu-500: "#8F4D4C"
  primary: "{colors.bengara-600}"
  primary-hover: "{colors.bengara-700}"
  on-primary: "#FFFFFF"
  secondary: "{colors.mokujiki-500}"
  secondary-deep: "{colors.mokujiki-400}"
  tertiary: "{colors.kinpaku-400}"
  neutral: "{colors.mokujiki-950}"
  surface: "{colors.mokujiki-950}"
  surface-container: "{colors.mokujiki-900}"
  surface-container-high: "{colors.mokujiki-800}"
  outline: "{colors.mokujiki-500}"
  outline-variant: "{colors.mokujiki-700}"
  on-surface: "{colors.sumi-900}"
  on-surface-variant: "{colors.sumi-700}"
  link: "{colors.ai-700}"
  success: "{colors.koke-700}"
  error: "{colors.shu-500}"
```

主な組み合わせのコントラスト比（WCAG 2.x の計算式による）：

| 前景 / 背景 | 比 | 用途 |
|---|---|---|
| 墨 / 生成り | 11.82 | 本文 |
| 墨・淡（sumi-700）/ 生成り | 8.33 | 補足文 |
| 白 / 紅殻 | 9.25 | 主要ボタン |
| 藍 / 生成り | 8.33 | リンク |
| 墨 / 金箔 | 5.86 | お知らせ帯 |
| 木色 / 生成り | 3.92 | 入力欄の枠線（非テキスト 3:1 以上） |
| 木色・淡（mokujiki-700）/ 生成り | 2.02 | 装飾の罫線のみ（意味を持たせない） |

## Typography

DADS と同じく **Noto Sans JP** を基本にする。見出しの大きいものだけ **Noto Serif JP**（明朝）を使い、城下町らしい格調を出す。行間は和文向けに広め（本文 1.7）にする。サイズの段階は DADS の FontSize に合わせる。

```yaml
typography:
  headline-display:
    fontFamily: Noto Serif JP
    fontSize: 45px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0.04em
  headline-lg:
    fontFamily: Noto Serif JP
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0.04em
  headline-md:
    fontFamily: Noto Sans JP
    fontSize: 24px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0.02em
  headline-sm:
    fontFamily: Noto Sans JP
    fontSize: 20px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0.02em
  body-lg:
    fontFamily: Noto Sans JP
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: 0.02em
  body-md:
    fontFamily: Noto Sans JP
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: 0.02em
  body-sm:
    fontFamily: Noto Sans JP
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: 0.02em
  label-lg:
    fontFamily: Noto Sans JP
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0.04em
  label-md:
    fontFamily: Noto Sans JP
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0.04em
```

- 本文は 16px 未満にしない（補足や注記だけ 14px まで）。
- 太さは 400 と 700 の2種類だけ（DADS と同じ）。

## Layout

格子（こうし）のように **規則正しく、細かすぎない** リズム。8px を基本単位とし、DADS の余白感に合わせる。コンテンツ幅は最大 960px（読み物中心のため、横に広げすぎない）。スマートフォンでは左右 16px、PC では左右 32px の余白。

```yaml
spacing:
  base: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 32px
  content-max: 960px
  tap-target: 44px
```

- 押せる要素は最小 44×44px。
- 見出しの上は `xl`（40px）、見出しと本文の間は `md`（16px）。セクションの区切りは罫線より余白を優先する。

## Elevation & Depth

**影はほとんど使わない**。奥行きは、面の色の差（生成り → 生成り濃 → 区切り面）と、木色の細い罫線で表す。漆喰の壁と木の柱のように、平面の重なりで構成する。影を使うのはメニューやダイアログなど浮いている要素だけで、DADS の Elevation 1〜2 相当（`0 2px 8px rgba(56,47,42,.12)`）にとどめる。

## Shapes

角丸は小さめ（4〜8px）。木組みのような **直線的で端正な** 印象を保ち、ふくらんだ丸いボタンや完全な円のボタンは使わない（アイコン用の丸だけは可）。

```yaml
rounded:
  none: 0px
  sm: 4px
  md: 6px
  lg: 8px
  full: 9999px
```

## Components

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.sm}"
    padding: 12px 24px
    height: 48px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.sm}"
    padding: 12px 24px
    height: 48px
  input-field:
    backgroundColor: "#FFFFFF"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
    height: 48px
  card:
    backgroundColor: "{colors.surface-container}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.lg}"
    padding: 24px
  notice-banner:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 16px 24px
  notice-error:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.error}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
  header:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    height: 64px
  link:
    textColor: "{colors.link}"
    typography: "{typography.body-md}"
  notice-success:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.success}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
  heading-accent:
    textColor: "{colors.secondary-deep}"
    typography: "{typography.headline-sm}"
  brand-band:
    backgroundColor: "{colors.secondary}"
    height: 6px
  divider:
    backgroundColor: "{colors.outline-variant}"
    height: 1px
  section-band:
    backgroundColor: "{colors.surface-container-high}"
    textColor: "{colors.on-surface-variant}"
    padding: 24px
```

- **主要ボタン**：紅殻の面に白文字。1画面に1つ。ホバーで一段暗く（bengara-700）、フォーカス時は 2px の藍の輪郭線を 2px 離して表示する。
- **副ボタン**：生成りの面に木色（#90745E）の 1px 枠線、墨の文字。
- **入力欄**：白地に木色の 1px 枠線（3:1 以上を確保）。ラベルは常に欄の上に表示し、プレースホルダーをラベルの代わりにしない。エラー時は枠線を 2px のエラー色にし、欄の下に「！」アイコンと文言を出す。
- **カード**：生成り濃（#F0E7DF）の面。影は付けない。
- **お知らせ帯**：金箔の面に墨の文字。重要なお知らせ1件だけに使う。
- **ヘッダー**：生成りの面、下端に木色・淡（#BEAA99）の 1px 罫線。現在いるメニュー項目は紅殻の 3px 下線で示す。
- **ブランド帯**：ページ最上端の高さ 6px の木色の帯。金沢らしさを示す唯一の「飾り」。
- **区切り帯（section-band）**：区切り面（#E2D3C5）に墨・淡の文字。フッターや補足情報のまとまりに使う。
- **リンク**：藍の文字に常に下線。訪問済みも同じ色でよい（色の種類を増やさない）。

## Do's and Don'ts

- Do：色を足したくなったら、まず景観計画の禁止色ルール（R・YR は彩度6、Y は彩度4、その他は彩度2まで）に収まるかを確かめる。収まらない色は使わない。
- Do：目立たせたいときは、色ではなく、余白・文字の太さ・配置で目立たせる。
- Do：本文テキストは 4.5:1 以上、枠線やアイコンは 3:1 以上のコントラストを保つ。
- Do：状態（エラー・成功・現在地）は、色に加えてアイコン・文言・下線など色以外の手がかりでも示す。
- Don't：紅殻を広い面（背景全体、ヘッダー全面）に使わない。紅殻は格子の「線」の色であり、「地」の色ではない。
- Don't：蛍光色、純色の原色、グラデーション、ネオン調の発光表現を使わない。
- Don't：木色（#90745E）を本文の文字色にしない（背景との比が 3.92:1 で足りない）。
- Don't：金箔（#C3AB7B）を線や文字に使わない（面としてだけ使う）。
- Don't：金沢市の市章や、許可が必要なロゴマークを、このシステムの一部として埋め込まない。

## Provenance

このファイルの数値がどこから来たかの記録（DESIGN.md 仕様にない独自セクション。仕様上、未知の見出しはそのまま保持される）。

| 項目 | 出典 | 扱い |
|---|---|---|
| 推奨色の範囲（5YR〜2.5Y、明度4〜7、彩度2〜4） | 金沢市景観計画 2-9/2-10「色彩基準等について」 | 木色系トークンの中心と範囲 |
| 禁止色（R・YR 彩度6超／Y 彩度4超／その他 彩度2超／蛍光色） | 同上 | 全トークンの彩度の上限として自主適用 |
| 「目立つより、溶け込む」 | 金沢市屋外広告物ガイドライン | Overview と Do's の方針 |
| フォント、サイズの段階、太さ2種、44px のタップ領域 | デジタル庁デザインシステム（design-tokens, MIT） | Typography と Layout |
| DESIGN.md の書式 | google-labs-code/design.md（Apache 2.0, alpha） | ファイル全体の構造 |

注意：景観計画の色彩基準は **建築物の外壁などの基調色** についてのもので、Web 画面に適用する義務はない。ここでは「金沢らしさ」を数値で表した手がかりとして借りている。
