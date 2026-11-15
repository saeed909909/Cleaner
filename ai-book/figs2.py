"""Illustrations for chapters 6-19. Uses the drawing helpers from figs.py."""
import math
import random
import numpy as np
from figs import svg, t, line, arrow, rect, circ, path, box_label, C, W

MONO = 'font-family="JetBrains Mono, monospace"'


# ------------------------------------------------------------------ chapter 6
def conv():
    h = 200
    b = ""
    img = np.zeros((7, 7))
    img[:, 3:] = 1
    img[1:6, 1] = .5
    cs = 20
    x0, y0 = 10, 30
    b += t(x0 + 70, 18, "Image", 10.5, weight=600)
    for i in range(7):
        for j in range(7):
            v = img[i, j]
            fill = "#ffffff" if v == 0 else ("#9fb3c0" if v == .5 else C["ink"])
            b += f'<rect x="{x0+j*cs}" y="{y0+i*cs}" width="{cs-1}" height="{cs-1}" fill="{fill}" stroke="{C["rule"]}" stroke-width=".6"/>'
    b += rect(x0 + 1*cs - 2, y0 + 2*cs - 2, 3*cs + 3, 3*cs + 3, "none", "amber", 2, 2.6, 'fill-opacity="0"')
    k = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    kx, ky = 195, 60
    b += t(kx + 30, 48, "Kernel (3 × 3)", 10.5, weight=600)
    for i in range(3):
        for j in range(3):
            b += rect(kx + j*22, ky + i*22, 21, 21, "amber_soft", "amber", 2, .8)
            b += t(kx + j*22 + 10.5, ky + i*22 + 15, f"{k[i][j]:+d}", 9.5, extra=MONO)
    b += t(kx + 32, 145, "finds vertical edges", 9, fill="muted")
    b += arrow(155, 90, 188, 90, "amber")
    b += arrow(268, 90, 300, 90)
    fm = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            fm[i, j] = sum(img[i+a, j+c]*k[a][c] for a in range(3) for c in range(3))
    fx, fy = 310, 40
    b += t(fx + 60, 18, "Feature map", 10.5, weight=600)
    mx = np.abs(fm).max() or 1
    for i in range(5):
        for j in range(5):
            v = fm[i, j] / mx
            op = abs(v)
            col = C["sea"] if v >= 0 else C["amber"]
            b += f'<rect x="{fx+j*24}" y="{fy+i*24}" width="23" height="23" fill="{col}" fill-opacity="{0.08+0.85*op:.2f}" stroke="{C["rule"]}" stroke-width=".6"/>'
    b += rect(fx + 0*24 - 1, fy + 1*24 - 1, 25, 25, "none", "amber", 2, 2.4, 'fill-opacity="0"')
    b += t(fx + 60, 182, "bright where the edge is", 9, fill="muted")
    return svg(h, b)


def rnn():
    h = 186
    words = ["The", "whale", "swam", "deep"]
    b = ""
    for i, wd in enumerate(words):
        x = 30 + i*105
        b += box_label(x, 60, 70, 40, "RNN", None, "sea_soft", "sea", 10.5)
        b += arrow(x + 35, 138, x + 35, 103)
        b += t(x + 35, 154, f"“{wd}”", 10, fill="muted")
        b += arrow(x + 35, 58, x + 35, 30)
        b += t(x + 35, 22, f"output {i+1}", 9, fill="muted")
        if i < 3:
            b += arrow(x + 70, 80, x + 103, 80, "amber")
            b += t(x + 87, 73, f"h{i+1}", 9, fill="amber", weight=600)
    b += t(W/2, 180, "the same weights are reused at every step · h = hidden state (memory)", 9, fill="muted")
    return svg(h, b)


def autoencoder():
    h = 190
    sizes = [8, 5, 2, 5, 8]
    xs = [40, 135, 230, 325, 420]
    pos = []
    for x, n in zip(xs, sizes):
        ys = np.linspace(95 - (n-1)*10.5, 95 + (n-1)*10.5, n) if n > 1 else [95]
        pos.append([(x, y) for y in ys])
    b = ""
    b += f'<path d="M40 14 L230 72 L230 118 L40 176 Z" fill="{C["sea_soft"]}" opacity=".7"/>'
    b += f'<path d="M420 14 L230 72 L230 118 L420 176 Z" fill="{C["violet_soft"]}" opacity=".7"/>'
    for A, B in zip(pos, pos[1:]):
        for (x1, y1) in A:
            for (x2, y2) in B:
                b += line(x1, y1, x2, y2, "muted", .5, 'opacity=".5"')
    for li, L in enumerate(pos):
        for (x, y) in L:
            b += circ(x, y, 6.5, "amber_soft" if li == 2 else "paper", "ink", 1.1)
    b += t(130, 188, "Encoder: compress", 9.5, weight=600, fill="sea")
    b += t(330, 188, "Decoder: rebuild", 9.5, weight=600, fill="violet")
    b += t(230, 60, "latent code", 9.5, weight=600, fill="amber")
    b += t(40, 8, "input", 9, fill="muted") + t(420, 8, "copy of input", 9, fill="muted")
    return svg(h, b)


def gan():
    h = 190
    b = ""
    b += box_label(8, 30, 70, 36, "Noise", "random numbers", "grey", "muted", 10)
    b += box_label(110, 26, 96, 44, "Generator", "the forger", "amber_soft", "amber", 10.5)
    b += box_label(238, 30, 72, 36, "Fake", "image", "grey", "muted", 10)
    b += box_label(238, 112, 72, 36, "Real", "images", "grey", "muted", 10)
    b += box_label(340, 66, 112, 44, "Discriminator", "the detective", "sea_soft", "sea", 10.5)
    b += arrow(78, 48, 108, 48) + arrow(206, 48, 236, 48)
    b += arrow(310, 50, 338, 78) + arrow(310, 128, 338, 100)
    b += t(396, 130, "“real or fake?”", 9.5, fill="muted")
    b += path([(396, 140), (396, 172), (158, 172), (158, 72)], "amber", 1.4, 'stroke-dasharray="4 3" marker-end="url(#ara)"')
    b += t(277, 166, "feedback: how it was caught", 9, fill="amber")
    return svg(h, b)


def _noisy_panel(x0, y0, size, noise, seed):
    rng = np.random.default_rng(seed)
    n = 14
    cs = size / n
    out = rect(x0, y0, size, size, "paper", "rule", 3)
    for i in range(n):
        for j in range(n):
            cx, cy = (j + .5) / n - .5, (i + .5) / n - .5
            base = 0.0
            if cx*cx + (cy + .05)**2 < .13: base = 1.0         # face
            if (cx + .13)**2 + (cy + .12)**2 < .004 or (cx - .13)**2 + (cy + .12)**2 < .004: base = 0.0
            if abs(cy - .12) < .035 and abs(cx) < .16: base = 0.0
            v = (1 - noise) * base + noise * rng.random()
            v = min(1, max(0, v + (rng.normal(0, .25) * noise)))
            if v > .08:
                out += f'<rect x="{x0+j*cs:.1f}" y="{y0+i*cs:.1f}" width="{cs+.2:.1f}" height="{cs+.2:.1f}" fill="{C["amber"]}" fill-opacity="{v:.2f}"/>'
    return out


def diffusion():
    h = 170
    b = ""
    levels = [0, .3, .55, .8, 1.0]
    for k, nz in enumerate(levels):
        x = 14 + k*90
        b += _noisy_panel(x, 36, 70, nz, k + 3)
        b += t(x + 35, 122, ["clean", "a little noise", "more", "mostly noise", "pure noise"][k], 9, fill="muted")
    b += arrow(40, 18, 430, 18, "ink")
    b += t(W/2, 13, "training: add noise step by step", 9.5, weight=600)
    b += arrow(430, 146, 40, 146, "amber")
    b += t(W/2, 162, "generating: remove a little noise at each step", 9.5, weight=600, fill="amber")
    return svg(h, b)


# ------------------------------------------------------------------ chapter 8
def embed_map():
    h = 230
    b = rect(4, 4, W - 8, h - 8, "grey", None, 8)
    groups = [("animals", "sea", [("cat", 70, 60), ("kitten", 100, 44), ("dog", 60, 98), ("puppy", 104, 86), ("whale", 130, 118)]),
              ("vehicles", "amber", [("car", 360, 52), ("truck", 398, 72), ("bus", 352, 90), ("ship", 392, 112)]),
              ("numbers", "violet", [("one", 70, 178), ("two", 104, 196), ("three", 140, 176)])]
    for name, col, pts in groups:
        for wd, x, y in pts:
            b += circ(x, y, 3.5, col, None) + t(x + 6, y + 4, wd, 10, "start")
        cx = sum(p[1] for p in pts)/len(pts); cy = min(p[2] for p in pts) - 16
        b += t(cx + 10, cy, name, 8.5, fill=col, weight=600)
    roy = {"man": (230, 190), "woman": (300, 166), "king": (226, 120), "queen": (296, 96)}
    for wd, (x, y) in roy.items():
        b += circ(x, y, 3.5, "green", None) + t(x + 6, y + 4, wd, 10, "start")
    b += line(230, 190, 296, 167, "green", 1.4, 'stroke-dasharray="4 3" marker-end="url(#ar)"')
    b += line(226, 120, 292, 97, "green", 1.4, 'stroke-dasharray="4 3" marker-end="url(#ar)"')
    b += t(330, 148, "same direction:", 8.5, "start", "green")
    b += t(330, 160, "“male → female”", 8.5, "start", "green")
    return svg(h, b)


def context():
    h = 120
    b = ""
    n = 22
    bw = 19
    x0 = 12
    win = 7
    for i in range(n):
        x = x0 + i*bw
        inside = i >= win
        fill = "sea_soft" if inside else "grey"
        op = "" if inside else 'opacity=".55"'
        b += rect(x, 46, bw - 3, 22, fill, "muted" if not inside else "sea", 3, .8, op)
    nx = x0 + n*bw
    b += rect(nx, 46, bw - 3, 22, "amber_soft", "amber", 3, 1.2, 'stroke-dasharray="3 2"') + t(nx + 8, 61, "?", 11, weight=600, fill="amber")
    b += rect(x0 + win*bw - 4, 38, (n - win)*bw + 5, 38, "none", "sea", 6, 2, 'fill-opacity="0"')
    b += t(x0 + win*bw + (n - win)*bw/2, 28, "context window: everything the model can see", 9.5, weight=600, fill="sea")
    b += t(x0 + win*bw/2, 96, "fell out of the window", 9, fill="muted")
    b += t(x0 + win*bw/2, 108, "(the model can't see it)", 9, fill="muted")
    b += t(nx + 8, 96, "next", 9, fill="amber") + t(nx + 8, 108, "token", 9, fill="amber")
    return svg(h, b)


# ------------------------------------------------------------------ chapter 9
def attention_arcs():
    words = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "too", "tired"]
    wts = {"The": .05, "animal": .62, "didn't": .03, "cross": .04, "the": .02, "street": .12, "because": .04, "it": .08}
    h = 150
    # positions
    sizes = [len(w) for w in words]
    total = sum(sizes) * 6.6 + (len(words) - 1) * 9
    x = (W - total) / 2
    xs = []
    for w_ in words:
        wpx = len(w_) * 6.6
        xs.append(x + wpx/2)
        x += wpx + 9
    b = ""
    it = xs[7]
    for i, w_ in enumerate(words[:8]):
        if i == 7: continue
        wv = wts[w_]
        x1 = xs[i]
        mid = (x1 + it) / 2
        hh = 20 + abs(it - x1) * .38
        b += f'<path d="M{it:.1f} 108 Q{mid:.1f} {108 - hh*1.6:.1f} {x1:.1f} 108" fill="none" stroke="{C["sea"]}" stroke-width="{.6 + wv*9:.2f}" opacity="{.25 + wv:.2f}"/>'
    for i, (w_, xx) in enumerate(zip(words, xs)):
        col = "amber" if i == 7 else ("sea" if i == 1 else "ink")
        b += t(xx, 126, w_, 11, fill=col, weight=600 if i in (1, 7) else 400)
    b += t(xs[1], 144, "62%", 9, fill="sea", weight=600) + t(xs[5], 144, "12%", 9, fill="muted")
    return svg(h, b)


def qkv():
    h = 210
    toks = ["The", "animal", "street", "it"]
    scores = [0.4, 3.1, 1.5, 1.0]
    ex = [math.exp(s) for s in scores]
    sh = [e/sum(ex) for e in ex]
    b = ""
    b += t(52, 16, "Token", 9.5, weight=600) + t(130, 16, "Key", 9.5, weight=600)
    b += t(215, 16, "Score", 9.5, weight=600) + t(300, 16, "Share", 9.5, weight=600) + t(400, 16, "Value", 9.5, weight=600)
    rng = random.Random(4)
    for i, (tk, s, p) in enumerate(zip(toks, scores, sh)):
        y = 30 + i*34
        b += t(52, y + 15, tk, 10.5, weight=600 if tk == "animal" else 400)
        for j in range(4):
            b += rect(110 + j*10, y + 4, 9, 14, "sea", None, 1, extra=f'opacity="{rng.uniform(.25,.95):.2f}"')
            b += rect(380 + j*10, y + 4, 9, 14, "violet", None, 1, extra=f'opacity="{rng.uniform(.25,.95):.2f}"')
        b += t(215, y + 15, f"{s:.1f}", 10, extra=MONO)
        b += rect(268, y + 4, p*90, 14, "amber", None, 2)
        b += t(268 + p*90 + 4, y + 15, f"{p*100:.0f}%", 9, "start")
    b += rect(100, 172, 58, 24, "amber_soft", "amber", 4)
    for j in range(4):
        b += rect(106 + j*12, 177, 10, 14, "amber", None, 1, extra=f'opacity="{.4+.15*j:.2f}"')
    b += t(94, 189, "Query of “it”", 9.5, "end", weight=600)
    b += t(240, 189, "compared with each key", 9, fill="muted")
    b += arrow(420, 168, 420, 176) if False else ""
    b += t(400, 189, "→ blend of values,", 9, fill="muted") + t(400, 201, "mostly “animal”", 9, fill="violet", weight=600)
    return svg(h, b)


def mask():
    words = ["The", "cat", "sat", "on", "the", "mat"]
    n = len(words)
    h = 214
    cs = 26
    x0, y0 = 150, 30
    b = ""
    rng = random.Random(8)
    for i in range(n):
        b += t(x0 - 8, y0 + i*cs + 17, words[i], 10, "end")
        b += t(x0 + i*cs + 13, y0 - 8, words[i], 9.5, extra=f'transform="rotate(-35 {x0 + i*cs + 13} {y0 - 8})"' if False else "")
        ws = [rng.random() + (1.2 if j == i else 0) for j in range(i + 1)]
        s = sum(ws)
        for j in range(n):
            if j <= i:
                op = .12 + .85 * ws[j] / s
                b += f'<rect x="{x0+j*cs}" y="{y0+i*cs}" width="{cs-2}" height="{cs-2}" rx="2" fill="{C["sea"]}" fill-opacity="{op:.2f}"/>'
            else:
                b += f'<rect x="{x0+j*cs}" y="{y0+i*cs}" width="{cs-2}" height="{cs-2}" rx="2" fill="{C["grey"]}"/>'
                b += line(x0 + j*cs + 5, y0 + i*cs + 5, x0 + j*cs + cs - 7, y0 + i*cs + cs - 7, "rule", 1)
    b += t(x0 + n*cs + 16, y0 + 40, "hidden:", 9.5, "start", "muted", 600)
    b += t(x0 + n*cs + 16, y0 + 53, "the future", 9.5, "start", "muted")
    b += t(x0 + n*cs/2, y0 + n*cs + 20, "each row: one token looking back at the ones before it", 9, "middle", "muted")
    return svg(h, b)


def block():
    h = 290
    b = ""
    sx = 120
    b += line(sx, 270, sx, 22, "ink", 3, 'marker-end="url(#ar)"')
    b += t(sx, 284, "token embeddings in", 9.5, fill="muted")
    b += t(sx, 14, "to the next block", 9.5, fill="muted")
    b += t(sx - 14, 150, "residual stream", 9.5, fill="muted", extra=f'transform="rotate(-90 {sx-14} 150)"')
    for k, (name, sub, y, fill, stroke) in enumerate([("Attention", "tokens share information", 178, "sea_soft", "sea"),
                                                    ("Feed-forward", "each token thinks alone", 72, "violet_soft", "violet")]):
        ln_y = y + 50
        b += line(sx, ln_y + 12, 190, ln_y + 12, "muted", 1.2)
        b += box_label(190, ln_y, 86, 24, "LayerNorm", None, "grey", "muted", 9)
        b += arrow(233, ln_y, 233, y + 40, "ink")
        b += box_label(190, y, 160, 38, name, sub, fill, stroke, 10.5)
        b += path([(350, y + 19), (372, y + 19), (372, y - 12), (sx + 12, y - 12)], "ink", 1.2, 'marker-end="url(#ar)"')
        b += circ(sx, y - 12, 10, "paper", "ink", 1.6) + t(sx, y - 7.5, "+", 13, weight=600)
    b += f'<path d="M402 40 Q414 40 414 52 L414 250 Q414 262 402 262" fill="none" stroke="{C["muted"]}" stroke-width="1.2"/>'
    b += t(436, 150, "× N", 12, weight=600) + t(436, 164, "blocks", 9, fill="muted")
    return svg(h, b)


# ------------------------------------------------------------------ chapter 10
def pipeline():
    h = 160
    stages = [("Pretraining", "guess next token", "trillions of tokens", "sea_soft", "sea"),
              ("SFT", "example chats", "curated examples", "violet_soft", "violet"),
              ("Preferences", "RLHF / DPO", "“A or B?”", "amber_soft", "amber"),
              ("RL reasoning", "checkable tasks", "maths, code", "green_soft", "green")]
    b = ""
    bw, gap = 98, 14
    for i, (n, s1, s2, f, st) in enumerate(stages):
        x = 6 + i*(bw + gap)
        b += rect(x, 20, bw, 70, f, st)
        b += t(x + bw/2, 42, n, 10.5, weight=600) + t(x + bw/2, 60, s1, 8.6, fill="muted") + t(x + bw/2, 74, s2, 8.6, fill="muted")
        if i < 3: b += arrow(x + bw + 1, 55, x + bw + gap - 1, 55)
    b += t(55, 12, "→ base model", 9, fill="sea", weight=600, anchor="start") if False else ""
    costs = [1.0, .05, .06, .15]
    b += t(6, 116, "share of compute (illustrative):", 9, "start", "muted")
    for i, c in enumerate(costs):
        x = 6 + i*(bw + gap)
        b += rect(x, 124, bw, 10, "grey", None, 2) + rect(x, 124, max(3, bw*c), 10, "ink", None, 2)
    b += t(6 + bw/2, 152, "→ base model", 9, fill="sea", weight=600)
    b += t(6 + 3*(bw + gap) + bw/2, 152, "→ chat model", 9, fill="green", weight=600)
    return svg(h, b)


def scaling():
    h = 200
    X = lambda e: 50 + (e - 18) / 7 * 380
    Y = lambda L: 170 - (L - 1.6) / 2.0 * 150
    b = line(50, 170, 440, 170, "rule") + line(50, 15, 50, 170, "rule")
    pts = []
    for e in np.linspace(18, 25, 100):
        L = 1.7 + 2.6 * (10 ** (-(e - 18) * 0.17))
        pts.append((X(e), Y(L)))
    b += path(pts, "sea", 2.6)
    for e in range(18, 26):
        L = 1.7 + 2.6 * (10 ** (-(e - 18) * 0.17))
        b += circ(X(e), Y(L), 3.5, "sea", None)
        b += t(X(e), 184, f"10<tspan baseline-shift='super' font-size='7'>{e}</tspan>", 9, fill="muted")
    b += t(245, 198, "training compute (FLOPs, log scale) →", 9, fill="muted")
    b += t(24, 92, "loss", 9, fill="muted", extra='transform="rotate(-90 24 92)"')
    b += t(436, 24, "schematic, not real data", 8.5, "end", "muted")
    return svg(h, b)


def lora():
    h = 170
    b = ""
    b += rect(20, 20, 120, 120, "grey", "muted", 4)
    b += t(80, 75, "W", 20, weight=600, fill="muted") + t(80, 95, "original weights", 9, fill="muted") + t(80, 108, "(frozen)", 9, fill="muted")
    b += t(160, 86, "+", 18, weight=600)
    b += rect(185, 20, 16, 120, "amber_soft", "amber", 3)
    b += t(193, 156, "A", 11, weight=600, fill="amber")
    b += t(215, 86, "×", 15, weight=600)
    b += rect(230, 72, 120, 16, "amber_soft", "amber", 3)
    b += t(290, 108, "B", 11, weight=600, fill="amber")
    b += t(290, 126, "two thin trainable tables", 9, fill="amber")
    b += t(370, 86, "=", 18, weight=600)
    b += t(415, 70, "small", 9.5, fill="muted") + t(415, 84, "correction", 9.5, fill="muted") + t(415, 98, "added to W", 9.5, fill="muted")
    return svg(h, b)


# ------------------------------------------------------------------ chapter 11
def genloop():
    h = 200
    b = ""
    b += box_label(20, 70, 120, 50, "Text so far", "“Call me Ish”", "grey", "muted", 10.5)
    b += box_label(180, 70, 100, 50, "Model", "one forward pass", "sea_soft", "sea", 10.5)
    b += arrow(140, 95, 178, 95)
    bx = 320
    probs = [("mael", .82), ("a", .07), ("ma", .05), ("…", .06)]
    b += t(bx + 60, 52, "probabilities", 9.5, weight=600)
    for i, (tk, p) in enumerate(probs):
        y = 62 + i*16
        b += t(bx + 26, y + 11, tk, 9.5, "end", extra=MONO)
        b += rect(bx + 32, y + 2, p*95, 11, "amber" if i == 0 else "rule", None, 2)
    b += arrow(280, 95, 318, 95)
    b += path([(bx + 60, 132), (bx + 60, 172), (80, 172), (80, 124)], "amber", 1.6, 'marker-end="url(#ara)"')
    b += t(240, 166, "pick “mael”, append it, and go round again", 9.5, fill="amber", weight=600)
    return svg(h, b)


def temperature():
    h = 160
    toks = ["sea", "ship", "whale", "boat", "sky"]
    logits = [2.2, 1.6, 1.4, .9, -.2]
    b = ""
    for k, T in enumerate([0.3, 1.0, 1.8]):
        x0 = 8 + k*152
        ex = [math.exp(l/T) for l in logits]
        ps = [e/sum(ex) for e in ex]
        b += rect(x0, 6, 144, 118, "grey", None, 5)
        for i, (tk, p) in enumerate(zip(toks, ps)):
            x = x0 + 12 + i*26
            hh = p * 90
            b += rect(x, 104 - hh, 20, hh, "amber" if i == 0 else "sea", None, 2)
            b += t(x + 10, 118, tk, 8, fill="muted")
            b += t(x + 10, 100 - hh, f"{p*100:.0f}", 8)
        b += t(x0 + 72, 142, f"T = {T}", 10.5, weight=600)
        b += t(x0 + 72, 156, ["focused", "normal", "adventurous"][k], 9, fill="muted")
    return svg(h, b)


# ------------------------------------------------------------------ chapter 12
def moe_block():
    h = 260
    b = ""
    b += box_label(180, 222, 100, 30, "token “whale”", None, "grey", "muted", 10)
    b += arrow(230, 220, 230, 200)
    b += box_label(170, 168, 120, 30, "Router", None, "amber_soft", "amber", 10.5)
    scores = [.04, .31, .06, .03, .08, .38, .05, .05]
    chosen = {1, 5}
    ex_w, gap = 46, 9
    x0 = (W - (8*ex_w + 7*gap)) / 2
    for i, s in enumerate(scores):
        x = x0 + i*(ex_w + gap)
        act = i in chosen
        b += line(230, 168, x + ex_w/2, 118, "amber" if act else "rule", 2 if act else 1)
        b += rect(x, 84, ex_w, 34, "violet_soft" if act else "grey", "violet" if act else "rule", 4, 1.6 if act else 1)
        b += t(x + ex_w/2, 98, f"Expert {i+1}", 8.5, weight=600 if act else 400, fill="ink" if act else "muted")
        b += t(x + ex_w/2, 111, f"{s*100:.0f}%", 8.5, fill="amber" if act else "muted", weight=600 if act else 400)
        if act:
            b += line(x + ex_w/2, 84, 230, 50, "violet", 2)
    b += circ(230, 40, 11, "paper", "ink", 1.6) + t(230, 45, "+", 14, weight=600)
    b += arrow(230, 29, 230, 8)
    b += t(240, 18, "weighted sum of the 2 chosen experts", 9, "start", "muted")
    b += t(x0 + 8*(ex_w + gap) - gap, 140, "grey experts: idle for this token", 9, "end", "muted")
    return svg(h, b)


def dense_vs_moe():
    h = 190
    b = ""
    for k, (name, sub) in enumerate([("Dense", "all 64 blocks of weights used for every token"),
                                     ("Mixture of Experts", "same total size, only 16 blocks used per token")]):
        x0 = 20 + k*230
        rng = random.Random(11)
        act = set(range(64)) if k == 0 else set(rng.sample(range(8, 64), 12)) | {0, 1, 2, 3}
        for i in range(64):
            r, c = divmod(i, 8)
            on = i in act
            b += rect(x0 + c*22, 24 + r*16, 20, 14, ("sea" if k == 0 else "violet") if on else "grey", None, 2)
        b += t(x0 + 88, 14, name, 10.5, weight=600)
        b += t(x0 + 88, 172, sub, 8.5, fill="muted")
    return svg(h, b)


def routing():
    toks = ["Call", " me", " Ish", "mael", ".", " Some", " years", " ago"]
    picks = [(1, 4), (2, 4), (0, 5), (0, 5), (3, 2), (1, 2), (1, 3), (1, 3)]
    h = 170
    b = ""
    cw, rh = 46, 20
    x0, y0 = 72, 30
    for j, tk in enumerate(toks):
        b += t(x0 + j*cw + cw/2, y0 - 10, tk.strip() or "·", 9.5, extra=MONO)
    for i in range(6):
        b += t(x0 - 10, y0 + i*rh + 14, f"Expert {i+1}", 9, "end", "muted")
        for j in range(len(toks)):
            on = i in picks[j]
            b += rect(x0 + j*cw + 4, y0 + i*rh + 2, cw - 8, rh - 4, "violet" if on else "grey", None, 3)
    return svg(h, b)


# ------------------------------------------------------------------ chapter 13
def patches():
    h = 180
    b = ""
    x0, y0, s = 20, 18, 128
    scene = (f'<rect x="0" y="0" width="128" height="128" fill="{C["sea_soft"]}"/>'
             f'<path d="M0 128 L40 60 L70 92 L98 50 L128 80 L128 128 Z" fill="{C["green"]}" opacity=".75"/>'
             f'<circle cx="98" cy="26" r="13" fill="{C["amber"]}"/>')
    b += f'<g transform="translate({x0},{y0})">{scene}</g>'
    for k in range(1, 4):
        b += line(x0 + k*s/4, y0, x0 + k*s/4, y0 + s, "#ffffff", 2) + line(x0, y0 + k*s/4, x0 + s, y0 + k*s/4, "#ffffff", 2)
    b += t(x0 + s/2, y0 + s + 18, "image cut into 16 patches", 9, fill="muted")
    b += arrow(160, 82, 190, 82)
    ps = 23
    for i in range(16):
        r, c = divmod(i, 4)
        row, col = divmod(i, 8)
        px, py = 200 + col*(ps + 4), 50 + row*(ps + 10)
        b += f'<clipPath id="pc{i}"><rect x="{px}" y="{py}" width="{ps}" height="{ps}"/></clipPath>'
        k = ps / 32
        b += f'<g clip-path="url(#pc{i})"><g transform="translate({px},{py}) scale({k:.4f}) translate({-c*32},{-r*32})">{scene}</g></g>'
        b += rect(px, py, ps, ps, "none", "muted", 1, .7, 'fill-opacity="0"')
    b += t(320, 132, "a sequence of 16 visual tokens,", 9, fill="muted")
    b += t(320, 145, "read by a transformer like words", 9, fill="muted")
    return svg(h, b)

def rag():
    h = 180
    b = ""
    b += box_label(6, 20, 92, 40, "Question", "“refund policy?”", "grey", "muted", 10)
    b += box_label(128, 20, 96, 40, "Search", "by meaning", "sea_soft", "sea", 10)
    b += box_label(254, 20, 96, 40, "Documents", "vector database", "grey", "muted", 10)
    b += arrow(98, 40, 126, 40) + arrow(224, 40, 252, 40)
    b += box_label(128, 112, 140, 50, "Prompt", "question + best passages", "amber_soft", "amber", 10)
    b += path([(302, 60), (302, 86), (198, 86), (198, 110)], "ink", 1.3, 'marker-end="url(#ar)"')
    b += t(300, 80, "top 3 passages", 8.5, "start", "muted") if False else t(250, 80, "top matching passages", 8.5, "middle", "muted")
    b += path([(52, 60), (52, 137), (126, 137)], "ink", 1.3, 'marker-end="url(#ar)"')
    b += box_label(298, 112, 66, 50, "LLM", None, "sea_soft", "sea", 11)
    b += arrow(268, 137, 296, 137)
    b += box_label(392, 112, 62, 50, "Answer", "with sources", "green_soft", "green", 10)
    b += arrow(364, 137, 390, 137)
    return svg(h, b)


def agent_loop():
    h = 200
    b = ""
    b += box_label(10, 80, 76, 40, "Goal", "from the user", "grey", "muted", 10)
    b += arrow(86, 100, 128, 100)
    b += box_label(130, 76, 104, 48, "Model", "decides next step", "sea_soft", "sea", 10.5)
    b += box_label(300, 14, 120, 44, "Tool acts", "search, run code, click", "amber_soft", "amber", 10)
    b += box_label(300, 142, 120, 44, "Result", "added to context", "violet_soft", "violet", 10)
    b += path([(234, 90), (270, 36), (298, 36)], "ink", 1.4, 'marker-end="url(#ar)"')
    b += path([(420, 58), (440, 100), (420, 140)], "ink", 1.4, 'marker-end="url(#ar)"')
    b += path([(298, 164), (270, 164), (234, 112)], "ink", 1.4, 'marker-end="url(#ar)"')
    b += t(182, 152, "repeat until done", 9, fill="muted") + t(182, 168, "→ report back", 9, fill="green", weight=600)
    return svg(h, b)


# ------------------------------------------------------------------ chapter 14
def cpu_gpu():
    h = 200
    b = ""
    b += rect(10, 24, 170, 150, "grey", "muted", 8)
    b += t(95, 16, "CPU: a few big cores", 10.5, weight=600)
    for i in range(8):
        r, c = divmod(i, 4)
        b += rect(20 + c*39, 34 + r*42, 34, 36, "sea_soft", "sea", 4)
        b += t(37 + c*39, 56 + r*42, "core", 8.5, fill="sea")
    b += rect(20, 124, 151, 40, "amber_soft", "amber", 4) + t(95, 148, "large cache + control", 9, fill="amber")
    b += rect(200, 24, 250, 150, "grey", "muted", 8)
    b += t(325, 16, "GPU: thousands of small cores", 10.5, weight=600)
    for gi in range(4):
        for gj in range(3):
            gx, gy = 208 + gi*60, 32 + gj*46
            b += rect(gx, gy, 56, 42, "paper", "rule", 3)
            for i in range(6):
                for j in range(4):
                    b += f'<rect x="{gx+3+i*8.6:.1f}" y="{gy+3+j*7.4:.1f}" width="7" height="6" fill="{C["violet"]}" opacity=".75"/>'
            b += rect(gx + 3, gy + 33, 50, 6, "amber", None, 1)
    b += t(325, 190, "purple: simple cores · orange: tensor cores", 8.5, fill="muted")
    return svg(h, b)


def gpu_card():
    h = 250
    b = ""
    bx0, bx1 = 22, 318
    b += rect(6, 30, 16, 150, "#b9c3ca", "muted", 2)
    for i in range(3):
        b += rect(10, 50 + i*36, 8, 22, "#7f8c95", None, 1)
    b += rect(bx0, 40, bx1 - bx0, 130, "#28414f", None, 6)
    b += rect(92, 170, 170, 12, "#28414f", None, 0)
    for i in range(34):
        b += rect(94 + i*4.9, 172, 3.4, 9, "#d9a441", None, .5)
    cx, cy = 140, 105
    b += rect(cx - 36, cy - 36, 72, 72, "#9aa7b0", None, 4)
    b += rect(cx - 23, cy - 23, 46, 46, "#1d2b34", None, 3)
    b += t(cx, cy + 4, "GPU", 10, fill="#ffffff", weight=600)
    for x, y in [(cx - 60, 50), (cx - 14, 47), (cx + 34, 50), (cx + 44, 96), (cx + 34, 145), (cx - 14, 148), (cx - 60, 145), (cx - 70, 96)]:
        b += rect(x, y, 26, 15, "#11191f", None, 2)
    for i in range(6):
        b += rect(230 + (i % 3)*24, 70 + (i // 3)*26, 18, 18, "#5d6d78", None, 2)
    b += rect(268, 40, 36, 14, "#11191f", None, 2)
    for i in range(4):
        b += rect(271 + i*8, 43, 6, 8, "#ffd27d", None, 1)
    def lab(px, py, ty, title, sub=None):
        o = line(px, py, 330, ty, "ink", .8) + circ(px, py, 2.4, "amber", None)
        o += t(334, ty + 4, title, 9.5, "start", weight=600)
        if sub: o += t(334, ty + 16, sub, 8.5, "start", "muted")
        return o
    b += lab(296, 47, 40, "power connector")
    b += lab(278, 92, 82, "power delivery (VRM)")
    b += lab(cx + 70, 103, 122, "VRAM chips", "8 GB of GDDR6")
    b += lab(cx + 18, cy - 18, 160, "GPU chip", "cores, tensor cores, cache")
    b += line(177, 182, 177, 204, "ink", .8) + circ(177, 182, 2.4, "amber", None) + t(150, 216, "PCIe connector to the motherboard", 9.5, "start", weight=600)
    b += line(14, 165, 22, 204, "ink", .8) + circ(14, 165, 2.4, "amber", None) + t(8, 216, "display outputs", 9.5, "start", weight=600)
    b += t(W/2, 240, "448 GB/s between GPU and VRAM · about 16 GB/s across PCIe", 8.5, fill="muted")
    return svg(h, b)

def memory_pyramid():
    h = 230
    layers = [("Registers", "bytes · instant", "violet"), ("On-chip cache (SRAM)", "MBs · fastest memory", "violet"),
              ("VRAM (GDDR / HBM)", "8–200 GB · 0.4–8 TB/s", "sea"), ("System RAM", "16–512 GB · ~50–100 GB/s", "amber"),
              ("SSD storage", "TBs · ~3–7 GB/s", "muted")]
    b = ""
    top, bot = 14, 214
    lh = (bot - top) / len(layers)
    cx = 150
    for i, (n, d, col) in enumerate(layers):
        y1, y2 = top + i*lh, top + (i + 1)*lh
        w1, w2 = 20 + i*52, 20 + (i + 1)*52
        b += f'<path d="M{cx-w1/2} {y1} L{cx+w1/2} {y1} L{cx+w2/2} {y2-3} L{cx-w2/2} {y2-3} Z" fill="{C[col]}" fill-opacity="{.85 - i*.12:.2f}"/>'
        b += t(cx + w2/2 + 14, (y1 + y2)/2, n, 10, "start", weight=600)
        b += t(cx + w2/2 + 14, (y1 + y2)/2 + 13, d, 8.5, "start", "muted")
    b += t(14, 30, "smaller,", 9, "start", "muted") + t(14, 42, "faster", 9, "start", "muted")
    b += t(14, 196, "bigger,", 9, "start", "muted") + t(14, 208, "slower", 9, "start", "muted")
    b += line(30, 50, 30, 184, "muted", 1, 'marker-start="url(#ar)" marker-end="url(#ar)"')
    return svg(h, b)


def datacenter():
    h = 180
    b = ""
    # chip
    b += rect(20, 60, 50, 50, "#9aa7b0", None, 4) + rect(30, 70, 30, 30, "#1d2b34", None, 3)
    b += t(45, 136, "1 GPU", 10, weight=600)
    b += arrow(78, 85, 100, 85)
    # server
    b += rect(106, 50, 96, 70, "grey", "muted", 4)
    for i in range(8):
        r, c = divmod(i, 4)
        b += rect(114 + c*21, 58 + r*30, 17, 24, "#1d2b34", None, 2)
    b += t(154, 136, "server: 8 GPUs", 10, weight=600) + t(154, 149, "linked by NVLink", 8.5, fill="muted")
    b += arrow(208, 85, 230, 85)
    # rack
    b += rect(236, 22, 50, 126, "#28414f", None, 3)
    for i in range(8):
        b += rect(240, 27 + i*15, 42, 11, "#5d6d78", None, 1) + circ(276, 32.5 + i*15, 1.6, "green", None)
    b += t(261, 164, "rack", 10, weight=600)
    b += arrow(292, 85, 314, 85)
    # cluster
    for r in range(3):
        for c in range(6):
            b += rect(322 + c*21, 30 + r*40, 16, 32, "#28414f", None, 2)
    b += line(322, 26, 444, 26, "sea", 1.2) + line(322, 152, 444, 152, "sea", 1.2)
    b += t(383, 168, "cluster: thousands of GPUs", 10, weight=600) + t(383, 180, "networked (e.g. InfiniBand)", 8.5, fill="muted") if False else t(383, 168, "cluster: tens of thousands", 10, weight=600)
    return svg(h, b)


def parallelism():
    h = 240
    b = ""
    rows = [("Data parallel", 16), ("Tensor parallel", 92), ("Pipeline parallel", 168)]
    cols = ["sea", "violet", "amber"]
    for name, y in rows:
        b += t(8, y + 30, name, 10, "start", weight=600)
    # data parallel: 3 GPUs each full model of 4 layers, different data
    for g in range(3):
        x = 140 + g*104
        b += rect(x, 10, 90, 62, "grey", "rule", 4) + t(x + 45, 22, f"GPU {g+1}", 8.5, fill="muted")
        for L in range(4):
            b += rect(x + 10, 27 + L*10, 70, 8, "sea", None, 2)
        b += t(x + 45, 84, f"data batch {g+1}", 8.5, fill="sea")
    # tensor parallel: each layer split in 3 slices across GPUs
    for g in range(3):
        x = 140 + g*104
        b += rect(x, 92, 90, 54, "grey", "rule", 4) + t(x + 45, 104, f"GPU {g+1}", 8.5, fill="muted")
        for L in range(4):
            b += rect(x + 10, 109 + L*9, 70, 7, "violet", None, 1)
        b += t(x + 45, 158, f"slice {g+1} of every layer", 8.5, fill="violet")
    # pipeline
    for g in range(3):
        x = 140 + g*104
        b += rect(x, 168, 90, 52, "grey", "rule", 4) + t(x + 45, 180, f"GPU {g+1}", 8.5, fill="muted")
        b += rect(x + 10, 186, 70, 9, "amber", None, 2) + rect(x + 10, 199, 70, 9, "amber", None, 2)
        b += t(x + 45, 232, f"layers {2*g+1}–{2*g+2}", 8.5, fill="amber")
        if g < 2: b += arrow(x + 90, 197, x + 103, 197)
    return svg(h, b)


# ------------------------------------------------------------------ chapter 15
def bits():
    fmts = [("FP32", 1, 8, 23), ("FP16", 1, 5, 10), ("BF16", 1, 8, 7), ("FP8", 1, 4, 3), ("INT8", 0, 0, 8), ("INT4", 0, 0, 4)]
    h = 196
    bw = 11
    x0 = 56
    b = ""
    for i, (n, s, e, m) in enumerate(fmts):
        y = 14 + i*27
        b += t(x0 - 8, y + 13, n, 10, "end", weight=600)
        x = x0
        segs = [("sign", s, "violet"), ("exponent", e, "sea"), ("mantissa" if s else "value", m, "amber")]
        for lab, nb, col in segs:
            for k in range(nb):
                b += rect(x, y, bw - 1.5, 18, col, None, 1.5, extra='opacity=".85"')
                x += bw
        b += t(x + 6, y + 13, f"{s+e+m} bits", 9, "start", "muted")
    b += rect(60, 180, 10, 10, "violet", None, 2) + t(74, 189, "sign", 9, "start")
    b += rect(120, 180, 10, 10, "sea", None, 2) + t(134, 189, "exponent (range)", 9, "start")
    b += rect(240, 180, 10, 10, "amber", None, 2) + t(254, 189, "mantissa / value (precision)", 9, "start")
    return svg(h, b)


def quant():
    h = 196
    rng = np.random.default_rng(5)
    ws = rng.normal(0, .45, 26)
    ws = np.clip(ws, -1, 1)
    levels = np.linspace(-1, 1, 8)
    X = lambda i: 40 + i * 15.5
    Y = lambda v: 92 - v * 70
    b = ""
    for L in levels:
        b += line(30, Y(L), 445, Y(L), "rule", 1, 'stroke-dasharray="3 3"')
    for i, w in enumerate(ws):
        q = levels[np.argmin(np.abs(levels - w))]
        b += line(X(i), Y(w), X(i), Y(q), "amber", 1.2)
        b += circ(X(i), Y(w), 3.4, "ink", None)
        b += rect(X(i) - 4, Y(q) - 1.6, 8, 3.2, "amber", None, 1)
    b += circ(36, 172, 3.4, "ink", None) + t(44, 176, "original weight", 9, "start")
    b += rect(140, 170, 8, 3.2, "amber", None, 1) + t(154, 176, "rounded to nearest allowed level", 9, "start", "amber")
    b += t(445, 188, "8 levels shown here; 4-bit has 16", 9, "end", "muted")
    return svg(h, b)


def vram_budget():
    rows = [("7B · 4-bit", 3.9, .5, 1.0), ("8B · 4-bit", 4.6, .5, 1.0), ("3B · 16-bit", 6.0, .4, 1.0),
            ("13B · 4-bit", 7.3, .4, .8), ("7B · 8-bit", 7.4, .5, 1.0), ("7B · 16-bit", 14.0, .5, 1.0)]
    h = 210
    X = lambda gb: 100 + gb * 21
    b = ""
    for i, (n, wgt, kv, ov) in enumerate(rows):
        y = 16 + i*26
        b += t(92, y + 13, n, 9.5, "end", weight=600)
        x = X(0)
        for val, col in [(wgt, "sea"), (kv, "violet"), (ov, "muted")]:
            wpx = min(val*21, 455 - x)
            if wpx > 0: b += rect(x, y, wpx, 17, col, None, 0, extra='opacity=".85"')
            x += val*21
        total = wgt + kv + ov
        fits = total <= 8
        if X(total) < 440: b += t(X(total) + 5, y + 13, f"{total:.1f} GB" + ("" if fits else " ✗"), 9, "start", "green" if fits else "amber", 600)
        else: b += t(452, y + 13, f"{total:.1f} GB ✗", 9, "end", "paper", 600)
    b += line(X(8), 8, X(8), 176, "amber", 2, 'stroke-dasharray="5 3"')
    b += t(X(8), 190, "8 GB (RTX 2060 Super)", 9, fill="amber", weight=600)
    b += rect(100, 196, 10, 9, "sea", None) + t(114, 204, "weights", 8.5, "start")
    b += rect(170, 196, 10, 9, "violet", None) + t(184, 204, "KV cache", 8.5, "start")
    b += rect(245, 196, 10, 9, "muted", None) + t(259, 204, "overhead", 8.5, "start")
    return svg(h, b)


# ------------------------------------------------------------------ chapter 16
def stack():
    layers = [("Apps", "LM Studio · Ollama · chat apps · your own code", "green_soft", "green"),
              ("Models & inference engines", "Hugging Face Transformers · llama.cpp · vLLM", "amber_soft", "amber"),
              ("Frameworks", "PyTorch · JAX · TensorFlow", "violet_soft", "violet"),
              ("GPU platform & libraries", "CUDA (cuBLAS, cuDNN) · ROCm · Metal", "sea_soft", "sea"),
              ("Driver & operating system", "talks to the hardware", "grey", "muted"),
              ("Hardware", "GPU · CPU · memory", "grey", "ink")]
    h = 6*32 + 10
    b = ""
    for i, (n, d, f, s) in enumerate(layers):
        y = 6 + i*32
        inset = (5 - i) * 0
        b += rect(10 + inset, y, W - 20 - 2*inset, 28, f, s, 5)
        b += t(24, y + 18, n, 10.5, "start", weight=600)
        b += t(W - 22, y + 18, d, 9, "end", "muted")
    return svg(h, b)


def model_files():
    h = 180
    b = ""
    files = [("config.json", ["layers: 12", "heads: 12", "d_model: 768", "vocab: 50,257", "context: 1,024"], "sea"),
             ("tokenizer.json", ["vocabulary", "merge rules", "special tokens", "“ the” → 262", "“ whale” → 23756"], "violet"),
             ("model.safetensors", None, "amber")]
    for i, (n, lines_, col) in enumerate(files):
        x = 10 + i*150
        b += f'<path d="M{x} 20 L{x+118} 20 L{x+136} 38 L{x+136} 150 L{x} 150 Z" fill="#fff" stroke="{C[col]}" stroke-width="1.6"/>'
        b += f'<path d="M{x+118} 20 L{x+118} 38 L{x+136} 38" fill="none" stroke="{C[col]}" stroke-width="1.2"/>'
        b += t(x + 68, 172, n, 9.5, weight=600, fill=col, extra=MONO)
        if lines_:
            for k, ln in enumerate(lines_):
                b += t(x + 12, 52 + k*19, ln, 9, "start", extra=MONO)
        else:
            rng = random.Random(2)
            for r in range(7):
                vals = " ".join(f"{rng.uniform(-1, 1):+.2f}" for _ in range(3))
                b += t(x + 10, 50 + r*11, vals, 7.2, "start", "muted", extra=MONO)
            b += t(x + 68, 145, "124M numbers", 8.5, weight=600)
    return svg(h, b)


# ------------------------------------------------------------------ chapter 17
def perplexity():
    h = 200
    X = lambda L: 50 + L / 4.8 * 390
    Y = lambda p: 170 - p / 100 * 150
    b = line(50, 170, 445, 170, "rule") + line(50, 15, 50, 170, "rule")
    b += path([(X(L), Y(math.exp(L))) for L in np.linspace(0, 4.65, 120)], "sea", 2.6)
    for L in [0, 1, 2, 3, 4]:
        b += t(X(L), 184, str(L), 9, fill="muted")
    for p in [0, 25, 50, 75, 100]:
        b += t(44, Y(p) + 3, str(p), 9, "end", "muted")
    pts = [(4.56, "untrained: 96", "amber"), (2.2, "Tiny Writer, step ~500: 9", "violet"), (1.2, "a good letter model: ~3", "green")]
    offs = {4.56: (-8, -6, "end"), 2.2: (-6, -46, "end"), 1.2: (-4, -22, "end")}
    for L, lab, col in pts:
        p = math.exp(L)
        dx, dy, anc = offs[L]
        b += circ(X(L), Y(p), 4.5, col, None)
        if L < 3:
            b += line(X(L), Y(p) - 5, X(L) + dx + 2, Y(p) + dy + 4, col, .9)
        b += t(X(L) + dx, Y(p) + dy, lab, 9, anc, col, 600)
    b += t(247, 198, "loss →", 9, fill="muted")
    b += t(20, 92, "perplexity", 9, fill="muted", extra='transform="rotate(-90 20 92)"')
    return svg(h, b)


# ------------------------------------------------------------------ chapter 19
def decode():
    parts = [("Example", "the model's name", "muted"), ("30B", "30 billion total parameters", "sea"),
             ("A3B", "3 billion active per token, so it is a Mixture of Experts", "violet"),
             ("Instruct", "fine-tuned to follow instructions (not a base model)", "green"),
             ("32k", "context window of about 32,000 tokens", "amber"), ("Q4_K_M", "quantized to about 4 bits per weight", "sea"),
             (".gguf", "file format for llama.cpp, Ollama and LM Studio", "violet")]
    h = 250
    b = ""
    texts = ["Example", "-", "30B", "-", "A3B", "-", "Instruct", " · ", "32k", " · ", "Q4_K_M", ".gguf"]
    widths = [len(s_) * 8.6 for s_ in texts]
    x = (W - sum(widths)) / 2
    for s_, wpx in zip(texts, widths):
        if s_.strip("- ·"):
            col = [p[2] for p in parts if p[0] == s_][0]
            b += rect(x - 1, 12, wpx + 2, 24, col if col != "muted" else "grey", None, 3, extra='fill-opacity=".2"')
            b += t(x + wpx/2, 29, s_, 13, weight=600, fill=col if col != "muted" else "ink", extra=MONO)
        else:
            b += t(x + wpx/2, 29, s_, 13, fill="muted", extra=MONO)
        x += wpx
    for i, (key, meaning, col) in enumerate(parts):
        y = 58 + i*26
        wpx = len(key) * 7.6 + 12
        b += rect(110 - wpx, y, wpx, 19, col if col != "muted" else "grey", None, 3, extra='fill-opacity=".2"')
        b += t(110 - wpx/2, y + 14, key, 10.5, weight=600, fill=col if col != "muted" else "ink", extra=MONO)
        b += t(122, y + 14, meaning, 10, "start")
    return svg(h, b)
