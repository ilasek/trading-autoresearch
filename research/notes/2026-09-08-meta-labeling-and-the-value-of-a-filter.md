---
title: "On Market Timing and Investment Performance, Parts I and II" — read as the pricing theory for meta-labeling (López de Prado; Joubert; Meyer–Joubert–Alfeus)
authors: Merton (Part I); Henriksson, Merton (Part II). Meta-labeling sources: López de Prado; Joubert; Meyer, Joubert, Alfeus
year: 1981 (both Merton papers); 2018 / 2022 (meta-labeling sources)
venue: Journal of Business 54(3), 363–406 and 54(4), 513–533 — Tier 1 (peer-reviewed). Meta-labeling: a trade book (Wiley), and The Journal of Financial Data Science 4(3), 31–44 and 4(4), 10–24 — Tier 3/4 practitioner
url: https://doi.org/10.1086/296137 and https://doi.org/10.1086/296144 — meta-labeling https://doi.org/10.3905/jfds.2022.1.098 and https://doi.org/10.3905/jfds.2022.1.108
citations: Merton Part I — 466 (Crossref), 505 (OpenAlex), 199 (Semantic Scholar), all by DOI:10.1086/296137, checked 2026-09-08. Henriksson–Merton Part II — 1221 (Crossref), 1355 (OpenAlex), 810 (Semantic Scholar), by DOI:10.1086/296144, checked 2026-09-08. Meta-labeling — Joubert 2022 **1** (Crossref, DOI:10.3905/jfds.2022.1.098, checked 2026-09-08); Meyer–Joubert–Alfeus 2022 **1** (Crossref, DOI:10.3905/jfds.2022.1.108, checked 2026-09-08); the López de Prado book carries no DOI and is not indexed as an article.
sample_period: n/a for both Merton papers — Part I is equilibrium theory, Part II is statistical procedure; neither reports a historical performance sample. Not established for the meta-labeling sources, which were not read.
markets: none (theory and test procedure); the meta-labeling sources are not market-specific as far as their public descriptions state
tier: A for the Merton–Henriksson pair (tier-1 peer-reviewed, theory plus an exact distribution-free test). C for the meta-labeling sources, which are the mechanism's only primaries and consist of a trade book plus two practitioner-journal articles carrying **one recorded citation each**.
validation_overlap: false
published_post_2018: false for the Merton papers; true for the meta-labeling sources
---

Merton Part I and Henriksson–Merton Part II both read **in full**, from the MIT Sloan working
paper versions scanned by the Internet Archive (`archive.org/details/onmarkettimingin00mert` and
`.../onmarkettimingin00henr`), using the items' OCR `_djvu.txt` full text. **This is a channel
worth recording**: MIT DSpace, which holds the same two scans, rate-limits an automated client
with HTTP 429 and did not serve them across five retries with backoff; the Internet Archive
served both instantly *and* as extracted text, so neither page-image rendering nor `pypdf` was
needed. Where a scanned working paper exists, check `archive.org/metadata/<id>` for a
`_djvu.txt` before rendering anything.

The three meta-labeling sources are **not read**. The publisher (`pm-research.com`) redirects an
automated client into an OpenID authorization flow, and the book has no open text. The
construction below is taken from the authors' **own published reference implementation**
(`github.com/hudson-and-thames/meta-labeling`, the code base for the JFDS papers) plus the
publisher's public description — the channel `SUMMARY.md` added on 2026-09-07 for method papers.
No finding is relied on from any of the three; they supply the *object*, and the Merton pair
supplies the *price*.

This completes the last `program.md` sub-mechanism with no coverage — `portfolio-learning`'s
"stacking or meta-labelling over family leads". Its other half is
`notes/2026-09-08-stacked-regressions-nonnegative-weights.md`.

## Mechanism

**The object.** Meta-labeling splits a strategy into two models. A **primary** model decides the
*side* of a bet. A **secondary** model is then trained on a different target — not "what will the
return be" but "**was the primary model right**" — and its predicted probability is used to decide
whether to take the bet at all and how large to make it. The claimed benefits, in the sources'
own framing, are filtering false positives and sizing positions, with the secondary model's
output read as an estimated probability of a profitable trade and fed into a position-sizing
function; the companion paper compares six such functions on calibrated and uncalibrated
probabilities. The appeal is decomposition: a model that only has to judge *whether* a signal is
trustworthy can use features (volatility state, breadth, dispersion, the signal's own strength)
that would be noise in a return-prediction model.

**The price, and it is exact.** Strip the machine learning away and a meta-labeling layer is a
*forecast that switches exposure between a risky and a riskless position*. That is precisely
Merton's market timer, and Merton's Part I settles what such a forecast can be worth, without
assuming CAPM, without assuming a return distribution, and without any parameter that decays.

Define the two **conditional** hit rates of the filter:

    p1 = Prob{ filter says "off"  |  the bet would have lost }
    p2 = Prob{ filter says "on"   |  the bet would have won  }

Then:

- **`p1` and `p2` are the sufficient statistic, and the unconditional accuracy is not.** Merton
  states it directly: "the probability of a correct forecast by the market timer is neither a
  necessary nor a sufficient statistic for determining whether or not his forecasts have positive
  value. Rather, it is the probability of a correct forecast, *conditional upon the return on the
  market*, which serves as such a sufficient statistic." The unconditional accuracy depends on
  the observer's prior over up- and down-states; the pair `(p1, p2)` does not.
- **Proposition III.2 — if `p1 + p2 = 1` the forecast is worth exactly zero**, to every investor,
  regardless of how accurate it looks. The proof is one substitution: at `p1 + p2 = 1` the
  posterior distribution equals the prior for *every* value of the forecast.
- **Proposition III.3 — `p1 + p2 > 1` is necessary, and (Section IV) sufficient, for positive
  value**, and "the larger is `p1 + p2`, the more valuable is the forecast information."
- **Proposition III.4 — a forecast independent of the outcome is worthless**, and the corollary
  is the one to keep: a filter that is *always* on has `p1 = 0, p2 = 1`, hence `p1 + p2 = 1`, and
  is worth nothing. So is a filter that is always off. Merton's phrasing: "Like a stopped clock,
  such a forecast will sometimes be correct, but it never has any value." A filter that leaves
  95% of bets untouched is *nearly* a stopped clock and is worth nearly nothing, no matter how
  high its raw accuracy reads.
- **A forecast that is reliably wrong is as valuable as one reliably right**, provided the bias
  is known: the contrary forecast has `p1' = 1 − p1`, `p2' = 1 − p2`, so `p1 + p2 < 1` flips to
  `> 1`. The null is `= 1`, not `≤ 1`, and it is two-sided.
- **The value is an option price.** Merton constructs an options portfolio that replicates the
  timer's fund and shows the equilibrium management fee per forecast period is
  `m = Δ · g · (p1 + p2 − 1)`, where `g` is the price of a one-period **put** on the market
  struck at the riskless return and `Δ = η2 − η1` is the swing in market allocation between the
  two forecasts. Three multiplicative terms and nothing else: **skill above chance × the price of
  the option the timing pattern replicates × how aggressively you act on it.** The isomorphism is
  to a *protective put*, which is why timing returns are asymmetric and why the value of any
  timing overlay rises with volatility and with the forecast horizon.

## Construction recipe

**The filter, as the sources build it.** (a) Run the primary strategy and record, for each
signal it emits, whether the realised outcome made it a winner. (b) Train a binary classifier on
those labels using features about the *state* rather than the direction. (c) Convert the
predicted probability into an exposure — thresholded on/off, or through a sizing function, with
calibration of the probabilities treated as a separate step.

**The test, which is the part with a proof behind it.** Henriksson–Merton's non-parametric
procedure tests `H0: p1 + p2 = 1` and needs no return distribution, no asset-pricing model, and
no estimate of either probability. Count:

    N1 = periods the bet would have lost      n1 = of those, times the filter said "off"
    N2 = periods the bet would have won       n2 = of those, times the filter said "off" (errors)
    n  = n1 + n2 = total times the filter said "off"

Under the null, conditional on `N1`, `N2` and `n`, the distribution of `n1` is **hypergeometric**
— `P(n1 = x) = C(N1,x) C(N2, n−x) / C(N1+N2, n)` — and, in the authors' words, "is independent of
both `p1` and `p2`", with feasible range `max(0, n − N2) ≤ n1 ≤ min(N1, n)`. It is an exact test
of independence in a 2×2 table with both margins fixed; a normal approximation to the same
hypergeometric is given for large samples. **The whole test is four counts.**

**The parametric version, when the filter's decisions are not directly observable** (e.g. it is
embedded in a continuous sizing function): regress the strategy's excess return on the market
excess return `x(t)` *and* on `y(t) = max(0, −x(t))`,

    Z_p(t) − R(t) = α + β1 x(t) + β2 y(t) + ε(t)

where `β2 = (p1 + p2 − 1)(η2 − η1)` isolates timing and `α` isolates selection. The second
regressor is the put payoff, which is the same isomorphism in regression form. Note the
consequence: **timing skill and selection skill are separately identified, and a timing overlay
that is really a selection effect shows up in the wrong coefficient.**

## Robustness evidence (qualitative only)

The Merton pair is theory and exact statistics in a tier-1 peer-reviewed venue, with citation
counts in the hundreds and low thousands respectively across three indexes. Propositions III.1–5
are algebra; the hypergeometric test is exact and distribution-free, conditional on the margins.
Neither decays and neither has been overturned; the substantial downstream literature refines the
test (generalisations of the non-parametric statistic, corrections to the parametric
specification) rather than disputing the sufficient statistic. The framework's own scope limit is
explicit: it assumes frictionless markets, no taxes and no transaction costs, and a forecaster
small enough to be a price taker.

**The meta-labeling half has no comparable evidence and it should not be presented as if it did.**
Its primaries are a trade book and two practitioner-journal articles with **one recorded Crossref
citation each**, none of which was readable here. That is Tier C by this folder's rubric —
hypothesis fodder — and the honest summary is that the *idea* is plausible and the *evidence* is
absent. Nothing in this note relies on any empirical claim from them.

## Implementability here

**The structural mapping, which is what makes this decisive rather than tangential.** Under a
long-only mandate the primary model's "side" is always long. So the secondary model has exactly
one degree of freedom: **hold or hold less.** Meta-labeling in a long-only book *is* a
market-timing overlay — not by analogy, but because the two objects have the same decision space.
Merton's theory therefore prices it exactly, and three consequences follow that the lab can act on
without a trial:

1. **The screen: estimate `p1 + p2 − 1` before building anything.** Any proposed gate — a
   volatility state, a breadth condition, a dispersion filter, a learned classifier over the
   champion's own signals — reduces to a binary decision per rebalance date on the train split.
   Count the four numbers, run the exact hypergeometric test, and read the two-sided `p`-value.
   If `p1 + p2` is not reliably away from 1, the gate is worthless *whatever its architecture*,
   and no amount of model class, feature engineering or calibration changes that. Free, train-only,
   no trial, no holdout. See candidate #91.
2. **Pin the base rate first, or the screen lies to you.** The stopped-clock corollary is the trap
   this lab is most likely to walk into: a filter that is off on 5% of dates has a high raw hit
   rate and `p1 + p2` barely above 1. The hypergeometric test already conditions on `n`, so it is
   immune — which is precisely why it must be used instead of an accuracy or an IC. This is the
   same discipline as the 2026-09-06 "pin breadth by construction" rule, arriving from a different
   direction.
3. **The value is an option price, so read the sizing term too.** `m = Δ · g · (p1 + p2 − 1)`
   says a gate with real skill still pays nothing if `Δ` — the difference in exposure between "on"
   and "off" — is small. A gate that trims the book by a few percent cannot be worth much even if
   it is genuinely informed. Conversely a large `Δ` in a long-only book means large swings to cash,
   whose turnover this repo charges at 15 bps per side and whose realised cost is not in Merton's
   frictionless model at all. **The lab's own record already reports the empirical version of
   this**: `learnings.md`'s standing finding is "blending beats switching", with the vol-managed
   and turbulence-gated variants cutting a blend's Sharpe rather than raising it. Merton says why
   a switching overlay has to clear a high bar; the lab has measured that its overlays did not.

**This is therefore an anti-candidate, and a well-priced one.** `portfolio-learning` has closed
four times, `program.md`'s own instruction is against a further operator over these legs, and
meta-labeling's evidence base is a book plus two one-citation articles. The recommendation is
**not** to spend a trial on a meta-labeled construction. What the note contributes instead is the
screen in point 1, which is cheap, exact, and would have been the right first question for the
regime-switching and turbulence-gated candidates the lab already ran and refuted.

**One connection worth stating, because it closes a loop opened by the companion note.** The
stacking note shows that a fully-invested long-only book is confined to the simplex
(`α ≥ 0`, `Σα = 1`) and is therefore an interpolating predictor bounded by its components — and
that the one linear escape is to drop `Σα = 1`, i.e. to let the book hold cash. **This note is
the price of that escape.** A book whose invested fraction varies is a market timer, and its
entire value is `Δ · g · (p1 + p2 − 1)`. So the escape is not free and is not a loophole: it is
available, it is exactly priced, and the price is a hypergeometric test the lab can run for
nothing before writing a line of strategy code.

**Known pitfalls.** (a) The test's unit of observation is the rebalance date, not the trading
day; overlapping monthly tranches break the independence the hypergeometric assumes, so run it on
non-overlapping decision dates. (b) `p1` and `p2` are defined against "would the bet have won",
which requires a fixed forward horizon — choose it before looking, since it is a researcher
degree of freedom. (c) Merton's world has no costs; a gate that passes the test can still lose
money here, so the test is a **necessary condition only** — a kill switch, never a green light.
(d) The test is about the *market* leg in Merton's setting; applied to a cross-sectional book the
"bet" is the book's active return against its own benchmark, and that benchmark must be named
(the 2026-09-06 correction: for an equal-weight long-only book it is the equal-weight universe).

## Related

- `notes/2026-09-08-stacked-regressions-nonnegative-weights.md` — the other half of the same
  `program.md` clause. That note derives why a fully-invested long-only combination is bounded;
  this one prices the only linear way out.
- `notes/2026-09-01-multi-signal-overfitting-critical-t.md` — "the value of an aggregation
  operator is the value of its nonlinearity". A filter is a nonlinear operator, and Merton's
  option isomorphism is exactly what its nonlinearity is worth.
- `notes/2026-09-07-hierarchical-risk-parity-clustering-allocation.md` and `SUMMARY.md` #86 — the
  family's other anti-candidate. Same family, same conclusion, independent reasons.
- `experiments/learnings.md` — "blending beats switching", and the vol-managed / turbulence-gated
  results. This note supplies the theory those measurements were an instance of, and the screen
  that would have predicted them.
