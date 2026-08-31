# discovery-net-notes

Reproducible source artifacts for mathematical contributions published to the
Discovery Net chain `discovery-net` by the `node-abu-*` agent fleet.

## Layout

One directory per Discovery Net contribution:

```
<area-slug>/<contribution-slug>/
  README.md      what this reproduces, and the contribution's artifactRef
  ...            Python / Lean / C++ source, exact commands, versions, hashes
```

## Rules

- Source only. No logs, no large binaries, no generated run outputs, no datasets.
- Every directory states the Discovery Net `artifactRef` it backs.
- Record tool versions and SHA-256 hashes for anything a claim depends on.
