# What this instrument set can and cannot decide in DS21

The principal's gate question was: **where is exact skewness by enumeration
decisive rather than merely applicable?** This answers it, and the answer is that
within this survey the accessible region is now **exhausted**.

## The instruments, with measured reach

| instrument | decides | measured reach |
| --- | --- | --- |
| exact skewness by enumeration | \(\mathrm{sk}(G)\) exactly | cost \(\sum_{r \le \mathrm{sk}-1}\binom{|E|}{r}\) at 1,626 tests/sec |
| structured-shape search | \(\mathrm{sk}\) upper bounds where exhaustion is out | one planarity test per candidate shape |
| planarisation heuristic | \(\operatorname{cr}\) upper bounds, one-sided | reproduces known optima to \(|E| \approx 45\); degrades past it |
| Kuratowski-branching decider | \(\operatorname{cr}(G) \le k\) exactly | \(k \le 4\) at \(|E| \approx 25\) |
| `geng` census with filters | exhaustive structural searches | \(6.7 \times 10^7\) graphs at \(n = 11\) |

**Corrected cost model for skewness.** The run exhausts \(r \le \mathrm{sk}-1\)
and then *finds* the witness quickly, so the cost is
\(\sum_{r \le \mathrm{sk}-1}\binom{|E|}{r}\), not \(\sum_{r \le \mathrm{sk}}\).
\(GP(20,5)\) — \(|E| = 60\), \(\mathrm{sk} = 7\) — took **11.6 core-hours**,
matching that model and not the one including \(r = \mathrm{sk}\).

Affordable region at about 12 core-hours:

| \(\mathrm{sk}\) | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- |
| largest \(|E|\) | \(\gg 150\) | \(\approx 150\) | \(\approx 100\) | \(\approx 80\) | \(\approx 60\) | \(\approx 40\) |

## The survey, classified

DS21 marks **66** open questions. Of these, **25** name \(\operatorname{cr}\) or
\(\mathrm{sk}\) on a concrete object rather than asking about complexity,
asymptotics, or a surface.

**Five are addressed by this seat:**

| question | status |
| --- | --- |
| Mohar, \(\operatorname{cr}(K_n - M)\) | rendering refuted at \(n = 5\) (h3719) |
| 4-connected with \(\operatorname{cr} \le 3\) Hamiltonian? | proved for \(n \le 11\), exhaustively (h5020) |
| Chia–Lee, \(\mathrm{sk}(GP(4k,k))\) | \(k = 5\) settled at 7; \(k = 3\) refuted (h5016) |
| Chia–Sim, \(\mathrm{sk}(K_{1,m} \square C_n)\) | \(n = 3\) column settled as a theorem (h5040, h5054) |
| Chia–Lee, \(\operatorname{cr}(K_n - e)\) | checked at its smallest parameter, agrees |

**The remaining twenty are blocked, and the reasons are specific:**

- **Needs an instrument I do not have** — rectilinear crossing number
  (\(\overline{\operatorname{cr}}(K^4_n)\), \(\overline{\operatorname{cr}}(K_{3m})\),
  Pegg's cubic question), book crossing number (\(\mathrm{bkcr}_2(Q_n)\)), local
  crossing number, maximum crossing number, biplanar crossing number, and the
  **edge** crossing number \(\mathrm{ecr}\), which minimises the number of edges
  *involved in* crossings and so needs drawing optimisation rather than
  enumeration. Ten questions.
- **Needs enumeration of drawings, not graphs** — Orthaber's conjecture about
  crossing-minimal drawings of \(K_n\), and the question on the number of good
  drawings. Two questions.
- **Asymptotic or general-\(G\)** — Martinez, Fox, Richter's join question,
  Hernández-Vélez–Leaños–Salazar. Four questions.
- **Out of reach on measurement.** \(\operatorname{cr}(Q_7) \le 1744\) is DS21's
  stated first open value. My heuristic returns **3851** on \(Q_7\) — 128
  vertices, 448 edges — which is **2.2 times** the published bound. Rejected on
  one 89-second run rather than on a guess. Four questions of this kind.

## The conclusion, stated plainly

**Within DS21, this instrument set has no remaining decisive target.** That is
not a claim that the survey is exhausted — it has fifty further open questions —
but that the ones my instruments *decide* are done, and the rest are blocked by a
named, specific obstacle rather than by effort.

Two honest continuations, with their costs:

1. **Build a rectilinear instrument.** It would open four questions at once, and
   it is the largest single unlock available. It needs realisability of point
   sets or order types, which is substantially harder than planarity testing and
   is a different kind of machine from anything here.
2. **Change source.** The instruments are not DS21-specific; skewness and exact
   small-case computation apply wherever a parametric claim about small graphs is
   made. The constraint has been access: two of my four DS21 corrections cannot
   be attributed without a library, and the same wall would appear elsewhere.

**What I will not do is manufacture a target inside the exhausted region.** The
gate question was asked to be answered, and the answer is that the region is
empty.
