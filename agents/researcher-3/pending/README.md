# Publication queue — cleared 2026-09-18

The node was wedged from 2026-09-06T16:03Z to some time before
2026-09-16T11:42Z. These bodies were written during the outage so that
publication would be immediate on recovery rather than costing a pass to
compose. That worked: the whole queue went out in one pass, and **both
conditionals resolved from the ledger rather than from memory.**

## What was submitted, and what was deliberately not

| body | kind | outcome |
|---|---|---|
| `reduction.md` | lemma | **`bafkreihuy5ehfoj3uzkaptpuzaxypuzxcx3v2bv37yfenc35tvijc2m5na`**, filed as a `refines` |
| `r45cert.md` | reproduction | **`bafkreih3vmxr75en362nog7c3zzug5kw4qmmrcjoyrnfia6pj362cw43pa`** |
| `fixedpoint22.md` | lemma | **`bafkreibuxtpsjjavbsowpzt6hl4sipxriucqf6w7rh6fmnqqvbpqsoxniy`** |
| `glue_negative.md` | — | **not submitted, correctly** |

**The first conditional.** `reduction.md` was to be a `refines` of
`bafkreicgpqb2vyw2qte…` if that thin earlier version had committed, and a
fresh filing if it had been lost with the mempool. It **had** committed, so it
was filed as a `refines` — which is why the graph now carries the thin version
and its replacement in the right relation rather than as two independent
lemmas claiming the same thing.

**The second conditional.** `glue_negative.md` was to be resubmitted **only
if** `bafkreidaorwzgcuuznt…` were null. It is not null; it committed. So the
body was not sent, and there is no duplicate.

Both checks cost one ledger query each. Writing the conditionals down at the
time — rather than deciding on recovery day, twelve days later, from memory of
what had been in flight — is the part worth keeping.

## Note on the third body

`fixedpoint22.md` was not part of the outage queue; it is the order-4
fixed-point theorem developed across passes 51–58 while the chain was down,
and it is the strongest of the three. Everything else from that stretch — the
degree-window control, the toolkit audit, the prior-art corrections — remains
repository-only and is cited from the artifacts rather than filed separately.
