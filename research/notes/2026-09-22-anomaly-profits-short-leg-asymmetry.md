---
title: "The Short of It: Investor Sentiment and Anomalies"
authors: Stambaugh, Yu, Yuan
year: 2012
venue: Journal of Financial Economics 104(2), 288–302 — Tier 1 (top peer-reviewed)
url: https://doi.org/10.1016/j.jfineco.2011.12.001
citations: 1808 (Crossref is-referenced-by-count, checked 2026-09-22); 1862 (OpenAlex,
  checked 2026-09-22); 1198 (Semantic Scholar, checked 2026-09-22). Per the folder's
  session-7 rule the lone low count is the one to disbelieve — here Semantic Scholar's.
  Read in full from the NBER working-paper version (w16898), which is the same paper.
sample_period: 1965–2008 (portfolio returns from 1965:8; three of the eleven anomalies
  start later on data availability)
markets: US equities (CRSP/Compustat), eleven anomaly sorts
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The paper combines two existing ideas and derives three testable consequences. The ideas:

1. **Market-wide sentiment.** Investor beliefs contain a common, time-varying component that
   pushes many securities in the same direction at once.
2. **Miller's (1977) asymmetry.** Impediments to short selling mean that the most optimistic
   investors set the price, because the pessimists' view is expressed by *not holding*
   rather than by selling short. Overpricing is therefore possible; underpricing is much
   less so, since the rational valuation is already inside the range of views being
   expressed.

Put together: mispricing is predominantly **overpricing**, and it is worse when market-wide
sentiment is high. The three consequences the authors test:

- **H1** — anomaly long–short spreads are wider following high sentiment.
- **H2** — the **short leg** (the relatively overpriced names) is where the sentiment
  variation shows up: its returns are lower following high sentiment.
- **H3** — the **long leg** should be roughly insensitive to sentiment, because the long leg
  is not underpriced, merely least overpriced.

All three are borne out, across every one of the eleven anomalies tested. The asymmetry is
the point: in benchmark-adjusted terms the short leg carries substantially more of each
anomaly's spread than the long leg does, and this holds anomaly by anomaly rather than only
on average.

The economic reading, and the one that transfers: **an "anomaly" is usually a statement
about names an arbitrageur cannot cheaply sell, not about names they can cheaply buy.** The
tradeable-by-everyone side of the sort is the quiet side.

The paper is careful about one thing that is easy to lose. The mispricing measure is purely
cross-sectional and *relative*: the least-overpriced name in a cross-section may still be
overpriced in absolute terms. "Long leg" does not mean "underpriced", it means "least
overpriced in this cross-section" — which is precisely why H3 predicts a near-null there.

Why short selling is impeded, in the authors' own enumeration: institutional charters that
forbid it outright; the arbitrage risk of Shleifer–Vishny (an adverse move can force
liquidation before the correction arrives, and this has no unlevered long analogue);
behavioural reluctance among individuals, who almost never short; and direct shorting costs,
which — the important part — **rise with dispersion of opinion**, i.e. become expensive
exactly when a name is most worth shorting.

## Construction recipe

There is no portfolio here for a long-only lab to copy; what there is, is a **measurement
protocol for deciding where a signal's content lives**, and that protocol is the reusable
object.

1. **Sort into deciles** on the candidate variable and form portfolios within each decile
   (the paper value-weights). Define the long leg as the higher-performing extreme decile
   and the short leg as the other.
2. **Benchmark-adjust each leg separately**, not just the spread: estimate `a_i` in
   `R_i,t = a_i + b·MKT_t + c·SMB_t + d·HML_t + ε_i,t` where `R_i,t` is the *leg's* excess
   return. The decomposition of the spread's alpha into a long-leg alpha and a short-leg
   alpha is the whole experiment.
3. **Condition on a state variable** — here a market-wide sentiment index built as the first
   principal component of six sentiment proxies — split at its median, and compare each
   leg's alpha across the two states. H2/H3 are read off the *difference in differences*:
   the short leg should move with the state and the long leg should not.
4. **Combination strategy**: an equal-weight combination across the eleven individual
   long–short strategies, used to show the effect is not one anomaly's.

The eleven anomalies are financial distress (failure probability and Ohlson's O), net stock
issues, composite equity issues, total accruals, net operating assets, momentum, gross
profitability, asset growth, return on assets, and investment-to-assets. Ten of the eleven
require accounting data. The authors note the eleven are not highly correlated with each
other — the first principal component explains only about a third of their common variance,
and even the last explains a non-trivial share — which is what makes the combination
meaningful rather than a restatement of one sort.

## Robustness evidence (qualitative only)

- The long-leg/short-leg asymmetry holds for **all eleven** anomalies individually, not only
  in aggregate, and the eleven are largely independent of one another by construction.
- Results survive controls for macroeconomic conditions and hold with an alternative
  sentiment index, both reported as robustness sections.
- The general Miller-asymmetry prediction is corroborated from an entirely different angle
  by `2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md`, which reaches the same asymmetry
  from the idiosyncratic-volatility side with no sentiment index involved.
- The underlying short-sale-impediment literature the paper leans on is deep and
  multi-authored; the paper is a synthesis of it rather than a lone claim.
- **Gaps against the rubric.** Single market (US). Transaction costs are **not** modelled —
  the decile portfolios are paper portfolios, and the short legs of anomaly sorts are the
  expensive end to trade, so the reported asymmetry is if anything understated net of costs
  (which cuts *for* the paper's message but means the magnitudes are not net-of-cost
  magnitudes). Multiple testing is not formally addressed, though the use of eleven
  pre-existing published anomalies rather than a search over candidate variables is a
  partial defence. Sentiment-index construction is taken as given from another paper.

## Implementability here

**Nothing in this note is a candidate, and that is the finding.** The paper's content for
this repo is a **discount factor on every long-only cross-sectional hypothesis the lab will
ever write**, and it is the most direct mechanism anyone has offered for the stall.

- `program.md` makes this lab **long-only with gross leverage ≤ 1.0**. Under Miller plus
  this paper's evidence, the side of a cross-sectional sort that carries most of the
  abnormal return is the side this lab is structurally forbidden from holding. A long-only
  implementation of any published anomaly should be expected to capture the **minority** of
  its documented spread — before costs, before this universe's other handicaps, and before
  publication decay.
- This is a *different* explanation from the one the lab has been carrying. Eleven sessions
  have attributed nulls to "this universe's high-volatility survivors" and, latterly, to
  "monthly-horizon cross-sectional prediction may have very little signal here". Both may be
  true. But the long-only constraint alone predicts a large haircut on every anomaly, on any
  universe, and it has never been written down here as a quantity. **It should be, because
  it changes what a null means**: a long-only null is much weaker evidence against an effect
  than a long–short null would have been.
- **This also corrects a habit visible in the journal.** Candidates in this repo are
  routinely motivated by a published long–short spread and then judged as long-only books
  against a champion. The literature's effect size is not the reachable effect size. The
  discipline that follows is cheap and costs no trial: *when a hypothesis cites a published
  long–short result, state in the hypothesis line which leg the source attributes the result
  to, and if the source does not say, treat the reachable size as the minority share.*

**What *is* measurable here, and it is free.** The paper's step 2 — benchmark-adjust each
leg separately rather than only the spread — is directly runnable on this repo's data, on
any score the lab already has, with no `run_experiment.py` trial and no champion comparison.
The lab has already converged on a neighbouring rule from its own side: the 2026-09-19
nightly's "when a score is a signed combination of two arms, run the trend/artifact screen
on each arm separately". This paper supplies the **return-side** version of that rule and a
prediction to test it against: on a universe where the short leg cannot be held, the top
band's excess over the universe mean should be **small relative to** the bottom band's
shortfall. If the lab measures that shape on its own refuted scores, the refutations get a
mechanism rather than a shrug.

Two cautions, both sharp:

- **Do not try to reconstruct the mispricing measure.** Ten of the eleven anomalies need
  accounting data this repo does not have and will not get. Momentum is the only one
  reachable, and it is the incumbent's own family.
- **Do not try to build a sentiment index.** The Baker–Wurgler construction needs closed-end
  fund discounts, IPO counts and first-day returns, the equity share in new issues and the
  dividend premium — none of which are in `data/store/`. Any price-only proxy for it would be
  a market-state variable dressed in a sentiment label, and `experiments/learnings.md`
  already records that de-risking and market-timing overlays on this champion reliably
  backfire. The sentiment half of this paper is **out of scope here**; the asymmetry half is
  not, and the asymmetry half does not depend on it.

## Related

- `2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` — same authors, the asymmetry derived
  from arbitrage risk rather than sentiment, and the note with the conditional prediction.
- `2026-09-22-limits-of-arbitrage-performance-based.md` — why the short side is the risky
  side for a capital-constrained specialist.
- `notes/2026-09-13-information-uncertainty-and-price-continuation.md` — already records the
  long-side discount as a standing caveat; this note supplies the measurement behind it.
- `notes/2026-08-22-long-only-as-l1-regularization.md` — the other half of what the long-only
  constraint does to a book.
