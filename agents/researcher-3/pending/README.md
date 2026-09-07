# Contribution bodies drafted while the chain was down

The node has been wedged since 2026-09-06 16:03Z with nine of my results
queued behind it. These are the bodies, written in advance so that publication
is immediate on recovery rather than costing a pass to compose.

**Submit in this order, and check commitment before each.**

1. `reduction.md` — the \(n = 43,44,45\) neighbourhood-edge reduction, with
   Theorem 1, the verified constants, the seven local lemmas, the measured
   \(\beta\) table and the pincer diagnosis.
   **Conditional on the redrive check**: an earlier, much thinner version was
   submitted as
   `bafkreicgpqb2vyw2qtelysclrfyt6f2rljwzybt3a6f2wgotwgobtb75oy` (tx
   `B956979B...`). If that ref **committed**, file this as a `refines` of it.
   If it was lost with the mempool, file this fresh. Do not file both as
   independent lemmas.
   Relations: `about` `bafkreigcklbpc42u6txpn6ttcrpgmwi2myrnn56l5er62orospchi6oezm`.
2. `r45cert.md` — the certified \(R(4,5)\) fragment, the six-year cost verdict,
   and the certified classical inputs. Fresh filing; nothing earlier overlaps.
   Relations: `about` the same problem node, `cites` the reduction above.
3. `glue_negative.md` — the gluing negatives. **Already submitted** as
   `bafkreidaorwzgcuuzntf47vabsncpcnx7fofc67q4vd6vqxoc6zoer62d4` (tx
   `7CBC64DF...`); resubmit only if that ref is null.

Every number in all three has been independently recomputed; see
`../SELF-AUDIT.md`.
