from manim import *

GREEN = "#d2da22"; INK = "#000000"; MUTED = "#595757"; GRAY = "#efefef"
FONT = "Noto Sans CJK JP"
config.background_color = WHITE
STEPS = [("①","目的を決める","企画"),("②","事実を確定する","原稿の確定"),("③","文面を書く","原稿・コピー"),
         ("④","素材を選ぶ","素材の手配"),("⑤","配置を考える","ラフ"),("⑥","色・書体を決める","カンプ"),
         ("⑦","本番データを作る","入稿データ"),("⑧","確かめる","文字校正・色校正"),("⑨","承認して出す","校了・掲示")]

def T(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)

class Process(Scene):
    def construct(self):
        title = T("ポスター作りは、9つの工程に分かれている", 40, weight=BOLD).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN*0.2), run_time=0.8)
        boxes = VGroup()
        for n, name, alias in STEPS:
            r = RoundedRectangle(corner_radius=0.12, width=3.9, height=1.35, fill_color=GRAY, fill_opacity=1, stroke_color=GRAY, stroke_width=2)
            t1 = T(f"{n} {name}", 30, weight=BOLD)
            t2 = T(alias, 22, MUTED)
            g = VGroup(t1, t2).arrange(DOWN, buff=0.12).move_to(r)
            boxes.add(VGroup(r, g))
        boxes.arrange_in_grid(rows=3, cols=3, buff=(0.45, 0.4)).next_to(title, DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.15) for b in boxes], lag_ratio=0.18), run_time=3.2)
        self.wait(0.8)

        # 一気に作らせると、工程が消える
        one = RoundedRectangle(corner_radius=0.15, width=8, height=2.2, fill_color=GRAY, fill_opacity=1, stroke_width=0).move_to(boxes)
        one_t = T("「いい感じのポスターを作って」", 38, weight=BOLD).move_to(one)
        cap1 = T("一気に作らせると、工程が見えなくなる", 32, MUTED).to_edge(DOWN, buff=0.7)
        saved = boxes.copy()
        self.play(FadeTransform(boxes, VGroup(one, one_t)), FadeIn(cap1), run_time=1.4)
        self.wait(1.6)
        self.play(FadeTransform(VGroup(one, one_t), saved), FadeOut(cap1), run_time=1.2)
        boxes = saved

        # AIに案を出させる工程（⑤⑥）
        ai = [boxes[4], boxes[5]]
        cap2 = T("⑤ラフ ⑥カンプ ― AIに案を何枚も出させ、人が選ぶ", 32, weight=BOLD).to_edge(DOWN, buff=0.7)
        self.play(*[b[0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN) for b in ai], FadeIn(cap2), run_time=1.0)
        self.play(*[Indicate(b, scale_factor=1.06, color=None) for b in ai], run_time=0.8)
        self.wait(1.6)

        # 事実と承認は人
        human = [boxes[1], boxes[6], boxes[7], boxes[8]]
        cap3 = T("② ⑦ ⑧ ⑨ ― 事実・本番データ・確認・承認は、人", 32, weight=BOLD).to_edge(DOWN, buff=0.7)
        self.play(*[b[0].animate.set_stroke(INK, width=7) for b in human], FadeOut(cap2), FadeIn(cap3), run_time=1.2)
        self.wait(1.2)

        # ⑧から②へ：元と見比べる
        cap4 = T("⑧ 確かめるときは、② で確定した事実と見比べる", 32, weight=BOLD).to_edge(DOWN, buff=0.7)
        self.play(FadeOut(cap3), FadeIn(cap4), run_time=0.6)
        self.play(Circumscribe(boxes[1], color=INK, buff=0.08, time_width=1.5), Circumscribe(boxes[7], color=INK, buff=0.08, time_width=1.5), run_time=1.6)
        self.wait(1.4)

        final = T("AIに任せるのは「案」まで。事実と判断は手放さない。", 38, weight=BOLD).to_edge(DOWN, buff=0.85)
        self.play(FadeOut(cap4), FadeIn(final), run_time=1.0)
        credit = T("この動画は、AI（Claude）が manim のコードを書いて作成しました", 20, MUTED).to_corner(DR, buff=0.15)
        self.play(FadeIn(credit), run_time=0.6)
        self.wait(3)
