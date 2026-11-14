# tiny-ai — a 100-parameter neural network

A neural network with exactly **100 trainable parameters**, written in pure Python
(no dependencies). Forward pass, backpropagation and the Adam optimizer are all hand-written.

| Layer | Shape | Weights | Biases | Total |
|---|---|---|---|---|
| Hidden 1 (tanh) | 2 → 13 | 26 | 13 | 39 |
| Hidden 2 (tanh) | 13 → 4 | 52 | 4 | 56 |
| Output (sigmoid) | 4 → 1 | 4 | 1 | 5 |
| | | | | **100** |

It learns to separate two interleaving half-moons (2D binary classification) and
reaches about 100% test accuracy in about 3 seconds.

```bash
python3 tiny_ai.py                              # train, test, draw ASCII decision map
python3 tiny_ai.py --save weights.json          # save the 100 learned numbers
python3 tiny_ai.py --load weights.json --predict 0.5 -0.2
```
