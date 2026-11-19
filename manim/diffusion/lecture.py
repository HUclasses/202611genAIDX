"""講演用：画像生成AI（拡散モデル）のしくみ（数式なし・約2分）

レンダリング例：
    manim -qh lecture.py L0Title L1Forward L2Training L3Blur L4Reverse L5Prompt L6Summary
画像・ノイズ・2次元の点の動きは、すべて実際に計算したもの（common.py）。
"""
from manim import *
from common import *

config.background_color = "#14161c"

C_IMG = "#7fb6ff"
C_NOISE = "#ff9f6b"
C_AI = "#b58cff"
C_OK = "#7ee08a"


def jt(s, size=34, color=WHITE, **kw):
    return Text(s, font=JP, font_size=size, color=color, **kw)


class Cap:
    """画面下のキャプション（入れ替え用）。"""

    def __init__(self, scene):
        self.scene = scene
        self.m = None

    def show(self, s, size=32, rt=0.6):
        new = jt(s, size).to_edge(DOWN, buff=0.45)
        if self.m is None:
            self.scene.play(FadeIn(new, shift=UP * 0.2), run_time=rt)
        else:
            self.scene.play(FadeOut(self.m), FadeIn(new, shift=UP * 0.2), run_time=rt)
        self.m = new

    def clear(self):
        if self.m is not None:
            self.scene.play(FadeOut(self.m), run_time=0.4)
            self.m = None


def heading(scene, s):
    h = jt(s, 40).to_edge(UP, buff=0.4)
    scene.play(Write(h), run_time=0.8)
    return h


X0 = make_image()
EPS = make_noise()


# ------------------------------------------------------------------ 0
class L0Title(Scene):
    def construct(self):
        t = jt("画像生成AIは、どうやって絵を描くのか", 48)
        s = jt("ノイズから、少しずつ戻していく", 34, color=GRAY_B).next_to(t, DOWN, buff=0.5)
        self.play(Write(t), run_time=1.5)
        self.play(FadeIn(s, shift=UP * 0.2))
        self.wait(2.5)
        self.play(FadeOut(t), FadeOut(s))


# ------------------------------------------------------------------ 1
class L1Forward(Scene):
    def construct(self):
        h = heading(self, "① 画像にノイズを混ぜていく")
        cap = Cap(self)
        s = ValueTracker(1.0)
        img = always_redraw(lambda: img_mob(mix(X0, EPS, s.get_value()), 4.2).shift(LEFT * 2.6 + DOWN * 0.2))

        # 割合バー
        def bars():
            v = s.get_value()
            a, b = v, np.sqrt(max(0, 1 - v * v))
            L = 3.6
            g = VGroup()
            r1 = Rectangle(width=max(L * a, 0.01), height=0.4, fill_color=C_IMG, fill_opacity=1, stroke_width=0)
            r2 = Rectangle(width=max(L * b, 0.01), height=0.4, fill_color=C_NOISE, fill_opacity=1, stroke_width=0)
            l1 = jt("画像", 28, C_IMG)
            l2 = jt("ノイズ", 28, C_NOISE)
            l1.move_to([1.6, 0.9, 0], aligned_edge=LEFT)
            r1.next_to(l1, DOWN, buff=0.15, aligned_edge=LEFT)
            l2.move_to([1.6, -0.6, 0], aligned_edge=LEFT)
            r2.next_to(l2, DOWN, buff=0.15, aligned_edge=LEFT)
            frame = VGroup(
                Rectangle(width=L, height=0.4, stroke_color=GRAY, stroke_width=1).move_to(r1, aligned_edge=LEFT),
                Rectangle(width=L, height=0.4, stroke_color=GRAY, stroke_width=1).move_to(r2, aligned_edge=LEFT),
            )
            return VGroup(frame, r1, r2, l1, l2)

        bar = always_redraw(bars)
        self.play(FadeIn(img), FadeIn(bar))
        cap.show("ノイズを少しずつ混ぜると、最後は砂嵐になる")
        self.play(s.animate.set_value(0.03), run_time=5, rate_func=linear)
        self.wait(0.5)
        self.play(s.animate.set_value(0.6), run_time=1.2)
        cap.show("この手順は人が決めた固定のレシピ。ここはAIが学ぶ部分ではない")
        self.wait(2.5)
        cap.show("どの段階も「画像とノイズを決まった割合で混ぜたもの」")
        self.play(s.animate.set_value(0.25), run_time=1.2)
        self.play(s.animate.set_value(0.85), run_time=1.2)
        self.wait(1.5)
        cap.clear()
        self.play(FadeOut(VGroup(h, bar)), FadeOut(img))


# ------------------------------------------------------------------ 2
class L2Training(Scene):
    def construct(self):
        h = heading(self, "② AIの練習：「どのノイズを混ぜたか」を当てる")
        cap = Cap(self)
        H = 1.8
        a = img_mob(X0, H).move_to([-5.4, 1.2, 0])
        b = img_mob(EPS, H).move_to([-5.4, -1.4, 0])
        la = jt("元の画像", 24).next_to(a, UP, buff=0.12)
        lb = jt("混ぜたノイズ", 24, C_NOISE).next_to(b, DOWN, buff=0.12)
        xt = img_mob(mix(X0, EPS, 0.5), H).move_to([-2.2, -0.1, 0])
        lxt = jt("混ぜた画像", 24).next_to(xt, UP, buff=0.12)
        ar1 = Arrow(a.get_right(), xt.get_left() + UP * 0.3, buff=0.1)
        ar2 = Arrow(b.get_right(), xt.get_left() + DOWN * 0.3, buff=0.1)
        ai = RoundedRectangle(corner_radius=0.2, width=1.8, height=1.4, color=C_AI, fill_opacity=0.15).move_to([0.6, -0.1, 0])
        lai = jt("AI", 40, C_AI).move_to(ai)
        ar3 = Arrow(xt.get_right(), ai.get_left(), buff=0.1)
        pred = Square(side_length=H, color=C_AI).move_to([3.6, -0.1, 0])
        q = jt("?", 72, C_AI).move_to(pred)
        lp = jt("予想したノイズ", 24, C_AI).next_to(pred, UP, buff=0.12)
        ar4 = Arrow(ai.get_right(), pred.get_left(), buff=0.1)

        self.play(FadeIn(a), FadeIn(la))
        cap.show("元の画像にノイズを混ぜて、練習問題を作る")
        self.play(FadeIn(b), FadeIn(lb))
        self.play(GrowArrow(ar1), GrowArrow(ar2), FadeIn(xt), FadeIn(lxt))
        self.wait(1)
        cap.show("AIは混ぜた画像を見て、混ぜたノイズを予想する")
        self.play(GrowArrow(ar3), FadeIn(ai), Write(lai))
        self.play(GrowArrow(ar4), Create(pred), FadeIn(q), FadeIn(lp))
        self.wait(1.2)

        # 答え合わせ
        ans = img_mob(EPS, H * 0.8).move_to([6.1, -0.1, 0])
        lans = jt("正解", 24, C_OK).next_to(ans, UP, buff=0.1)
        bb = b.copy()
        self.play(bb.animate.move_to(ans).set_height(H * 0.8), run_time=1.2)
        self.play(FadeIn(lans))
        cmp = DoubleArrow(pred.get_right(), ans.get_left(), buff=0.08, color=C_OK)
        lc = jt("答え合わせ", 24, C_OK).next_to(cmp, DOWN, buff=0.9)
        self.play(GrowArrow(cmp), FadeIn(lc))
        cap.show("ノイズを混ぜたのは自分自身。だから正解を知っている")
        self.wait(2.5)
        cap.show("大量の画像で繰り返し、「画像らしくない成分」を見分ける力をつける", 30)
        self.wait(3)
        cap.clear()
        self.play(*[FadeOut(m) for m in self.mobjects])


# ------------------------------------------------------------------ 3
class L3Blur(Scene):
    def construct(self):
        h = heading(self, "③ ノイズまみれでも、大まかな構図は残っている")
        cap = Cap(self)
        sv = 0.12
        xt = mix(X0, EPS, sv)
        H = 3.8
        left = img_mob(xt, H).move_to([-3.3, 0.1, 0])
        ll = jt("1ピクセルずつ見ると…", 26).next_to(left, UP, buff=0.15)
        self.play(FadeIn(left), FadeIn(ll))
        cap.show("ノイズがかなり多い段階。画像の成分は1割ちょっと")
        self.wait(2)

        sig = ValueTracker(0.01)
        right = always_redraw(
            lambda: img_mob(auto_contrast(gauss_blur(xt, sig.get_value())) if sig.get_value() > 0.5 else xt, H).move_to([3.3, 0.1, 0])
        )
        lr = jt("広い範囲で平均すると…", 26).next_to(left, UP, buff=0.15).set_x(3.3)
        self.play(FadeIn(right), FadeIn(lr))
        cap.show("ノイズはバラバラなので、平均すると打ち消し合う")
        self.play(sig.animate.set_value(10), run_time=3)
        note = jt("※明るさを強調して表示", 20, GRAY).next_to(right, DOWN, buff=0.1, aligned_edge=RIGHT)
        self.play(FadeIn(note))
        self.wait(1)
        cap.show("空・太陽・山・地面…大まかな配置が見えてくる")
        ref = img_mob(X0, 1.4).next_to(right, RIGHT, buff=0.15).align_to(right, UP)
        lref = jt("元の画像", 20).next_to(ref, DOWN, buff=0.08)
        self.play(FadeIn(ref), FadeIn(lref))
        self.wait(2.5)
        cap.show("だから生成は「まず大まかな構図、あとで細部」の順に進む")
        self.wait(3)
        cap.clear()
        self.play(*[FadeOut(m) for m in self.mobjects])


# ------------------------------------------------------------------ 4,5 共通（2次元の地図）
PLANE_SCALE = 0.78
PLANE_SHIFT = UP * 0.35


def P(xy):
    return np.array([xy[0] * PLANE_SCALE, xy[1] * PLANE_SCALE, 0]) + PLANE_SHIFT


def regions(highlight=None):
    g = VGroup()
    for i, (mu, lab) in enumerate(zip(MUS, LABELS)):
        c = Circle(radius=SIG * 2.6 * PLANE_SCALE, color=C_IMG, fill_opacity=0.12, stroke_opacity=0.5).move_to(P(mu))
        t = jt(f"{lab}の画像", 24, C_IMG).next_to(c, UP if mu[1] > 0 else DOWN, buff=0.08)
        if highlight is not None and i != highlight:
            c.set_opacity(0.05)
            t.set_opacity(0.35)
        g.add(VGroup(c, t))
    return g


GRID = np.array([[x, y] for x in np.arange(-8.0, 8.1, 0.8) for y in np.arange(-3.6, 3.7, 0.8)])


def field(t, comps=None, w=1.0, color=GRAY_B):
    t = int(np.clip(t, 0, T - 1))
    e = eps_hat(GRID, t) if comps is None else guided_eps(GRID, t, comps, w)
    d = -e  # 「画像らしい方向」（スコアの向き）
    n = np.linalg.norm(d, axis=1) + 1e-9
    g = VGroup()
    for p, v, m in zip(GRID, d, n):
        u = v / m * 0.32
        g.add(
            Arrow(P(p), P(p + u), buff=0, stroke_width=2.2, max_tip_length_to_length_ratio=0.35, color=color).set_opacity(
                float(np.clip(m / 1.2, 0.15, 0.85))
            )
        )
    return g


def setup_points(scene, traj, ts, comps=None, w=1.0, color=YELLOW):
    """点・矢印・カウンタを初期状態で表示し、進める用の ValueTracker を返す。"""
    k = ValueTracker(0)
    K = len(traj) - 1

    def pos(i):
        kv = k.get_value()
        i0 = int(np.floor(kv))
        i1 = min(i0 + 1, K)
        f = kv - i0
        return P(traj[i0][i] * (1 - f) + traj[i1][i] * f)

    dots = VGroup(*[Dot(radius=0.035, color=color) for _ in range(traj.shape[1])])

    def upd(g):
        for i, d in enumerate(g):
            d.move_to(pos(i))

    dots.add_updater(upd)
    upd(dots)
    arrows = always_redraw(lambda: field(ts[int(k.get_value())], comps, w))
    counter = always_redraw(
        lambda: jt(f"ノイズの量：{np.sqrt(1 - ABARS[max(ts[int(k.get_value())], 0)]) * 100:4.0f}%", 24, GRAY_B).move_to([5.4, -2.45, 0])
    )
    scene.play(FadeIn(arrows), FadeIn(dots), FadeIn(counter))
    return k, K, dots, arrows, counter


def run_points(scene, traj, ts, run_time, comps=None, w=1.0, color=YELLOW):
    k, K, dots, arrows, counter = setup_points(scene, traj, ts, comps, w, color)
    scene.play(k.animate.set_value(K), run_time=run_time, rate_func=linear)
    return dots, arrows, counter


# ------------------------------------------------------------------ 4
class L4Reverse(Scene):
    def construct(self):
        h = heading(self, "④ 生成：ノイズから少しずつ戻す")
        cap = Cap(self)
        reg = regions()
        self.play(FadeIn(reg))
        cap.show("画像の世界を地図にしたイメージ。点1つ＝画像1枚", 30)
        self.wait(2.5)
        cap.show("丸の中は「ありそうな画像」が集まる場所", 30)
        self.wait(2)
        traj, ts = sample(n=260, seed=3)
        cap.show("出発点は砂嵐（ノイズ）。矢印はAIの予想が示す「画像らしい方向」", 28)
        k, K, dots, arrows, counter = setup_points(self, traj, ts)
        self.wait(3)
        cap.show("少し進んで、少しノイズを足し直す、を何十回も繰り返す", 30)
        self.play(k.animate.set_value(K), run_time=9, rate_func=linear)
        self.wait(0.5)
        cap.show("最初は「全体の平均」へ。途中から、偶然のゆらぎでどれかに決まる", 28)
        self.wait(3.5)
        cap.clear()
        self.play(*[FadeOut(m) for m in self.mobjects])


# ------------------------------------------------------------------ 5
class L5Prompt(Scene):
    def construct(self):
        h = heading(self, "⑤ 方向を決めるのはプロンプト")
        cap = Cap(self)
        for target, run in [(0, 8), (2, 6)]:
            reg = regions(highlight=target)
            box = VGroup(
                RoundedRectangle(corner_radius=0.15, width=3.6, height=0.8, color=C_AI),
                jt(f"プロンプト：「{LABELS[target]}」", 28, C_AI),
            ).move_to([-5.0, -2.45, 0])
            box[1].move_to(box[0])
            self.play(FadeIn(reg), FadeIn(box))
            if target == 0:
                cap.show("プロンプトを入れると、矢印の向きが変わる", 30)
            else:
                cap.show("同じ砂嵐から出発しても、プロンプトが違えば行き先が変わる", 30)
            traj, ts = sample(n=200, seed=3, comps=[target], w=3.0)
            dots, arrows, counter = run_points(self, traj, ts, run_time=run, comps=[target], w=3.0)
            self.wait(2)
            self.play(FadeOut(VGroup(reg, box, dots, arrows, counter)))
        cap.clear()
        self.play(FadeOut(h))


# ------------------------------------------------------------------ 6
class L6Summary(Scene):
    def construct(self):
        h = jt("まとめ", 44).to_edge(UP, buff=0.6)
        items = VGroup(
            jt("・AIは「混ぜたノイズを当てる」練習を、大量の画像で繰り返す", 30),
            jt("・ノイズまみれでも、大まかな構図は残っている", 30),
            jt("・生成は、砂嵐から少しずつ戻す（構図 → 細部）", 30),
            jt("・どの方向へ戻すかを決めるのがプロンプト", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(h, DOWN, buff=0.7)
        self.play(Write(h))
        for it in items:
            self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(1.6)
        self.wait(2)
        self.play(FadeOut(h), FadeOut(items))
