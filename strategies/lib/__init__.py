"""Shared, causal building blocks for candidate strategies.

Append-only by convention (see CLAUDE.md): a promoted candidate is copied to
`strategies/champion.py` and keeps importing this package, so editing a function
in place would silently change an already-measured champion. Add a new function
instead; CI requires `[engine-maintenance]` to modify an existing file here.

Everything in this package is causal by construction: the value on row `t` of a
returned frame uses only data at or before `t`. Nothing here reads the store,
the splits, or `trials.jsonl`.
"""
