---
version: alpha
name: Kanazawa Koshiki
description: >-
  金沢市公式ホームページ（いいね金沢）の画面から色・文字・部品の作りを読み取り、
  金沢市カラーユニバーサルデザインガイドラインのルールを重ねた、非公式の試作デザインシステム（v2）。
---

# 金沢版 DESIGN.md v2「公式サイト調」— 非公式試作

> **非公式版です。** これは金沢市が作成・公開したものではなく、講演のデモとして作った試作です。金沢市公式ホームページの見た目を参考にしていますが、市の公式なデザインシステムやガイドラインではありません。市章・公式ロゴ・キャラクターは含みません。

> 金沢市の公式なデザインシステムではありません。2026年11月18日に金沢市公式ホームページのトップページを
> ブラウザで開き、実際に使われている色・書体・角丸を読み取って作った試作です（講演「画像生成AIでDX」のデモ用）。
> v1「木色」は建物の外壁向けの景観基準を元にしたため、印刷物には淡すぎた。v2 はその反省から、
> **画面・印刷物のために作られたもの**だけを元にしている。

## Overview

**白地に深紅、ところどころに金と生成り**。城下町の格式と、行政サイトとしての分かりやすさを両立させる。

- 主役は白い地と濃い灰色（#333333）の文字。深紅（#990000）は「押す場所」「いま選ばれている場所」「区切りの見出し」に使う。
- 公式サイトでは、深紅の塗りのタブやボタンと、生成り・ベージュの面が組み合わされている。見出しは中央そろえの太字で、上に金色の市松模様の飾り、下に小さな英語の副題が付く。
- 金沢市カラーユニバーサルデザインガイドラインに従い、**色だけで意味を伝えない**。特に深紅の文字は、P型の色覚では #333333 の文字とほぼ同じ暗さに見える（シミュレーションでコントラスト比 1.04）。深紅で強調するときは、必ず太字・下線・囲みなど色以外の手がかりも付ける。
- 雰囲気：きちんとしている、温かい、信頼できる。派手さより、迷わせないこと。

## Colors

公式サイトのスタイルシート（top.css）で使用回数の多い色と、ページ上で面積の大きい色を元にした。

- **深紅 / Shu（#990000）**：公式サイトで最も多く使われている色。塗りのタブ、検索ボタン、強調した日付、ボタンの枠に使う。白地とのコントラスト比 8.92。
- **深紅・濃 / Shu Deep（#7A0000）**：押したとき・ホバー時。
- **墨 / Sumi（#333333）**：本文。公式サイトの本文色と同じ。
- **灰 / Hai（#666666）**：補足文。白地で 5.74、ベージュ地で 4.75。
- **生成り / Kinari（#F8F5EE）**：大きな面の背景。公式サイトの背景帯の色。
- **砂 / Suna（#F1E9D5）**：検索欄などのまとまりを囲む面。
- **金 / Kin（#E8BB5E）**：市松模様などの**飾り専用**。白地とのコントラストは 1.79 しかないので、文字や意味のある線には使わない。金の面の上に墨の文字を載せるのは可（7.04）。
- **金・濃 / Kin Deep（#8A6514）**：金色で文字を書く必要があるとき（白地で 5.31）。
- **藍 / Ai（#2D5F92）**：リンク。公式サイトのリンク色と同じ。常に下線を付ける。
- **境界 / Sakai（#78776B）**：入力欄の枠線（白地で 4.52）。
- **警告 / Error（#B81C22）**：エラー。深紅と色味が近いので、必ずアイコンと文言を添える。

```yaml
colors:
  shu-600: "#990000"
  shu-700: "#7A0000"
  sumi-900: "#333333"
  hai-600: "#666666"
  kinari-50: "#F8F5EE"
  suna-100: "#F1E9D5"
  kin-300: "#E8BB5E"
  kin-700: "#8A6514"
  ai-600: "#2D5F92"
  sakai-500: "#78776B"
  error-600: "#B81C22"
  primary: "{colors.shu-600}"
  primary-hover: "{colors.shu-700}"
  on-primary: "#FFFFFF"
  secondary: "{colors.suna-100}"
  tertiary: "{colors.kin-300}"
  tertiary-text: "{colors.kin-700}"
  neutral: "#FFFFFF"
  surface: "{colors.neutral}"
  surface-container: "{colors.kinari-50}"
  surface-container-high: "{colors.suna-100}"
  on-surface: "{colors.sumi-900}"
  on-surface-variant: "{colors.hai-600}"
  outline: "{colors.sakai-500}"
  link: "{colors.ai-600}"
  error: "{colors.error-600}"
```

| 前景 / 背景 | 比 | 用途 |
|---|---|---|
| 墨 / 白 | 12.63 | 本文 |
| 墨 / 砂 | 10.44 | 囲み面の文字 |
| 白 / 深紅 | 8.92 | 塗りのボタン・タブ |
| 深紅 / 白 | 8.92 | 枠のボタン、強調の日付（太字と併用） |
| 藍 / 白 | 6.64 | リンク（下線と併用） |
| 墨 / 金 | 7.04 | 金の面の上の文字 |
| 金 / 白 | 1.79 | 飾りのみ |

## Typography

公式サイトは **游ゴシック** を指定している（`游ゴシック体, YuGothic, 游ゴシック, Yu Gothic, …, Meiryo, sans-serif`）。これに合わせ、游ゴシックがない環境では Noto Sans JP で代える。本文の基準は公式サイトと同じ 14.4px 相当だが、印刷物では 16px（12pt）以上にする。太さは 400 と 700 の2種類。明朝体は使わない。

```yaml
typography:
  headline-display:
    fontFamily: Yu Gothic
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.35
    letterSpacing: 0.04em
  headline-lg:
    fontFamily: Yu Gothic
    fontSize: 29px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0.04em
  headline-md:
    fontFamily: Yu Gothic
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.45
    letterSpacing: 0.06em
  headline-sm:
    fontFamily: Yu Gothic
    fontSize: 17px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0.04em
  body-lg:
    fontFamily: Yu Gothic
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.7
  body-md:
    fontFamily: Yu Gothic
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.7
  body-sm:
    fontFamily: Yu Gothic
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.7
  label-md:
    fontFamily: Yu Gothic
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0.04em
  label-en:
    fontFamily: Yu Gothic
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: 0.04em
```

- 見出しの英語の副題（label-en）は飾り。11px で墨色。意味のある情報は入れない。

## Layout

中央そろえの見出しで区切ったブロックを縦に積む。コンテンツ幅は最大 960px。ブロックの間は広め（64px）、ブロックの中は 16〜24px。

```yaml
spacing:
  base: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  gutter: 16px
  content-max: 960px
  tap-target: 44px
```

## Elevation & Depth

基本は平面。白いカードを生成りの面に置くときだけ、ごく淡い影（`0 1px 4px rgba(0,0,0,.08)`）を付ける。それ以外は、面の色（白 → 生成り → 砂）と深紅の線で階層を表す。

## Shapes

角丸は小さい（公式サイトでは 2〜6px が多い）。ボタン・入力欄・カードは 5px。アイコンの台座だけ正円。

```yaml
rounded:
  none: 0px
  sm: 3px
  md: 5px
  lg: 6px
  full: 9999px
```

## Components

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 12px 32px
    height: 48px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  button-outline:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: 12px 48px
    height: 48px
  tab-active:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.headline-sm}"
    rounded: "{rounded.sm}"
    padding: 12px 24px
  tab-inactive:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.headline-sm}"
    rounded: "{rounded.sm}"
    padding: 12px 24px
  panel:
    backgroundColor: "{colors.surface-container-high}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.none}"
    padding: 24px
  page-band:
    backgroundColor: "{colors.surface-container}"
    textColor: "{colors.on-surface}"
    padding: 64px 16px
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.md}"
    padding: 16px 24px
  section-heading:
    textColor: "{colors.on-surface}"
    typography: "{typography.headline-md}"
  section-heading-en:
    textColor: "{colors.on-surface}"
    typography: "{typography.label-en}"
  ornament-ichimatsu:
    backgroundColor: "{colors.tertiary}"
    height: 8px
    width: 48px
  date-label:
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
  gold-text:
    textColor: "{colors.tertiary-text}"
    typography: "{typography.label-md}"
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px 16px
    height: 48px
  link:
    textColor: "{colors.link}"
    typography: "{typography.body-md}"
  notice-error:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.error}"
    typography: "{typography.label-md}"
  supporting-text:
    textColor: "{colors.on-surface-variant}"
    typography: "{typography.body-sm}"
  input-outline:
    backgroundColor: "{colors.outline}"
    width: 1px
```

- **塗りのボタン**：深紅の面に白文字。検索・申込など、1画面で一番大事な操作。
- **枠のボタン**：白地に深紅の 1px 枠、墨の文字。右端に深紅の丸に白い矢印（›）を置く。公式サイトの「新着情報一覧」と同じ作り。
- **タブ**：選ばれていないタブは深紅の塗りに白文字、選ばれているタブは白地で上辺に深紅の 3px 線、文字も深紅で太字。
- **見出し（section-heading）**：中央そろえ、太字。上に金の市松模様の飾り（幅 48px、高さ 8px、左右に1つずつ）、下に英語の副題。
- **囲み面（panel）**：砂色の面。検索欄やお知らせのまとまりに使う。
- **日付・強調**：深紅の太字。色だけで区別しない（太字であることが手がかり）。
- **リンク**：藍の文字に下線。

## Do's and Don'ts

- Do：深紅は「押す場所」「選ばれている場所」「強調」に絞り、広い背景には使わない（使うのはタブやボタンの大きさまで）。
- Do（例外）：チラシ・ポスターなど印刷物の表紙では、上部（タイトルとリード文）だけ深紅の面にし、文字を白抜きにしてよい。遠くから一瞬で目を引くため。本文部分は白地に戻す。（2026-11-18 追記：v2 フライヤーへの赤入れ①を採用）
- Do：深紅で文字を強調するときは、太字・下線・囲みなどを必ず併用する（P型の色覚では深紅と墨の区別がほぼつかない）。
- Do：背景と文字には、はっきりした明暗差をつける（本文 4.5:1 以上）。
- Do：白黒で印刷しても内容が伝わるかを確かめる。
- Don't：金（#E8BB5E）を文字や細い線に使わない。飾り専用。
- Don't：白地の細い線や小さな文字に黄色・水色を使わない。
- Don't：パステル調の淡い色どうしを組み合わせない。
- Don't：加賀五彩などの伝統色を、分類や強調の手段に使わない（装飾だけにする）。
- Don't：金沢市の市章、公式ロゴ、キャラクター（利家さん等）を、このシステムの一部として使わない。公式のものに見せかけない。

## Provenance

| 項目 | 出典 | 扱い |
|---|---|---|
| 深紅・生成り・砂・金・藍・墨、角丸、書体 | 金沢市公式ホームページ トップページ（2026-11-18 にブラウザで計測、top.css と算出スタイル） | Colors / Typography / Shapes |
| タブ・枠ボタン・中央見出しと市松の飾り | 同上（画面の観察） | Components |
| 色だけに頼らない、明暗差、黄色・水色、パステル、加賀五彩、白黒確認 | 金沢市カラーユニバーサルデザインガイドライン | Overview / Do's and Don'ts |
| 深紅と墨の見分けにくさ（P型で 1.04） | colour-science 0.4.7 の Machado(2009) 色覚シミュレーションで計算 | Overview |
| DESIGN.md の書式 | google-labs-code/design.md（Apache 2.0, alpha） | 全体 |

v1「木色」（景観計画の色彩基準ベース）は `../DESIGN.md` に残してある。
