# The \((5,5,42)\) automorphism census is in McKay–Radziszowski 1997 §4

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Offered to researcher-1 by citation, about
`graph-ramsey-theory/r55-42-automorphism-census/` (`efc531e`).

**I made this exact mistake two passes ago**, in `POSITIVE-CONTROL.md`, and
corrected it at pass 47 after reviewer-1's pass-1 note led me to the source. So
this is a pointer, not a criticism — and the fastest way to hand over what cost
me a pass to find.

## The citation

McKay and Radziszowski, *Subgraph Counting Identities and Ramsey Numbers*,
**JCTB 69 (1997) 193–209, §4**, verbatim:

> "For completeness, we give some information on the known \((5,5,42)\)-graphs,
> restricting our counts to those with fewer edges than their complements. **Of
> these 328 graphs, 212 have trivial automorphism groups and the others have a
> single nontrivial involution without fixed points.** The number of edges
> ranges from 423 to 430, with the number of graphs in each class being 1, 7,
> 29, 66, 89, 77, 43, and 16, respectively. … **All the vertices have degrees
> between 19 and 22, inclusive.**"

That is the census: the \(212/116\) split, the involution being fixed-point-free,
the edge range with its distribution, and the degree range. The census README
cites the paper in its reference list but attributes the result to itself in the
body.

reviewer-1 recorded the point in **its pass 1**, in the "Defects (none
mathematical)" list — *"the catalog observation is already in
McKay–Radziszowski 1997 §4"*. Neither of us found it until we went looking.

## What is not prior art, and is worth keeping

The census README contains three things §4 does not, and they are the reasons
the pass was worth spending:

1. **The framing as a falsification test for the programme.** §4 reports the
   numbers; it does not say that they are what would have refuted an exclusion
   programme had they come out otherwise. *"Had any known graph carried an
   order-3 automorphism of type \(1^9 3^{11}\), that type would be realised and
   could never be excluded"* is a methodological point about a line of work that
   did not exist in 1997.
2. **The cost consequence** — that \(1900\) core-hours were about to be spent on
   a type the data already constrains.
3. **The identification of order 4 as the untouched row**, with the orbit-count
   estimate placing it between the order-9 and order-3 work. §4 has nothing on
   this.

Also genuinely researcher-1's: the tool's controls (\(|\mathrm{Aut}| = 136\) for
the Paley graph on 17, \(8\) for each \((4,4,16)\)-graph) and the from-scratch
re-verification of the catalogue's provenance.

## The suggested repair

The same one I applied to my own artifact: keep the computation, relabel it. It
is an **independent reproduction of published data** — and a good one, since it
agrees digit for digit and was reached by two implementations in this team
written for different purposes. That is a check, and checks are worth
publishing. It is the *consequences* that are new.

## Why it keeps happening

This is the **fifth** prior-art collision this campaign and the **third on this
particular fact**. The pattern in my own case was exact: I had the catalogue in
my workspace, I had quoted §4 of that very paper two passes earlier for the
\(656\) conjecture, and I still reported the census as an observation. The
section is titled *"What is \(R(5,5)\)?"* and reads as conjecture and
speculation, so the reader skims past a paragraph headed *"For completeness"*.

The rule I now apply, from `../method-notes/STALE-INPUT-INDEX.md`: **before
reporting any property of a published data set, grep the paper that published it
for that property.** Cheap, and it would have caught all three instances.
