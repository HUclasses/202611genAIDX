"""拡散モデル解説アニメ用の共通部品。

- 元画像：numpy で描いた簡単な風景（オリジナル）
- 順方向：x_t = sqrt(abar) x0 + sqrt(1-abar) eps を実際に計算
- 2次元の逆過程：混合ガウス分布ならスコア（ノイズの最適予測）が厳密に計算できるので、
  それを使って DDPM の逆過程を実際に走らせる（作り物の軌跡ではない）
"""
import numpy as np
from manim import ImageMobject, RESAMPLING_ALGORITHMS

JP = "Noto Sans CJK JP"
SIZE = 256
RNG_SEED = 7

# ---------------------------------------------------------------- 画像

def make_image(n=SIZE):
    """[-1,1] の RGB 画像（空・太陽・山・地面・家）。"""
    y, x = np.mgrid[0:n, 0:n] / n
    img = np.zeros((n, n, 3))
    # 空のグラデーション
    sky = np.stack([0.35 + 0.3 * y, 0.6 + 0.25 * y, 0.95 - 0.1 * y], -1)
    img[:] = sky
    # 太陽
    sun = (x - 0.75) ** 2 + (y - 0.22) ** 2 < 0.11 ** 2
    img[sun] = [1.0, 0.85, 0.2]
    # 山
    m1 = y > 0.62 - 0.9 * (0.28 - np.abs(x - 0.30))
    m2 = y > 0.66 - 0.9 * (0.22 - np.abs(x - 0.62))
    img[m2] = [0.30, 0.42, 0.55]
    img[m1] = [0.22, 0.32, 0.45]
    # 地面
    ground = y > 0.70
    img[ground] = np.stack([0.25 + 0 * y, 0.6 - 0.2 * (y - 0.7), 0.25 + 0 * y], -1)[ground]
    # 家
    house = (x > 0.58) & (x < 0.80) & (y > 0.62) & (y < 0.82)
    img[house] = [0.95, 0.92, 0.85]
    roof = (y > 0.50) & (y <= 0.62) & (np.abs(x - 0.69) < (y - 0.50) * 1.1)
    img[roof] = [0.75, 0.15, 0.15]
    door = (x > 0.66) & (x < 0.72) & (y > 0.70) & (y < 0.82)
    img[door] = [0.45, 0.28, 0.15]
    return img * 2 - 1


def make_noise(n=SIZE, seed=RNG_SEED):
    return np.random.default_rng(seed).standard_normal((n, n, 3))


def mix(x0, eps, s):
    """s = sqrt(abar)（画像の割合）。ノイズの割合は sqrt(1-s^2)。"""
    return s * x0 + np.sqrt(max(0.0, 1 - s * s)) * eps


def block_blur(x, k):
    n = x.shape[0]
    m = n // k
    b = x[: m * k, : m * k].reshape(m, k, m, k, 3).mean(axis=(1, 3))
    return np.repeat(np.repeat(b, k, 0), k, 1)


def to_uint8(x, lo=-1.0, hi=1.0):
    return (np.clip((x - lo) / (hi - lo), 0, 1) * 255).astype(np.uint8)


def img_mob(x, height=3.0, lo=-1.0, hi=1.0):
    m = ImageMobject(to_uint8(x, lo, hi))
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    m.height = height
    return m


def gauss_blur(x, sigma):
    from scipy.ndimage import gaussian_filter
    return np.stack([gaussian_filter(x[..., c], sigma, mode="reflect") for c in range(3)], -1)


def auto_contrast(x):
    """ぼかした画像は振幅が小さいので、見やすく引き伸ばす（表示上の調整）。"""
    c = x - x.mean((0, 1))
    return c / (np.percentile(np.abs(c), 98) + 1e-9)


# ---------------------------------------------------------------- 2次元の混合ガウス

# 3つの「山」＝3種類の画像（猫・車・海）のたとえ
MUS = np.array([[-2.2, 1.4], [2.2, 1.4], [0.0, -2.2]])
LABELS = ["猫", "車", "海"]
SIG = 0.35  # 各山の広がり
T = 200
BETAS = np.linspace(1e-4, 0.06, T)
ALPHAS = 1 - BETAS
ABARS = np.cumprod(ALPHAS)


def eps_hat(x, t, comps=None):
    """時刻 t の x に対する「混ぜたノイズ」の最適予測 E[eps | x_t]（厳密）。
    comps でどの山に条件づけるかを指定（None なら全部＝プロンプトなし）。"""
    ab = ABARS[t]
    idx = range(len(MUS)) if comps is None else comps
    var = ab * SIG**2 + (1 - ab)
    mus = np.sqrt(ab) * MUS[list(idx)]  # (K,2)
    d = x[:, None, :] - mus[None]  # (N,K,2)
    logw = -(d**2).sum(-1) / (2 * var)
    logw -= logw.max(1, keepdims=True)
    w = np.exp(logw)
    w /= w.sum(1, keepdims=True)
    score = -(w[..., None] * d).sum(1) / var
    return -np.sqrt(1 - ab) * score


def x0_hat(x, t, comps=None):
    ab = ABARS[t]
    return (x - np.sqrt(1 - ab) * eps_hat(x, t, comps)) / np.sqrt(ab)


def guided_eps(x, t, comps, w):
    eu = eps_hat(x, t, None)
    ec = eps_hat(x, t, comps)
    return eu + w * (ec - eu)


def sample(n=250, seed=3, comps=None, w=1.0, keep_every=1):
    """DDPM の逆過程を実際に走らせ、各ステップの位置を返す。
    返り値: traj[k] は「ノイズの多い順」に k 番目の状態 (n,2)、ts[k] はその時刻。"""
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((n, 2))
    traj, ts = [x.copy()], [T - 1]
    for t in range(T - 1, -1, -1):
        e = eps_hat(x, t) if comps is None else guided_eps(x, t, comps, w)
        mean = (x - BETAS[t] / np.sqrt(1 - ABARS[t]) * e) / np.sqrt(ALPHAS[t])
        if t > 0:
            sig = np.sqrt(BETAS[t] * (1 - ABARS[t - 1]) / (1 - ABARS[t]))
            x = mean + sig * rng.standard_normal(x.shape)
        else:
            x = mean
        traj.append(x.copy())
        ts.append(t - 1)
    traj = np.array(traj)[::keep_every]
    ts = np.array(ts)[::keep_every]
    return traj, ts
