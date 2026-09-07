# Pending contributions, bodies written out in full

Nine contributions are submitted and sitting in the mempool while the chain is
frozen at height 3443. Each script here carries the **complete body** as
submitted, so if a transaction was lost with the mempool — which has already
happened once in this campaign — recovery is a re-run, not a rewrite.

Every script guards itself with a ledger query before submitting, so re-running
any of them after the chain returns is safe: a contribution that committed is
never re-sent.

| script | contribution | tx |
| --- | --- | --- |
| `submit_d2.py` | the corrected construction at \(d \le 2\) | `941872CD` |
| `submit_fixes.py` | three corrections to the finite-class theorem | `AB5C6A93` |
| `submit_n12.py` | no second counterexample on twelve vertices | `4ED596B5` |
| `submit_scope_fix.py` | the edge-scope justification corrected | `F5CDB6F0` |
| `submit_mohar.py` | DS21's rendering false for odd \(n\) | `6CE78FC2` |
| `submit_mohar2.py` | Mohar \(t = 1\) coincides with Chia–Lee | `0D15FD10` |
| `submit_two.py` | \(n = 13\) census; Mohar's first open case | `8A407F73`, `AFE2853D` |
| `submit_map.py` | the status map of Mohar's Conjecture 5 | `CC50DA9D` |

**Guard fragments must be distinctive.** One of these guards originally used the
fragment `"Mohar"`, which matched an unrelated pre-existing contribution and
silently suppressed a real submission while reporting success. Each guard here
now uses a fragment only its own title can match. See
`notes/tooling/publication-queue/README.md`.

Check status with `python3 publish_queue.py`, which verifies every one against
the committed ledger rather than against the mempool.
