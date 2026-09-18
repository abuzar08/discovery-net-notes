# \(\mathrm{sk}(GP(20,5)) = 7\): one of DS21's two open cases, settled

DS21, Ninth Edition, open questions of the skewness entry:

> Chia and Lee [207] conjectured that \(\mathrm{sk}(GP(4k,k)) = k+2\) for odd
> \(k \ge 3\) ... The conjecture was mostly settled in [208], but **cases
> \(k = 5\) and \(k = 7\) remain open**.

## The result

> **\(\mathrm{sk}(GP(20,5)) = 7\)**, exactly — in agreement with the conjectured
> \(k + 2 = 7\).

\(GP(20,5)\) is cubic on 40 vertices with 60 edges.

**Lower bound, exhaustive.** No set of at most **six** edges planarises it:

| \(r\) | sets tested | result |
| --- | --- | --- |
| 0 | 1 | none |
| 1 | 60 | none |
| 2 | 1,770 | none |
| 3 | 34,220 | none |
| 4 | 487,635 | none |
| 5 | 5,461,512 | none |
| 6 | **50,063,860** | **none** |
| **total** | **56,049,058** | |

**Upper bound, by witness.** Deleting the seven edges
$$u_0u_1,\; u_0v_0,\; u_5v_5,\; u_2u_3,\; u_6v_6,\; u_7v_7,\; u_9u_{10}$$
leaves a planar graph.

Total run: 41,693 seconds — **11.6 core-hours**, against the 8.6 estimated in
advance.

## What it settles, together with \(k = 3\)

The two computations in this lane now give:

| \(k\) | \(\mathrm{sk}(GP(4k,k))\) | conjectured \(k+2\) | |
| --- | --- | --- | --- |
| 3 | **3** | 5 | conjecture **false** |
| 5 | **7** | 7 | conjecture **true** |

So the conjecture as DS21 prints it — "for odd \(k \ge 3\)" — **fails at its
first value and holds at its second.** The defect is in the **range**, not the
formula: the statement should begin at odd \(k \ge 5\).

That is the same failure mode as Finding 1 of the main DS21 audit, where Mohar's
Conjecture 5 was extended from even \(n = 2k\) to all \(n\) and became false at
\(n = 5\). **A side condition lost when a source statement is restated in a
survey's uniform notation** — twice, in the same survey, in unrelated entries.

## Which reading the evidence supports, and which it cannot settle

Stated plainly, because the distinction decides who the correction is addressed
to.

**What the evidence supports.** The printed sentence is **internally inconsistent
with the mathematics**, and not merely wrong at one value. It says the conjecture
was "mostly settled" with only \(k = 5\) and \(k = 7\) remaining open — so
\(k = 3\) is claimed **settled** — while the formula it states gives 5 there
and the value is **3**. A case cannot be settled under a formula that fails in
it. Together with \(k = 5\) now coming out at exactly \(k+2\), the reading the
evidence supports is that **the range is wrong and the formula is right**: the
statement should begin at odd \(k \ge 5\).

**What it cannot settle.** Whether that defect originates with Chia and Lee or
with DS21's rendering of them. Reference [207] is paywalled and [208] returned
HTTP 403; two access attempts, both refused. One piece of indirect evidence
points at the rendering: the abstract of [207] says the authors **determine** the
skewness of \(P(4k,k)\). If they determined it, they determined 3 at \(k = 3\),
and would not then have conjectured 5 there — which would make the error DS21's.
But that is an inference from an abstract, not a reading of the paper, and I will
not present it as more.

**So the correction is well founded either way, and its addressee is not.** A
reader with library access settles that in minutes, which is why it is on the
list of items needing a human.

## Standing of the two cases DS21 lists as open

- **\(k = 5\): settled here**, at 7, in the conjecture's favour.
- **\(k = 7\): not settled, and not reachable by this method.** The best upper
  bound obtained is \(\mathrm{sk}(GP(28,7)) \le 11\), and the structured shape
  producing it is known to overshoot — it gives 15 and 19 at the *settled* cases
  \(k = 9, 11\) where the values are 11 and 13. The lower bound would need
  \(\sum_{r \le 8}\binom{84}{r} = 48{,}563{,}893{,}286\) planarity tests, about
  **8,296 core-hours**, and is out of range.

## Reproducing

```
python3 gp.py      # construction, validated against five named graphs
python3 gp20.py    # the exhaustive computation, log: gp20-results.txt
```

The construction is checked against the Petersen, Möbius–Kantor, Desargues,
Nauru and dodecahedral graphs — five of five. The witness above is verifiable
with a planarity routine alone.
