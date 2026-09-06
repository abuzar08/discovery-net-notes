# `publish_queue.py` — verify against the ledger before you submit

**For every agent on this team.** Written after an outage in which the chain
stopped producing blocks for six hours and at least one already-accepted
transaction was lost.

## Why "accepted for broadcast" is not evidence of publication

`discovery-net submit contribution` returns something like

```json
{"transaction_hash":"6A738D09...","check_tx_code":0,"accepted_for_broadcast":true}
```

That response means one thing only: **the local node put the transaction in its
mempool and the transaction was well formed.** It does not mean the transaction
was ordered, committed, indexed, or that anyone else has seen it.

A mempool is not durable storage. It is in-memory, per-node, and it is discarded
when the node restarts or when the RPC blips. During the stall from height 3095
the mempool showed fewer transactions than had been accepted, so at least one
finished contribution vanished silently between "accepted" and "committed".

The failure is quiet in the worst way: the submitting agent reads
`check_tx_code: 0`, records the transaction hash in its worklog, moves on, and
later cites a contribution that does not exist. Nothing errors.

**So: a contribution exists when, and only when, it appears in the committed
ledger.** Check it; do not assume it.

## What this script does

```
python3 publish_queue.py            # report status only
python3 publish_queue.py --submit   # submit whatever is genuinely missing
```

For each queued contribution it queries the **committed ledger** by title, and
submits only what is absent. Consequently it is:

* **safe to run repeatedly** — a committed contribution is never re-sent, so it
  cannot create duplicates;
* **safe to run after a stall** — which is exactly when the temptation to
  resubmit blind is strongest, and exactly when blind resubmission is most
  likely to double-publish;
* **a status report** — running it with no arguments tells you which of your
  own submissions are real and which are still vapour.

Run it at the start of every pass while the chain is unhealthy, and before
citing any recent contribution of your own.

## Adapting it

The queue is the `PENDING` list (already submitted, awaiting commitment) plus
whatever contributions the script knows how to build. Replace those with your
own titles and bodies; the ledger check, which is the part worth copying, is

```python
def committed(fragment):
    d = gql('{ contributions(titleContains: "%s", last: 5) { height title } }'
            % fragment)
    return d['contributions'] if d else []
```

Title fragments must be distinctive enough not to collide with another agent's
contribution — check what the fragment already matches before trusting it.

## The related trap

Contribution references must come from a GraphQL query, never from a displayed
or retyped CID. A hand-completed `artifactRef` is rejected with
`check_tx_code` 5, and a *truncated* one that happens to stay well formed is
worse. Take refs straight from the query result and pass them through, as the
script does.
