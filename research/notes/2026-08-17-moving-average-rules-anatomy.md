---
title: "Market Timing with Moving Averages: Anatomy and Performance of Trading Rules" (working paper) / "Market Timing with Moving Averages: The Anatomy and Performance of Trading Rules" (book)
authors: Zakamulin
year: 2015 (working paper), 2017 (Springer monograph)
venue: SSRN working paper; Springer, New Developments in Quantitative Trading and Investment series (venue tier 2 — substantial working paper subsequently published as an academic monograph; the author has a peer-reviewed track record in this specific area)
url: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2585056 ; https://link.springer.com/book/10.1007/978-3-319-60970-6
citations: working paper 31; Springer monograph 23 (OpenAlex, checked 2026-08-17). Low for the age — the analytical decomposition is the durable contribution, not a widely-cited empirical result.
sample_period: long-horizon US market data; exact span not verified when this note was written (full text was unreachable under the then-current egress restriction — re-checkable now, see SUMMARY tooling note)
markets: US equity indices (market-timing setting)
tier: B — the analytical result is a mathematical identity and needs no replication; the empirical performance claims around it are single-market and were not verifiable this session
validation_overlap: false (work predates 2018)
published_post_2018: false
---

## Mechanism

The contribution is analytical rather than empirical, which is why it survives not being able to
read the performance tables: **every moving-average-based trading indicator can equivalently be
written as a weighted average of past price changes.** Crossover rules, price-minus-moving-
average rules, moving-average envelopes, and plain momentum rules are all the same object —
a linear filter applied to the return series — and they differ *only* in the shape of the
weighting function they apply to past returns.

The consequence the author draws is the one worth carrying: **the performance of a moving-average
trading rule depends exclusively on the shape of its return-weighting function.** Not on the type
of average, not on the rule's name, not on whether it is framed as a crossover or a level
comparison. Two rules with similar weighting-function shapes are near-duplicates however
different their descriptions sound, and the profusion of named technical rules is mostly
re-parameterisation rather than genuine variety — the author's framing is that half a century
of development has consisted of proposing new ad-hoc rules without analysing what they have in
common.

The second, related theme is **window-size (parameter) risk**. Because a rule is fully
characterised by its weighting function, and the averaging window is that function's principal
parameter, a rule tuned to one window is a bet on that parameter. The author's response is to
ask which weighting schemes generate *sustainable* performance across a broad range of window
sizes (a manifold of roughly 4 to 18 months) rather than which window maximises performance —
defining robustness as insensitivity to the averaging-window choice, and reporting that some
schemes' performance is stable as the window grows while others' (notably the plain momentum
rule) deteriorates.

## Construction recipe

Less a strategy than a diagnostic procedure to run *before* building one:

- **Write any candidate trend/MA rule in its equivalent form**: the vector of weights it places
  on past daily (or monthly) returns. This is a derivation, not a backtest.
- **Compare that weight vector's shape to rules already tested.** Similar shape ⇒ expect similar
  behaviour, regardless of naming or framing.
- **Judge a rule by performance stability across the window-size range**, not by its performance
  at the best window. A rule whose merit disappears when the window moves is a parameter bet.
- If a single window must be chosen, prefer weighting schemes whose behaviour is flat in window
  size over schemes that peak sharply.

## Robustness evidence (qualitative only)

The equivalence result is an algebraic identity and is therefore as robust as any result in this
folder — it does not depend on a sample and cannot decay. The empirical claims layered on it
(which weighting schemes are stable in window size; that momentum-rule performance degrades as
the window lengthens) are single-market, from one author, and were **not verifiable this
session**; they should be treated as tier-C-strength claims sitting on top of a tier-A-strength
identity. The author's broader body of work on moving averages is peer-reviewed and the
monograph was published by an academic press, which is what keeps the overall tier at B rather
than C.

No transaction-cost treatment was verifiable this session, and the setting is market timing on
an index rather than cross-sectional selection.

## Implementability here

The empirical half is a poor fit — it is single-market long/flat index timing, which is close to
the binary SPY-trend regime switch the lab has already refuted, and nothing here argues that
refutation was wrong. **The analytical half, however, is a free triage rule of exactly the kind
`learnings.md` says has been most valuable**, and it costs no trial:

> **Before testing any new trend or moving-average rule, write down the weights it places on
> past returns. If that weight vector is close in shape to one already tested, the rule is a
> re-parameterisation and should not cost a trial.**

This slots directly into the lab's established practice of killing ideas with holdings-only
diagnostics (rank-correlating candidate scores, checking what a component's code actually
reads). It is the same move applied one level earlier — at the signal-definition stage, on
paper, before any code runs. It is also a sharper instrument than rank-correlating realised
scores, because it is derivable in closed form and needs no data at all.

Two concrete applications available immediately:
- The lab's refuted **per-asset 200-day-MA filter** and the refuted **binary SPY-trend switch**
  can be checked for weight-shape similarity to each other; if they are near-duplicates, their
  two independent refutations are really one, which slightly weakens how much evidence the lab
  should think it has against trend overlays generally.
- The champion's **6-1/12-1 composite** is itself expressible as a weight vector over past
  returns (a flat-ish weighting over months −12 to −2 with month −1 zeroed). Any proposed new
  horizon or lookback for the composite can be compared to it in that form, which is a cheaper
  and more decisive test than the rank-correlation diagnostic the lab currently uses — and it
  gives a principled way to ask whether a proposed additional ensemble component supplies real
  decorrelation before building it.

Pitfall: the identity holds for *linear* filters of past returns. Rules with a genuine
non-linearity — a buffer/hysteresis band, a threshold trigger, a cap — are **not** covered by
it, and the champion's buffer and vol-spike trim are exactly such non-linearities. So the triage
rule applies to scoring signals, not to construction mechanics, and it must not be used to argue
that two constructions are equivalent when they differ in their non-linear parts. That boundary
is precisely where the lab's own live edge sits, which is a reassuring sign about where the
remaining opportunity is.

## Related

- `notes/2026-08-17-time-series-momentum-evidence-and-replication.md` — the family this rule
  class belongs to, and the reason its prior here is low.
- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md` — the window-size
  robustness theme is the same average-don't-select principle, arrived at independently; note
  that this author's answer is to *find a robust weighting scheme*, whereas the combination
  literature's answer is to *hold several and average*. The latter is better supported.
- `experiments/learnings.md`: the 0.89 rank-correlation diagnostic that killed an inter-signal
  ensemble (this note gives a cheaper closed-form version of that test); the refuted 200dma and
  SPY-trend overlays (candidates for the duplicate-check above).
