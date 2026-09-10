# researcher-2: contributions submitted but not yet committed

The Discovery Net ledger has been stalled at block **3443** since
**2026-09-06T16:03Z**. As of 2026-09-09T10:20Z that is about **66 hours**, far
beyond the previous outage in this campaign (about nine hours, which cleared with
everything committing untouched).

Twenty-three of my contributions are queued (pass 36 produced no submission: its
content, a strengthening that closed nothing plus two negatives, is folded into
the pass-37 body). Each was accepted for broadcast with
`check_tx_code 0`, so they sit in the node's mempool. **A mempool is not durable
storage.** If the node is restarted or the mempool dropped, these submissions are
lost and would have to be reconstructed. This directory is that insurance.

Every one of them cites a GitHub commit in this repository, so the *mathematics
and its artifacts are already durable*; what was at risk is only the contribution
text and the relation targets.

## The queue

| pass | kind | artifact ref | transaction hash | body |
|---|---|---|---|---|
| 21 | lemma | `bafkreibj46rfm35nbz5fgc6asww4tdry7xt2kejj2mnki6t6cjcnoa7jq4` | `32B51CC1…E3E8` | reconstruct |
| 22 | lemma | `bafkreif7x4v3cwq2fbzdnqvidsvixy7aglc66uulfyhlentcrvhcdoxy3y` | `7C6FC1A3…4A5E` | reconstruct |
| 23 | lemma | `bafkreihj3mct4sadf43cyb4nfzx2cwtu6p2pjavamiyup55rgptki7q7im` | `A141400D…54BD` | reconstruct |
| 24 | lemma | `bafkreiby3yyat6arjzslah4ctyfbl6iel2l4leqrwv5sz54qbfzzbq5fxy` | `0C15472E…B3C9` | reconstruct |
| 25 | lemma | (see pass 24 row; residue57 closure) | `5FBECEB6…B6AE` | reconstruct |
| 26 | finding | `bafkreieda2azciig5pa5sju6qlxalh53l6x4pyenoxe4t3nf3z6en22epe` | `3F9A2537…3E15` | `pass26.md` |
| 27 | lemma | `bafkreigmmqcahaq63hwruj56wear2lct7bi5num23zmly47tvrz2hcrtvi` | `BFFC13A1…0278` | `pass27.md` |
| 28 | finding | `bafkreidnfstwip7yqhfgnv6url5pz45k5zirfq6ry6g2b6c3fltm4vku2q` | `8FE1ECAA…0CFA` | `pass28.md` |
| 29 | finding | `bafkreiby47tn7grte7ucxt3pf2cgxqxnyfg5dt7ibwro2o6wt6xf4jq4xa` | `8C4B4E7C…D021B` | `pass29.md` |
| 30 | finding | `bafkreihi35swprlytmhmg5kgjwb4xopvjwfzxybqluxu26kapwhmwuol4q` | `E258F272…5654` | `pass30.md` |
| 31 | lemma | `bafkreichvzfjx62dqx5mgmzm3t4tcxh24wdraphqlgebjneevi55lcbyf4` | `C11CDA25…291C` | `pass31.md` |
| 32 | lemma | `bafkreihwe5x4nq2s3lxthaxcon3vwmpwfdivrhzoxp6hvwdexpwmviq7ia` | `512382BB…169F` | `pass32.md` |
| 33 | summary | `bafkreih5ur2ppwnibxiljyxaqimlb5o4dnvaqpbxr5eubyd3c4mandmtxe` | `0AAE119A…BB0C` | `pass33.md` |
| 34 | finding | `bafkreifnhmjmaqzwuzzvk6deqpvsjrcee7przvt7jhjzuuwa4rd7qpwkli` | `561E2EE1…AD0D` | `pass34.md` |
| 35 | finding | `bafkreiekgbvm7uvshbyklle46p3etxw6e2tlcg2p3h76oxafoqpwrhdmbq` | `E4BB56BA…F0BC` | `pass35.md` |
| 37 | finding | `bafkreibnvjxxyyisygfdbpiduowjxe3knfwml7aau7tqzhecdhbccytkqe` | `3CEB0435…E274` | `pass37.md` |
| 38 | finding | `bafkreigw22k6k6qzpmxdbp6capverov36uek2ag24yh3tojai676uudcey` | `20AC3AAF…83D3` | `pass38.md` |
| 39 | finding | `bafkreiebblqqqclxqgl5s5jmg77e62u2oy65ulhkugdqb6yyuq7mcqilja` | `29DF4ECF…E959` | `pass39.md` |
| 40 | finding | `bafkreicqzx5mswis2rkmhpg4evkjwedmxwljnv4m4e2f7rw6prjteycpjq` | `FA0D4AFA…CD5D` | `pass40.md` |
| 41 | summary | `bafkreiejn45vzo7sxhu3an5q2qrymvaztxkno5uiyglwwdyegtay2r744m` | `39ED34B0…ACA1` | `pass41.md` |
| 42 | finding | `bafkreih45df67hesz3wnefzgagrw6bzzwmdnnldyqsee4f766nwlkiyvva` | `BE462F6C…2139` | `pass42.md` |
| 43 | lemma | `bafkreieuzklki2g7cdon7ppu5pylepnn4jkrsqpwvsfdz7a64s2fdx4eky` | `F4CACD93…0CE3` | `pass43.md` |
| 45 | finding | `bafkreih4dcapnstaitspvacmqyc2q5clhszten6urxqs7hs3yau2fd4ku4` | `9EA01F84…C769` | `pass45.md` |
| 46 | finding | `bafkreibam4ugewxb7xx63l744yq3awjhwojph43tnn72nnmedb5zyn7mga` | `9AEAAD8C…F177` | `pass46.md` |
| 47 | finding | `bafkreifk7mpulb4tsavrmavytz7ubjf7dj3btceh4fmy2yd7nxcm7gcuf4` | `5B773028…E9D7` | `pass47.md` |

Passes 21–25 predate the files kept here; their content is recorded in
`../WORKLOG.md` under the corresponding dated entries, and every artifact they
cite is committed in
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, so they can
be rewritten from that material if the mempool is lost.

## Relations

Every submission relates only to refs verified **committed** at submission time —
a lesson from the pass-24 rejection (`check_tx_code 5`), where a relation
targeted an uncommitted contribution. The usual targets are

- `bafkreid3lqitm4jq6nyraxj7aswy7v2dyu3s3klfdipqmcxrmm2n6plagu` — the \(b\ge8\)
  order-58 closure;
- `bafkreid5rciyqzspzls5xmufbr5jh33rnmaoscfefqzfvuegs56glw3y6u` — the
  seed-ladder unconditionality finding;
- `bafkreif4aphbotvuuxtek4grpghtqb463vvyzhwrpft6yfkklfwqctudfi` and
  `bafkreiafu3krb262eyahjjcr7ctiei5vqluq2wqri5vqxrcb26hjfgfpe4` — the order-\(2r\)
  non-domination and two-disjoint-triangle lemmas.

## If the queue is lost

Do **not** blindly resubmit: first query the ledger and check which refs have
committed, exactly as each pass does. Resubmitting a committed contribution
duplicates it; a rejected transaction, by contrast, creates nothing.

## What the queue is worth

The standing position it encodes is in
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/state29.py`:
\(r=27\) and \(r=28\) proved and reviewed; at \(r=29\) order 57 closed and order
58 open in 8310 configurations. Albertson's conjecture is **not** proved for
\(r=29\).
