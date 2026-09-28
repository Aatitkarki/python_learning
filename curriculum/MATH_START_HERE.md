# Math bridge for a first-time learner

Work through this before Stage 02. Use paper alongside Python. You can spend several sessions here; the course schedule is an estimate, not a deadline. When a word is unfamiliar, stop and calculate a small example before moving on.

## Arithmetic and signs

A negative number lies below zero on the number line. `3 - 5 = -2`; subtracting a negative reverses direction: `3 - (-2) = 5`. Multiplying two negatives gives a positive: `(-2) * (-3) = 6`. Parentheses make the intended order clear.

Evaluate parentheses, powers, multiplication/division, then addition/subtraction. `2 + 3 * 4 = 14`, while `(2 + 3) * 4 = 20`. Python writes powers as `**`: `2 ** 3 = 8`. `-3 ** 2` evaluates to -9; `(-3) ** 2` is 9.

## Fractions, ratios, and percentages

A fraction `a/b` means a divided by b, and b must not be zero. Half a pizza is `1/2 = .5`; a quarter is `1/4 = .25`. To add, use a common denominator: `1/2 + 1/4 = 2/4 + 1/4 = 3/4`. To multiply: `(2/3)*(3/4)=6/12=1/2`.

A percentage is a fraction of 100: `25% = 25/100 = .25`. Twenty percent of 80 is `.2 * 80 = 16`. Growth from 80 to 100 is `(100-80)/80=.25=25%`. Falling from 100 to 80 is `(80-100)/100=-.2=-20%`: the denominators differ. A fraction and its percentage representation differ by a factor of 100.

## Variables, equations, and units

In `cost = price * quantity`, the names represent quantities. If price is 3 dollars/item and quantity is 4 items, cost is 12 dollars. Units help check a formula: dollars/item times items gives dollars. Adding 3 metres and 4 seconds has no meaningful total without another model.

Solve `2*x + 3 = 11` by doing the same operation to both sides. Subtract 3: `2*x=8`. Divide by 2: `x=4`. Substitute to verify. An equation expresses equality; Python assignment stores a computed result. To check the proposed answer, write `assert 2 * 4 + 3 == 11`.

## Averages, powers, roots, and notation

The mean of `[3,6,9]` is their sum divided by their count: `18/3=6`. Squaring multiplies a number by itself. The square root reverses squaring for nonnegative numbers: `sqrt(16)=4`. An exponent of -1 means reciprocal, so `2**-1=.5`. Scientific notation `1e-5` means `0.00001`, not “1 minus 5.”

| Notation | Say it aloud | Meaning |
|---|---|---|
| $x_i$ | x sub i | entry i in a collection; mathematical indexing often starts at 1, Python at 0 |
| $\sum_{i=1}^{n}x_i$ | sum x from i equals one to n | add every entry |
| $\hat y$ | y hat | predicted value |
| $\Delta x$ | delta x | change in x |
| $\alpha$, $\lambda$ | alpha, lambda | names for quantities; the lesson defines which |
| $\|v\|$ | norm of v | vector length under a specified rule |
| $\partial L/\partial w$ | partial derivative of L with respect to w | local change in loss as w changes |
| $P(A\mid B)$ | probability of A given B | probability after conditioning on B |

Read a formula once as words, substitute small numbers, calculate by hand, and only then translate it into Python. Do not attempt to memorize a page of unexplained symbols.

## Readiness check

Calculate without opening the answers: `4-7`; `4-(-2)`; `3/4` as a percentage; 10% of 60; solve `3*x-2=10`; mean of `[1,4,7]`; the square of -4; growth from 50 to 60.

<details><summary>Worked answers</summary>

- `4-7=-3` and `4-(-2)=6`.
- `3/4=.75=75%`; `.1*60=6`.
- Add 2 to both sides, then divide by 3: `x=4`.
- `(1+4+7)/3=4`.
- `(-4)*(-4)=16`.
- `(60-50)/50=.2=20%`.

</details>

Continue with [vectors and algebra](concepts/02a.md), [derivatives and learning](concepts/02b.md), then [probability and statistics](concepts/02c.md). These same explanations are embedded in the corresponding course notebooks.
