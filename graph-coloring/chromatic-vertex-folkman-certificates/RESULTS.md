### Exact values (lower-bound chain + verified witness)

| n(k,q) | value | chain refuted for m | witness edges | largest LRAT in chain |
|---|---|---|---|---|
| n(4,3) | **11** | 4..10 (7 certificates) | 20 | 29 KB |
| n(4,4) | **6** | 4..5 (2 certificates) | 10 | 0 KB |
| n(5,4) | **11** | 5..10 (6 certificates) | 30 | 435 KB |
| n(5,5) | **7** | 5..6 (2 certificates) | 16 | 1 KB |
| n(6,5) | **10** | 6..9 (4 certificates) | 35 | 15 KB |
| n(6,6) | **8** | 6..7 (2 certificates) | 23 | 2 KB |
| n(7,5) | **13** | 7..12 (6 certificates) | 52 | 3182 KB |
| n(7,6) | **11** | 7..10 (4 certificates) | 45 | 36 KB |
| n(8,6) | **14** | 8..13 (6 certificates) | 65 | 14401 KB |

### Certified lower bounds (chain complete, value not yet reached)

| n(k,q) | certified | chain refuted for m | largest LRAT in chain |
|---|---|---|---|
| n(6,4) | **>= 14** | 6..13 (8 certificates) | 152.3 MB |
| n(7,4) | **>= 15** | 7..14 (8 certificates) | 178.6 MB |
| n(8,5) | **>= 15** | 8..14 (7 certificates) | 135.3 MB |
| n(9,6) | **>= 15** | 9..14 (6 certificates) | 26.3 MB |

### Certificate manifest

| tag | partitions | LRAT bytes | xz bytes | stored | sha256 (prefix) |
|---|---|---|---|---|---|
| `n4_k4_q3` | 0 | 107 | 140 | yes | `4a5e7051ef14c054` |
| `n5_k4_q3` | 0 | 328 | 236 | yes | `8f90492efbad94ab` |
| `n6_k4_q3` | 1 | 775 | 340 | yes | `ce3f0c0189ee0a26` |
| `n7_k4_q3` | 2 | 1520 | 484 | yes | `542bb6ea40bf10cb` |
| `n8_k4_q3` | 8 | 2622 | 736 | yes | `277889c9a612e1ac` |
| `n9_k4_q3` | 16 | 8929 | 2336 | yes | `4b5a5ca833704831` |
| `n10_k4_q3` | 55 | 29818 | 5992 | yes | `9924b036d634fcd1` |
| `n4_k4_q4` | 0 | 98 | 132 | yes | `52bf1ee3579e9bad` |
| `n5_k4_q4` | 1 | 406 | 272 | yes | `e0a322c05a7f1b27` |
| `n5_k5_q4` | 0 | 224 | 184 | yes | `585cf654794c3c9e` |
| `n6_k5_q4` | 1 | 772 | 352 | yes | `26f8d28c5fbf84f8` |
| `n7_k5_q4` | 8 | 1801 | 564 | yes | `15db8a6957447be1` |
| `n8_k5_q4` | 31 | 3471 | 880 | yes | `2c80d426affe14bf` |
| `n9_k5_q4` | 119 | 30957 | 7400 | yes | `70c94bf25da6150d` |
| `n10_k5_q4` | 846 | 445305 | 98372 | yes | `f8e81f4e2e42bf07` |
| `n5_k5_q5` | 0 | 212 | 188 | yes | `f5eb4229632d9164` |
| `n6_k5_q5` | 2 | 812 | 368 | yes | `1297bea916cd61fc` |
| `n6_k6_q4` | 0 | 448 | 248 | yes | `68ddc30a70001dfb` |
| `n7_k6_q4` | 0 | 1240 | 404 | yes | `7171a28707245487` |
| `n8_k6_q4` | 4 | 3020 | 728 | yes | `f0944d31abafca0a` |
| `n9_k6_q4` | 24 | 11316 | 2624 | yes | `a6600dff0b54eb13` |
| `n10_k6_q4` | 114 | 37238 | 8152 | yes | `449fe901cbd5443b` |
| `n11_k6_q4` | 421 | 272288 | 60188 | yes | `38befc0c25786e4d` |
| `n12_k6_q4` | 2299 | 4822792 | 1047984 | yes | `84d186c01f681c11` |
| `n13_k6_q4` | 11897 | 159729815 | -1 | no (hash only) | `e9ea4ee7e91440f0` |
| `n6_k6_q5` | 0 | 412 | 248 | yes | `152ef39d606bede0` |
| `n7_k6_q5` | 1 | 1402 | 468 | yes | `76e3d8708e1f7e29` |
| `n8_k6_q5` | 20 | 4114 | 1072 | yes | `f094fe8401cca661` |
| `n9_k6_q5` | 94 | 15473 | 3684 | yes | `05e9e18c4884dadb` |
| `n6_k6_q6` | 0 | 392 | 240 | yes | `c109983372dfd8ed` |
| `n7_k6_q6` | 2 | 1584 | 572 | yes | `2f8df82d3b0dcc97` |
| `n7_k7_q4` | 0 | 792 | 296 | yes | `7b1fd720f32def79` |
| `n8_k7_q4` | 0 | 1902 | 488 | yes | `4f4b43f82de6b2fe` |
| `n9_k7_q4` | 1 | 4322 | 812 | yes | `fc0b3f4556f123f4` |
| `n10_k7_q4` | 9 | 16502 | 3060 | yes | `6e9af738ec09f986` |
| `n11_k7_q4` | 76 | 47047 | 8584 | yes | `49a6eb6191959a69` |
| `n12_k7_q4` | 286 | 213252 | 43496 | yes | `8c271100cf8c7d27` |
| `n13_k7_q4` | 1413 | 2723217 | 578260 | yes | `b010202a2cce8314` |
| `n14_k7_q4` | 7075 | 187230996 | -1 | no (hash only) | `e7969df9e73a6033` |
| `n7_k7_q5` | 0 | 736 | 288 | yes | `6e6c9d9ca281ab13` |
| `n8_k7_q5` | 1 | 2197 | 600 | yes | `971eeafd5b2c716d` |
| `n9_k7_q5` | 17 | 5505 | 1200 | yes | `72c89bdf65d1ceb4` |
| `n10_k7_q5` | 118 | 26568 | 5588 | yes | `edd1e4440628ae18` |
| `n11_k7_q5` | 650 | 164477 | 37680 | yes | `095f66c9875a1419` |
| `n12_k7_q5` | 2971 | 3258357 | 708968 | yes | `e60e5b4a25d22271` |
| `n7_k7_q6` | 0 | 680 | 288 | yes | `70422d912ae95275` |
| `n8_k7_q6` | 2 | 1987 | 552 | yes | `fd1530a0cd3ac768` |
| `n9_k7_q6` | 29 | 7516 | 1788 | yes | `32debfa22cbb7bbd` |
| `n10_k7_q6` | 224 | 36800 | 7344 | yes | `4867349e198e875d` |
| `n8_k8_q5` | 0 | 1196 | 328 | yes | `09d5aa7cf622e83b` |
| `n9_k8_q5` | 0 | 3149 | 736 | yes | `d51cc92cf6f0bbaa` |
| `n10_k8_q5` | 8 | 7400 | 1136 | yes | `20a3d3dd3b36d770` |
| `n11_k8_q5` | 159 | 51642 | 9424 | yes | `52a0270ac51a7137` |
| `n12_k8_q5` | 869 | 354391 | 77428 | yes | `f4a86cf6c704619f` |
| `n13_k8_q5` | 3506 | 4371260 | 917844 | yes | `c787cc90dd6269ea` |
| `n14_k8_q5` | 14602 | 141914468 | -1 | no (hash only) | `a695072184e0f478` |
| `n8_k8_q6` | 0 | 1084 | 320 | yes | `6a1fb318406dd4db` |
| `n9_k8_q6` | 1 | 3212 | 776 | yes | `5c7a2d8218ff737b` |
| `n10_k8_q6` | 19 | 9418 | 1668 | yes | `935ebc7768e93324` |
| `n11_k8_q6` | 336 | 54462 | 9800 | yes | `126b5128ba65899b` |
| `n12_k8_q6` | 2191 | 569441 | 114588 | yes | `9b6f271608ced02f` |
| `n13_k8_q6` | 11424 | 14746522 | 2947024 | yes | `01db394740cf8036` |
| `n9_k9_q6` | 0 | 1684 | 376 | yes | `c730d00211e88db8` |
| `n10_k9_q6` | 1 | 4538 | 908 | yes | `a8d615986220d0c0` |
| `n11_k9_q6` | 29 | 16023 | 2472 | yes | `d3485a80c737e318` |
| `n12_k9_q6` | 453 | 74261 | 11780 | yes | `df0b3071aaaa21cc` |
| `n13_k9_q6` | 3436 | 1480854 | 290408 | yes | `9e6daf9fe76342bb` |
| `n14_k9_q6` | 15897 | 27537055 | 5525388 | yes | `e2fcd8cf921e62f0` |
