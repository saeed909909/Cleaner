#!/usr/bin/env python3
"""
tiny_ai.py - a neural network with exactly 100 trainable parameters.

Written from scratch in pure Python (no numpy, no PyTorch). It includes
the forward pass, hand-written backpropagation and the Adam optimizer.

Architecture (2 -> 13 -> 4 -> 1, tanh hidden layers, sigmoid output):
    layer 1: 2*13 weights + 13 biases = 39
    layer 2: 13*4 weights +  4 biases = 56
    layer 3:  4*1 weights +  1 bias   =  5
                                total = 100

Task: learn to separate two interleaving half-moons in 2D (binary classification).

Usage:
    python3 tiny_ai.py                 # train, report accuracy, draw decision map
    python3 tiny_ai.py --save w.json   # also save the 100 weights
    python3 tiny_ai.py --load w.json --predict 0.5 -0.2
"""
import argparse
import json
import math
import random

LAYERS = [2, 13, 4, 1]


# ---------------------------------------------------------------- model
class TinyNet:
    def __init__(self, sizes=LAYERS, seed=0):
        rng = random.Random(seed)
        self.sizes = sizes
        self.W, self.b = [], []
        for n_in, n_out in zip(sizes[:-1], sizes[1:]):
            scale = 1.0 / math.sqrt(n_in)  # Xavier-style init
            self.W.append([[rng.gauss(0, scale) for _ in range(n_in)] for _ in range(n_out)])
            self.b.append([0.0] * n_out)

    def num_params(self):
        return sum(len(r) for W in self.W for r in W) + sum(len(b) for b in self.b)

    # flat views for the optimizer / saving
    def params(self):
        out = []
        for W, b in zip(self.W, self.b):
            for row in W:
                out.extend(row)
            out.extend(b)
        return out

    def set_params(self, flat):
        i = 0
        for W, b in zip(self.W, self.b):
            for row in W:
                for j in range(len(row)):
                    row[j] = flat[i]; i += 1
            for j in range(len(b)):
                b[j] = flat[i]; i += 1

    def forward(self, x):
        """Returns output probability and cached activations for backprop."""
        acts = [x]
        a = x
        last = len(self.W) - 1
        for L, (W, b) in enumerate(zip(self.W, self.b)):
            z = [sum(w * ai for w, ai in zip(row, a)) + bj for row, bj in zip(W, b)]
            a = [1 / (1 + math.exp(-zi)) for zi in z] if L == last else [math.tanh(zi) for zi in z]
            acts.append(a)
        return a[0], acts

    def predict(self, x):
        return self.forward(x)[0]

    def backward(self, acts, y):
        """Binary cross-entropy gradient. Returns flat gradient (same order as params())."""
        gW = [None] * len(self.W)
        gb = [None] * len(self.b)
        # dLoss/dz for sigmoid + BCE simplifies to (p - y)
        delta = [acts[-1][0] - y]
        for L in reversed(range(len(self.W))):
            a_prev = acts[L]
            gW[L] = [[d * ap for ap in a_prev] for d in delta]
            gb[L] = list(delta)
            if L > 0:
                W = self.W[L]
                back = [sum(W[k][j] * delta[k] for k in range(len(delta))) for j in range(len(a_prev))]
                delta = [bj * (1 - ap * ap) for bj, ap in zip(back, a_prev)]  # tanh'
        flat = []
        for W, b in zip(gW, gb):
            for row in W:
                flat.extend(row)
            flat.extend(b)
        return flat


# ---------------------------------------------------------------- optimizer
class Adam:
    def __init__(self, n, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
        self.lr, self.b1, self.b2, self.eps = lr, b1, b2, eps
        self.m, self.v, self.t = [0.0] * n, [0.0] * n, 0

    def step(self, params, grads):
        self.t += 1
        out = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * g * g
            mh = self.m[i] / (1 - self.b1 ** self.t)
            vh = self.v[i] / (1 - self.b2 ** self.t)
            out.append(p - self.lr * mh / (math.sqrt(vh) + self.eps))
        return out


# ---------------------------------------------------------------- data
def make_moons(n=300, noise=0.12, seed=1):
    rng = random.Random(seed)
    data = []
    for i in range(n):
        t = math.pi * rng.random()
        if i % 2 == 0:
            x, y, label = math.cos(t), math.sin(t), 0
        else:
            x, y, label = 1 - math.cos(t), 0.5 - math.sin(t), 1
        x += rng.gauss(0, noise); y += rng.gauss(0, noise)
        data.append(([x - 0.5, y - 0.25], label))  # roughly centre on origin
    return data


# ---------------------------------------------------------------- training
def bce(p, y):
    p = min(max(p, 1e-9), 1 - 1e-9)
    return -(y * math.log(p) + (1 - y) * math.log(1 - p))


def evaluate(net, data):
    loss = acc = 0
    for x, y in data:
        p = net.predict(x)
        loss += bce(p, y)
        acc += (p > 0.5) == bool(y)
    return loss / len(data), acc / len(data)


def train(net, train_data, epochs=300, batch=16, lr=0.02, seed=2, verbose=True):
    rng = random.Random(seed)
    opt = Adam(net.num_params(), lr=lr)
    data = list(train_data)
    for ep in range(1, epochs + 1):
        rng.shuffle(data)
        for s in range(0, len(data), batch):
            chunk = data[s:s + batch]
            grad = [0.0] * net.num_params()
            for x, y in chunk:
                _, acts = net.forward(x)
                for i, g in enumerate(net.backward(acts, y)):
                    grad[i] += g / len(chunk)
            net.set_params(opt.step(net.params(), grad))
        if verbose and (ep % 50 == 0 or ep == 1):
            loss, acc = evaluate(net, train_data)
            print(f"epoch {ep:4d}  loss {loss:.4f}  train acc {acc:6.1%}")


def draw(net, data, w=60, h=24):
    """ASCII decision map: '.'/':' = predicted class, 'o'/'x' = actual points."""
    xs = [p[0][0] for p in data]; ys = [p[0][1] for p in data]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    grid = [[":" if net.predict([x0 + (x1 - x0) * c / (w - 1), y1 - (y1 - y0) * r / (h - 1)]) > 0.5 else " "
             for c in range(w)] for r in range(h)]
    for (x, y), lab in data:
        c = round((x - x0) / (x1 - x0) * (w - 1)); r = round((y1 - y) / (y1 - y0) * (h - 1))
        grid[r][c] = "x" if lab else "o"
    print("+" + "-" * w + "+")
    for row in grid:
        print("|" + "".join(row) + "|")
    print("+" + "-" * w + "+   o = class 0, x = class 1, ':' = region predicted as class 1")


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description="A 100-parameter neural network from scratch.")
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--save", help="save trained weights to a JSON file")
    ap.add_argument("--load", help="load weights from a JSON file instead of training")
    ap.add_argument("--predict", nargs=2, type=float, metavar=("X", "Y"), help="classify one point")
    args = ap.parse_args()

    net = TinyNet()
    assert net.num_params() == 100, net.num_params()
    print(f"Model {' -> '.join(map(str, LAYERS))} | trainable parameters: {net.num_params()}")

    data = make_moons(400)
    train_data, test_data = data[:300], data[300:]

    if args.load:
        with open(args.load) as f:
            net.set_params(json.load(f))
        print(f"Loaded weights from {args.load}")
    else:
        train(net, train_data, epochs=args.epochs)
        if args.save:
            with open(args.save, "w") as f:
                json.dump(net.params(), f)
            print(f"Saved 100 weights to {args.save}")

    if args.predict:
        p = net.predict(args.predict)
        print(f"point {args.predict} -> class {int(p > 0.5)}  (p = {p:.3f})")
        return

    loss, acc = evaluate(net, test_data)
    print(f"\nTest set: loss {loss:.4f}  accuracy {acc:.1%}\n")
    draw(net, data)


if __name__ == "__main__":
    main()
