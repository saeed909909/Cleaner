"""Illustrations for Inside the Machine, generated as inline SVG.
Each public function returns an <svg> string. Colours come from CSS classes in style.css
(f-* fills, s-* strokes) so every drawing shares the book's palette."""
import math
import random
import numpy as np

W = 460  # all figures use a 460-unit wide viewBox (~4.6 in on the page)

C = {"ink": "#16212b", "muted": "#5d6b77", "rule": "#cfd8df", "sea": "#1d6a86", "amber": "#c06f22",
     "violet": "#6b46c9", "green": "#2e7d4f", "sea_soft": "#e3f0f5", "amber_soft": "#fbefe2",
     "violet_soft": "#efeafb", "green_soft": "#e5f3ea", "grey": "#eef2f5"}


def svg(h, body, w=W):
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg" role="img">'
            f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{C["ink"]}"/></marker>'
            f'<marker id="ara" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{C["amber"]}"/></marker>'
            f'<marker id="ars" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{C["sea"]}"/></marker></defs>{body}</svg>')


def t(x, y, s, size=11, anchor="middle", fill="ink", weight=400, extra=""):
    size = size * 1.12  # figures are scaled to ~73% on the page; keep labels readable
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{C.get(fill, fill)}" font-weight="{weight}" {extra}>{s}</text>'


def line(x1, y1, x2, y2, col="ink", w=1.2, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{C.get(col, col)}" stroke-width="{w}" {extra}/>'


def arrow(x1, y1, x2, y2, col="ink", w=1.4):
    m = {"ink": "ar", "amber": "ara", "sea": "ars"}[col]
    return line(x1, y1, x2, y2, col, w, f'marker-end="url(#{m})"')


def rect(x, y, w, h, fill="grey", stroke=None, r=6, sw=1.2, extra=""):
    s = f'stroke="{C.get(stroke, stroke)}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{C.get(fill, fill)}" {s} {extra}/>'


def circ(x, y, r, fill="paper", stroke="ink", sw=1.2, extra=""):
    f = "#ffffff" if fill == "paper" else C.get(fill, fill)
    s = f'stroke="{C.get(stroke, stroke)}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{f}" {s} {extra}/>'


def path(pts, col="sea", w=2, extra=""):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{C.get(col, col)}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def box_label(x, y, w, h, title, sub=None, fill="sea_soft", stroke="sea", size=11):
    out = rect(x, y, w, h, fill, stroke)
    if sub:
        out += t(x + w/2, y + h/2 - 2, title, size, weight=600) + t(x + w/2, y + h/2 + 12, sub, size - 2.5, fill="muted")
    else:
        out += t(x + w/2, y + h/2 + 4, title, size, weight=600)
    return out


# ------------------------------------------------------------------ cover
def cover_art():
    rnd = random.Random(7)
    Wc, Hc = 432, 648
    cols = [2, 4, 7, 10, 12, 10, 7]
    xs = np.linspace(46, 386, len(cols))
    layers = []
    for x, n in zip(xs, cols):
        ys = np.linspace(70, 370, n) if n > 1 else [220]
        span = 300 * (n / max(cols))
        ys = np.linspace(220 - span/2, 220 + span/2, n)
        layers.append([(x + rnd.uniform(-6, 6), y + rnd.uniform(-5, 5)) for y in ys])
    body = f'<rect width="{Wc}" height="{Hc}" fill="#0f1b24"/>'
    for gx in range(18, Wc, 24):
        for gy in range(18, Hc, 24):
            body += f'<circle cx="{gx}" cy="{gy}" r="0.8" fill="#24394a"/>'
    body += f'<circle cx="300" cy="230" r="190" fill="#14303f" opacity=".55"/>'
    for a, b in zip(layers, layers[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                if rnd.random() < .7:
                    col = rnd.choice(["#3fa7c9", "#3fa7c9", "#3fa7c9", "#e39a52", "#9b7bf0"])
                    op = rnd.uniform(.08, .42)
                    body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{rnd.uniform(.5,1.6):.2f}" opacity="{op:.2f}"/>'
    for li, L in enumerate(layers):
        for (x, y) in L:
            r = rnd.uniform(3.2, 5.5)
            fill = "#e8f3f7"
            if rnd.random() < .12: fill, r = "#9b7bf0", r + 2
            elif rnd.random() < .12: fill, r = "#e39a52", r + 1.5
            body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+5:.1f}" fill="{fill}" opacity=".12"/>'
            body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"/>'
    # tiny binary/number strip
    body += f'<text x="46" y="48" font-family="JetBrains Mono, monospace" font-size="8" fill="#3e5b6e" letter-spacing="2">w = [0.42, -1.07, 0.88, 0.13, -0.56, 2.31, 0.07 ...]</text>'
    return f'<svg class="art" viewBox="0 0 {Wc} {Hc}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


# ------------------------------------------------------------------ chapter 1
def nested_ai():
    h = 270
    rings = [("Artificial intelligence", "chess engines, expert systems, spam filters", 128, "grey"),
             ("Machine learning", "learns its rules from examples", 98, "sea_soft"),
             ("Deep learning", "many-layered neural networks", 68, "violet_soft"),
             ("LLMs", "chatbots", 36, "amber_soft")]
    body = ""
    cx, bottom = 230, 264
    for name, sub, r, fill in rings:
        cy = bottom - r
        body += f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.72:.1f}" ry="{r}" fill="{C[fill]}" stroke="{C['muted']}" stroke-width="1"/>'
    for name, sub, r, fill in rings:
        cy = bottom - r
        top = cy - r
        if r > 40:
            body += t(cx, top + 19, name, 11.5, weight=600) + t(cx, top + 32, sub, 8.5, fill="muted")
        else:
            body += t(cx, cy - 1, name, 11.5, weight=600) + t(cx, cy + 13, sub, 8.5, fill="muted")
    return svg(h, body)


# ------------------------------------------------------------------ chapter 2
def bio_neuron():
    h = 210
    b = ""
    # biological, left half
    b += t(110, 16, "Biological neuron", 11, weight=600)
    sx, sy = 70, 110
    rnd = random.Random(3)
    for ang in [150, 180, 205, 230, 125, 255]:
        a = math.radians(ang)
        x2, y2 = sx + 45*math.cos(a), sy - 45*math.sin(a)
        b += line(sx, sy, x2, y2, "sea", 2.2)
        for d in (-25, 25):
            a2 = math.radians(ang + d)
            b += line(x2, y2, x2 + 16*math.cos(a2), y2 - 16*math.sin(a2), "sea", 1.4)
    b += circ(sx, sy, 17, "sea_soft", "sea", 2)
    b += circ(sx, sy, 6, "sea", None)
    b += path([(sx + 17, sy), (120, sy + 4), (160, sy - 2), (178, sy)], "sea", 3)
    for dy in (-16, 0, 16):
        b += line(178, sy, 196, sy + dy, "sea", 1.6) + circ(198, sy + dy, 3.2, "sea", None)
    b += t(32, 178, "dendrites", 9, fill="muted") + t(70, 146, "cell body", 9, fill="muted")
    b += t(140, 128, "axon", 9, fill="muted") + t(198, 150, "synapses", 9, fill="muted")
    b += line(232, 30, 232, 195, "rule", 1, 'stroke-dasharray="3 3"')
    # artificial, right half
    b += t(350, 16, "Artificial neuron", 11, weight=600)
    ins = [(262, 60, "x₁", "w₁"), (262, 110, "x₂", "w₂"), (262, 160, "x₃", "w₃")]
    nx, ny = 360, 110
    for x, y, lab, wl in ins:
        b += line(x + 11, y, nx - 24, ny, "ink", 1.3)
        b += circ(x, y, 11, "grey", "muted") + t(x, y + 4, lab, 10)
        mx, my = (x + nx)/2 - 6, (y + ny)/2 - 5
        b += t(mx, my, wl, 9.5, fill="amber", weight=600)
    b += circ(nx, ny, 24, "sea_soft", "sea", 2) + t(nx, ny - 2, "Σ", 15, weight=600) + t(nx, ny + 12, "+ bias", 8, fill="muted")
    b += arrow(nx + 24, ny, 406, ny)
    b += t(424, ny + 4, "ƒ", 15, weight=600, fill="violet")
    b += t(424, ny + 22, "activation", 8, fill="muted")
    b += arrow(434, ny, 456, ny)
    b += t(262, 190, "inputs", 9, fill="muted") + t(312, 190, "weights", 9, fill="amber")
    b += t(360, 152, "add up", 9, fill="muted") + t(446, 96, "output", 8.5, fill="muted")
    return svg(h, b)


def _plot(x0, y0, w, h, f, xr, yr, title, col="sea"):
    b = rect(x0, y0, w, h, "grey", None, 4)
    X = lambda x: x0 + (x - xr[0]) / (xr[1] - xr[0]) * w
    Y = lambda y: y0 + h - (y - yr[0]) / (yr[1] - yr[0]) * h
    if yr[0] < 0 < yr[1]:
        b += line(x0, Y(0), x0 + w, Y(0), "rule", 1)
    b += line(X(0), y0, X(0), y0 + h, "rule", 1)
    pts = [(X(x), Y(min(max(f(x), yr[0]), yr[1]))) for x in np.linspace(xr[0], xr[1], 120)]
    b += path(pts, col, 2.4)
    b += t(x0 + w/2, y0 + h + 15, title, 10, weight=600)
    return b


def activations():
    sig = lambda x: 1/(1+math.exp(-x))
    gelu = lambda x: 0.5*x*(1+math.tanh(math.sqrt(2/math.pi)*(x+0.044715*x**3)))
    fs = [("Step", lambda x: 1.0 if x > 0 else 0.0, (-.3, 1.3)), ("Sigmoid", sig, (-.3, 1.3)),
          ("Tanh", math.tanh, (-1.3, 1.3)), ("ReLU", lambda x: max(0, x), (-.8, 3.2)), ("GELU", gelu, (-.8, 3.2))]
    b, w, gap = "", 80, 10
    for i, (name, f, yr) in enumerate(fs):
        b += _plot(8 + i*(w+gap), 8, w, 80, f, (-3, 3), yr, name, ["muted", "sea", "sea", "amber", "violet"][i])
    return svg(112, b)


# ------------------------------------------------------------------ chapter 3
def network(sizes, h=240, seed=1, labels=None, top=16, bottom_pad=36, rmax=8.5, highlight=None):
    rnd = random.Random(seed)
    xs = np.linspace(50, W - 50, len(sizes))
    pos = []
    for x, n in zip(xs, sizes):
        span = (h - top - bottom_pad) * min(1, (n - 1) / 12) if n > 1 else 0
        ys = np.linspace(top + (h - top - bottom_pad)/2 - span/2, top + (h - top - bottom_pad)/2 + span/2, n) if n > 1 else [top + (h - top - bottom_pad)/2]
        pos.append([(x, y) for y in ys])
    b = ""
    for A, B in zip(pos, pos[1:]):
        for (x1, y1) in A:
            for (x2, y2) in B:
                wv = rnd.gauss(0, 1)
                b += line(x1, y1, x2, y2, "sea" if wv > 0 else "amber", min(2.2, .4 + abs(wv)*.7), f'opacity="{min(.85, .2 + abs(wv)*.3):.2f}"')
    r = min(rmax, (h - top - bottom_pad) / max(sizes) / 2.4 + 2)
    for li, L in enumerate(pos):
        for (x, y) in L:
            fill = "grey" if li == 0 else ("amber_soft" if li == len(pos) - 1 else "sea_soft")
            b += circ(x, y, r, fill, "ink", 1.2)
    if labels:
        for x, lab in zip(xs, labels):
            b += t(x, h - 12, lab, 9.5, fill="muted")
    return svg(h, b)


def tiny_net():
    return network([2, 13, 4, 1], 240, 5, ["Input · 2", "Hidden · 13", "Hidden · 4", "Output · 1"])


def features():
    h = 150
    b = ""
    # panel 1: edges
    x0 = 10
    b += rect(x0, 10, 120, 100, "grey", None)
    rnd = random.Random(2)
    for i in range(4):
        for j in range(3):
            cx, cy = x0 + 18 + i*28, 28 + j*30
            a = rnd.choice([0, 45, 90, 135])
            dx, dy = 9*math.cos(math.radians(a)), 9*math.sin(math.radians(a))
            b += line(cx - dx, cy - dy, cx + dx, cy + dy, "ink", 2.2)
    b += t(x0 + 60, 128, "Early layers: edges", 9.5, weight=600)
    b += arrow(136, 60, 160, 60)
    # panel 2: parts
    x0 = 170
    b += rect(x0, 10, 120, 100, "grey", None)
    b += f'<ellipse cx="{x0+30}" cy="40" rx="15" ry="9" fill="none" stroke="{C["ink"]}" stroke-width="2"/>' + circ(x0 + 30, 40, 4, "ink", None)
    b += path([(x0 + 80, 28), (x0 + 74, 52), (x0 + 86, 54)], "ink", 2)
    b += path([(x0 + 22, 82), (x0 + 40, 92), (x0 + 58, 82)], "ink", 2)
    b += path([(x0 + 82, 74), (x0 + 96, 90), (x0 + 108, 72)], "ink", 2)
    b += t(x0 + 60, 128, "Middle: parts", 9.5, weight=600)
    b += arrow(296, 60, 320, 60)
    # panel 3: face
    x0 = 330
    b += rect(x0, 10, 120, 100, "grey", None)
    cx = x0 + 60
    b += circ(cx, 60, 40, "amber_soft", "ink", 2)
    b += f'<ellipse cx="{cx-15}" cy="48" rx="8" ry="5" fill="#fff" stroke="{C["ink"]}" stroke-width="1.6"/>' + circ(cx - 15, 48, 2.5, "ink", None)
    b += f'<ellipse cx="{cx+15}" cy="48" rx="8" ry="5" fill="#fff" stroke="{C["ink"]}" stroke-width="1.6"/>' + circ(cx + 15, 48, 2.5, "ink", None)
    b += path([(cx, 52), (cx - 5, 66), (cx + 3, 67)], "ink", 1.6)
    b += path([(cx - 14, 78), (cx, 85), (cx + 14, 78)], "ink", 1.8)
    b += t(cx, 128, "Late layers: objects", 9.5, weight=600)
    return svg(h, b)


def matrix():
    h = 150
    Wm = [[0.8, -0.2, 0.5, 0.1], [-0.4, 0.9, 0.0, 0.3], [0.2, 0.2, -0.7, 0.6]]
    x = [1.0, 0.5, -1.0, 2.0]
    out = [sum(a*b for a, b in zip(r, x)) for r in Wm]
    b = ""
    cw, ch = 40, 26
    x0, y0 = 40, 36
    b += t(x0 + 2*cw, 22, "Weights: 3 neurons × 4 inputs", 9.5, weight=600)
    for i, r in enumerate(Wm):
        b += t(x0 - 8, y0 + i*ch + 17, f"n{i+1}", 9, "end", "muted")
        for j, v in enumerate(r):
            b += rect(x0 + j*cw, y0 + i*ch, cw - 2, ch - 2, "amber_soft" if i == 0 else "grey", None, 3)
            b += t(x0 + j*cw + cw/2 - 1, y0 + i*ch + 16, f"{v:+.1f}", 10, extra='font-family="JetBrains Mono, monospace"')
    xv = x0 + 4*cw + 26
    b += t(xv - 13, y0 + 46, "×", 16, weight=600)
    b += t(xv + 18, 22, "Inputs", 9.5, weight=600)
    for j, v in enumerate(x):
        b += rect(xv, y0 + j*ch*0.78 - 8, 36, ch*0.78 - 2, "sea_soft", None, 3)
        b += t(xv + 18, y0 + j*ch*0.78 + 7, f"{v:+.1f}", 10, extra='font-family="JetBrains Mono, monospace"')
    ov = xv + 72
    b += t(ov - 16, y0 + 46, "=", 16, weight=600)
    b += t(ov + 22, 22, "Outputs", 9.5, weight=600)
    for i, v in enumerate(out):
        b += rect(ov, y0 + i*ch, 44, ch - 2, "violet_soft" if i else "amber_soft", None, 3)
        b += t(ov + 22, y0 + i*ch + 16, f"{v:+.2f}", 10, extra='font-family="JetBrains Mono, monospace"')
    calc = " + ".join(f"({a:+.1f}×{c:+.1f})" for a, c in zip(Wm[0], x))
    b += t(W/2, 135, f"n1 = {calc} = {out[0]:+.2f}", 9, fill="muted", extra='font-family="JetBrains Mono, monospace"')
    return svg(h, b)


def softmax():
    words = ["cat", "dog", "car", "sky"]
    logits = [3.0, 2.0, 0.5, -1.0]
    ex = [math.exp(v) for v in logits]
    pr = [e/sum(ex) for e in ex]
    h = 170
    b = t(110, 16, "Logits (raw scores)", 10.5, weight=600) + t(345, 16, "After softmax (probabilities)", 10.5, weight=600)
    base = 120
    for i, (wd, lg, p) in enumerate(zip(words, logits, pr)):
        x = 40 + i*44
        hh = lg * 28
        b += rect(x, base - max(hh, 0), 30, abs(hh), "sea" if lg >= 0 else "amber", None, 2)
        b += t(x + 15, (base - hh - 5) if lg >= 0 else (base - hh + 13), f"{lg:+.1f}", 9.5)
        b += t(x + 15, 160, wd, 10, fill="muted")
        x2 = 260 + i*48
        hh2 = p * 95
        b += rect(x2, base - hh2, 32, hh2, "violet", None, 2)
        b += t(x2 + 16, base - hh2 - 5, f"{p*100:.0f}%" if p > .02 else f"{p*100:.1f}%", 9.5)
        b += t(x2 + 16, 160, wd, 10, fill="muted")
    b += line(30, base, 216, base, "rule") + line(250, base, 450, base, "rule")
    b += arrow(222, 80, 248, 80)
    return svg(h, b)


# ------------------------------------------------------------------ chapter 4
def _loss(w):
    return 0.08*(w - 1.2)**2 + 0.6*math.exp(-((w + 1.6)**2)) * 0.6 + 0.05


def descent():
    h = 190
    X = lambda w: 30 + (w + 4) / 9 * 410
    Y = lambda L: 160 - L * 95
    pts = [(X(w), Y(_loss(w))) for w in np.linspace(-4, 5, 200)]
    b = path(pts, "ink", 2)
    b += line(30, 160, 445, 160, "rule")
    w = -3.6
    steps = []
    for _ in range(9):
        g = (_loss(w + 1e-4) - _loss(w - 1e-4)) / 2e-4
        steps.append(w)
        w -= 2.6 * g
    for i, s in enumerate(steps):
        x, y = X(s), Y(_loss(s))
        if i:
            px, py = X(steps[i-1]), Y(_loss(steps[i-1]))
            b += line(px, py - 7, x, y - 7, "amber", 1.4, 'stroke-dasharray="3 2"')
        b += circ(x, y - 7, 6 if i == 0 else 4.5, "amber", "paper" if False else None)
    b += t(X(steps[0]), Y(_loss(steps[0])) - 18, "start", 9, fill="amber", weight=600)
    b += t(X(1.2), 178, "lowest loss (best weights)", 9, fill="muted")
    b += line(X(1.2), 160, X(1.2), 166, "muted")
    b += t(22, 92, "loss", 9, "middle", "muted", extra='transform="rotate(-90 22 92)"')
    b += t(430, 152, "weight →", 9, "end", "muted")
    return svg(h, b)


def lr_compare():
    h = 150
    b = ""
    f = lambda w: 0.25 * w * w
    for k, (name, lr, n) in enumerate([("Too small", .25, 10), ("About right", 1.6, 6), ("Too large", 7.6, 6)]):
        x0 = 8 + k*152
        X = lambda w: x0 + 70 + w * 17
        Y = lambda L: 105 - L * 22
        b += rect(x0, 6, 144, 120, "grey", None, 5)
        b += path([(X(w), Y(f(w))) for w in np.linspace(-3.9, 3.9, 80)], "ink", 1.6)
        w = -3.6
        prev = None
        for i in range(n):
            x, y = X(w), Y(f(w))
            if abs(w) > 4.1: break
            if prev: b += line(prev[0], prev[1], x, y, "amber", 1.3)
            b += circ(x, y, 3.6, "amber", None)
            prev = (x, y)
            w -= lr * 0.5 * w
        b += t(x0 + 72, 142, name, 10, weight=600)
    return svg(h, b)


def backprop():
    h = 150
    names = ["Input", "Layer 1", "Layer 2", "Output", "Loss"]
    b = ""
    xs = [14 + i*90 for i in range(5)]
    for i, (x, n) in enumerate(zip(xs, names)):
        fill = "grey" if i == 0 else ("amber_soft" if i == 4 else "sea_soft")
        b += box_label(x, 55, 72, 38, n, None, fill, "amber" if i == 4 else "sea", 10.5)
    for i in range(4):
        b += arrow(xs[i] + 72, 64, xs[i+1] - 2, 64, "sea")
        b += arrow(xs[i+1], 86, xs[i] + 74, 86, "amber")
    b += t(W/2, 30, "Forward pass: data flows to an answer", 10, fill="sea", weight=600)
    b += t(W/2, 124, "Backward pass: blame (gradients) flows back to every weight", 10, fill="amber", weight=600)
    return svg(h, b)


# ------------------------------------------------------------------ chapter 5
def fit3():
    rng = np.random.default_rng(4)
    xs = np.linspace(-1, 1, 14)
    ys = np.sin(xs * 2.6) * 0.7 + rng.normal(0, .17, len(xs))
    b = ""
    h = 150
    for k, (name, deg) in enumerate([("Underfitting", 1), ("Good fit", 3), ("Overfitting", 13)]):
        x0 = 8 + k*152
        X = lambda x: x0 + 72 + x * 62
        Y = lambda y: 62 - y * 40
        b += rect(x0, 6, 144, 112, "grey", None, 5)
        cf = np.polyfit(xs, ys, deg)
        grid = np.linspace(-1.05, 1.05, 300)
        pts = [(X(x), Y(max(-1.35, min(1.35, np.polyval(cf, x))))) for x in grid]
        b += f'<clipPath id="cp{k}"><rect x="{x0}" y="6" width="144" height="112" rx="5"/></clipPath>'
        b += f'<g clip-path="url(#cp{k})">' + path(pts, ["amber", "sea", "violet"][k], 2.2) + "</g>"
        for x, y in zip(xs, ys):
            b += circ(X(x), Y(y), 3.2, "ink", None)
        b += t(x0 + 72, 136, name, 10, weight=600)
    return svg(h, b)


def overfit_curve():
    h = 180
    X = lambda e: 40 + e / 100 * 400
    Y = lambda L: 150 - L * 50
    tr = [(e, 2.4 * math.exp(-e/18) + .15 - e*0.0006) for e in range(0, 101)]
    va = [(e, 2.4 * math.exp(-e/18) + .35 + 0.00016*max(0, e - 30)**2) for e in range(0, 101)]
    b = line(40, 150, 440, 150, "rule") + line(40, 10, 40, 150, "rule")
    b += path([(X(e), Y(L)) for e, L in tr], "sea", 2.4)
    b += path([(X(e), Y(L)) for e, L in va], "amber", 2.4)
    best = min(va, key=lambda p: p[1])
    b += line(X(best[0]), Y(best[1]), X(best[0]), 150, "muted", 1, 'stroke-dasharray="3 3"')
    b += circ(X(best[0]), Y(best[1]), 5, "amber", None)
    b += t(X(best[0]) + 8, Y(best[1]) - 12, "best place to stop", 9.5, "start", "ink", 600)
    b += t(X(100), Y(va[-1][1]) - 8, "validation loss", 9.5, "end", "amber", 600)
    b += t(X(100), Y(tr[-1][1]) + 16, "training loss", 9.5, "end", "sea", 600)
    b += t(240, 172, "training time →", 9, fill="muted") + t(24, 80, "loss", 9, fill="muted", extra='transform="rotate(-90 24 80)"')
    b += t(X(78), 30, "memorising →", 9.5, "middle", "muted")
    return svg(h, b)


from figs2 import *  # noqa: E402,F401  (chapters 6-19)
