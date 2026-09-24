---
title: "Betting against correlation: Testing theories of the low-risk effect"
authors: Asness, Frazzini, Gormsen, Pedersen
year: 2020
venue: Journal of Financial Economics 135(3), 629–652 — Tier 1 (top peer-reviewed)
url: https://doi.org/10.1016/j.jfineco.2019.07.003
citations: 90 (Semantic Scholar by DOI, checked 2026-09-24). Read in full from the
  version of record, obtained from the corresponding author's faculty-hosted copy at
  `nielsgormsen.com/Papers/` — the 2026-09-18 faculty-page channel, used on the first try
  after the publisher's own repository copy refused an automated client (see access note
  below).
sample_period: "US: 1926–2015 (factor regressions from 1963, double sorts from 1929).
  Global: 1990–2015."
markets: 58,415 stocks across the 24 developed markets of the MSCI World index; CRSP plus
  XpressFeed global, all returns converted to USD and unhedged
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

The paper's contribution to this folder is not the low-risk effect, which is covered
already and which this lab has repeatedly refused. It is a **decomposition**, and the
decomposition is an identity:

    β_i = ρ_i,m · σ_i / σ_m

A name's market beta is its **correlation with the market** times its **volatility**,
scaled by market volatility. The two components are separately measurable, separately
sortable, and — this is the paper's design — implicated by *different* theories:

- **Leverage constraints** (Black; Frazzini–Pedersen) price *systematic* risk. Investors
  who want more expected return than the market offers, and cannot borrow to get it, bid
  up high-beta assets instead. The resulting CAPM alpha is `α_i = ψ(1 − β_i)`, with ψ a
  Lagrange multiplier common to all names. **Nothing in that expression cares whether a
  high beta came from high correlation or from high volatility.** The theory therefore
  predicts a positive risk-adjusted return to betting against *either* component.
- **Behavioural / lottery demand** (Barberis–Huang; Bali et al.'s MAX; the IVOL
  literature) prices *idiosyncratic* risk and skewness. Those objects live in the
  **volatility** term and have essentially nothing to do with the correlation term.

So the correlation half of beta is the part that the two theories disagree about, and it
is the part that can be isolated. That is the whole idea: build a factor that varies
correlation while **holding volatility fixed** (BAC), and its mirror that varies
volatility while holding correlation fixed (BAV). By construction, the long and short
sides of BAC have near-identical average volatility, skewness and MAX characteristic —
so BAC is close to orthogonal to every behavioural low-risk factor, while still betting
on beta.

**The empirical result that matters here, and it is not the one the title advertises.**
Theory predicts *both* components should pay. Across the samples studied, the
**correlation** component carries significant risk-adjusted returns in both the US and
the broad global sample, while the **volatility** component does not survive the fuller
factor controls in either. The paper is honest that this is a partial failure of the
theory it supports. For this lab the reading is sharper: **within the low-risk family, the
part that pays is the co-movement part, and the volatility part is the part that does
not.** This repo has independently established (`learnings.md`, 2026-09-17 and after)
that on *its* universe the volatility level is a survivorship artifact and that scores
which reduce to it are worthless. The literature and the lab agree on which half to throw
away, for entirely different reasons.

A second, weaker mechanism is recorded for completeness: the authors also decompose the
lottery measure MAX into a volatility part and a shape part, building **SMAX** = (mean of
the five highest daily returns over the past month) / (estimated volatility). SMAX is
"MAX with the volatility scaled out" and is their behavioural analogue of BAC.

## Construction recipe

**Per-name inputs, both estimated on daily closes only.**

- **Correlation with the market**: five-year rolling window of **overlapping three-day
  log returns**, `r³ᵈ_i,t = Σ_{k=0..2} ln(1 + r_i,t+k)`. Three-day returns are used
  explicitly to defuse **non-synchronous trading**; requires ≥ 750 non-missing trading
  days.
- **Volatility**: one-year rolling window of one-day log returns; requires ≥ 120
  non-missing days.
- **Beta**: `β̂ᵀˢ = ρ̂ · σ̂_i/σ̂_m`, then shrunk toward the cross-sectional mean à la
  Vasicek: `β̂ = w β̂ᵀˢ + (1−w)·1`, with `w = 0.6`. Note their own remark — **the shrinkage
  does not change the sort, only the leverage applied**, so a long-only implementation that
  never levers can skip it entirely.

**Portfolio.** At each month start, within each country:

1. Rank on **volatility**, cut into five quintiles (NYSE breakpoints in the US).
2. **Within each volatility quintile**, rank on **correlation** and split into a
   low-correlation and a high-correlation portfolio.
3. Weight by **demeaned rank**: `w_H = k(z − z̄)⁺`, `w_L = k(z − z̄)⁻`, with
   `k = 2/Σ|z − z̄|` so each side sums to 1. (This is the same rank-weighting scheme as
   BAB, already described in this folder's momentum notes; it is a linear function of
   rank, not a bucket.)
4. Each side is levered to beta 1 at formation, and BAC(q) is long-low minus short-high.
   The factor is the equal-weighted average over the five volatility quintiles; the global
   factor is a cap-weighted average of country factors.

BAV is the same recipe with the sort order swapped: quintile on correlation first, then
split on volatility within.

**The conditional double sort is the diagnostic worth copying even if the factor is not.**
25 portfolios, volatility quintile × correlation quintile within it, checking first that
the ex-ante sort actually produces an ex-post spread in realised beta (it does, and
correlation and volatility produce spreads of similar magnitude — correlation is *not*
too noisy to sort on, which is the objection one would expect), and only then looking at
alpha. Within each volatility row the CAPM alpha **declines monotonically in correlation**,
and the low-correlation cells are on the positive side in every volatility quintile.

**Turnover.** The BAB-family factors turn over roughly six times more slowly than the
MAX/IVOL factors, because their inputs are estimated over one to five years rather than
one month, and because correlation and volatility are more persistent characteristics than
a monthly maximum. The paper makes this an explicit part of its horse race: when all
factors are put on equal-turnover footing, the systematic factors' advantage *widens*,
because the idiosyncratic factors derive much of their edge from a short-horizon effect.

## Robustness evidence (qualitative only)

- Multi-decade US sample and a broad multi-country developed-market sample; the
  correlation factor's result is present in both, and the authors describe the case for
  the systematic channel as *stronger* outside the US.
- Robust to substituting other correlation and beta estimators (including Fama–French
  1992-style betas); a cruder estimator shrinks the ex-post beta spread but not the
  significance of the effect.
- Survives the five-factor model plus short-term reversal, in both samples — though the
  authors argue, reasonably, that controlling for factors which their own theory predicts
  is too stringent a test.
- Double-sorted against an external mispricing measure: the correlation effect is present
  within every mispricing quintile, so it is not an idiosyncratic-risk or mispricing
  effect in disguise. Both channels appear to be live; neither subsumes the other.
- Economic-driver evidence: a margin-debt measure predicts the systematic factors and not
  the idiosyncratic ones; a sentiment measure predicts some idiosyncratic ones and not the
  systematic ones. This is a genuine, if indirect, test of the mechanism rather than
  another sort.
- **Known gap**: BAB-family factors are long-short and leverage-adjusted, and this repo's
  standing short-leg discount (`SUMMARY.md` #135–#137, 2026-09-22) applies with full force.
  The one piece of evidence *against* the discount being fatal here is the double-sort
  panel: the low-correlation cells carry positive CAPM alpha on their own in every
  volatility quintile, so the reachable side is not merely the less-negative side.

## Implementability here

**In scope.** Both inputs are functions of daily USD closes, which is all this repo needs.
No fundamentals, no intraday, no short interest. The rank-weighting scheme, the monthly
rebalance and the conditional double sort all map onto the existing engine.

**What it says about the champion's new term.** Trial #98 (2026-09-23) seated a
co-movement selector — `E/Var`, the share of a name's variance spanned by its four
closest substitutes — and measured the book's mean pairwise correlation falling 0.242 →
0.174 with concentration unchanged. BAC is the literature's version of the same bet
against a *different reference*: correlation to the **market** rather than to a
name-specific peer set. The two are not the same object and the repo has never measured
their relationship.

**Three concrete adaptations, in the order this file would run them.**

1. **The non-synchronous-trading correction, and it is free.** BAC estimates correlation
   from **overlapping three-day log returns** specifically because daily closes in
   different time zones are not contemporaneous. This universe spans 15 regions; the
   champion's `E/Var` term and every correlation the lab has printed are computed from
   **one-day** returns, which mechanically *understates* co-movement for every non-US
   name and understates it by a different amount per region. That is a bias in the seated
   champion's own signal, not a hypothetical. **Test: recompute `E/Var` (and the book's
   mean pairwise correlation) from 3-day overlapping log returns and compare the ranking,
   the ETF-versus-single-name separation (rank-AUC 0.815 on the current estimator) and
   the per-region means.** No trial, train only. If the ranking is materially unchanged,
   the lab has retired a live objection for nothing; if it changes, the champion's term is
   measuring the trading calendar as much as the economics.
2. **A market-correlation score as a distinct challenger leg** — one number per name,
   five-year window, no `n × n` matrix, long-only low-correlation side only, demeaned
   within instrument type (the 2026-09-22 rider: `E/Var` separates ETFs from single names,
   and a market-correlation score will separate them harder, since a broad ETF *is* mostly
   market). **Pre-register the orthogonality gates before building anything**, exactly as
   2026-09-22 did: `|ρ(score, 250d vol level)|` and `|ρ(score, rank 12−1)|` against the
   0.50 bar, plus — new, and specific to this family — `|ρ(score, β̂)|`. The last is the
   screen that matters here and the lab's standing one does not cover it: a low-ρ name can
   have perfectly ordinary volatility, so the volatility-level screen can pass while the
   score is simply a low-beta bet, which is a family this repo has already refused.
3. **The conditional double sort as a free diagnostic, ahead of any candidate.** Sort on
   volatility, then on the co-movement score *within* volatility quintile, and check that
   the ex-ante co-movement sort produces an ex-post spread in realised correlation with
   volatility held flat. This is the identification BAC is built on, it costs no trial, and
   it answers the question the lab will otherwise answer with a trial.

**Known pitfalls, and one of them is probably decisive.**

- **The size collision.** The paper states plainly that, holding volatility constant,
  low-correlation names *tend to be small, undiversified firms*, and BAC loads heavily on
  size. This universe is ~145 large global survivors. The cross-sectional dispersion in
  market correlation that BAC harvests is largely dispersion this universe does not
  contain. Expect a compressed spread, and do not import the literature's effect size —
  which this folder forbids anyway.
- **ETFs are not firms.** 42 of ~140 instruments are ETFs; a regional or sector ETF's
  correlation with a global market proxy is high nearly by construction, and its
  "low-correlation" cousins are the niche ones. Without a within-type demean the score is
  an ETF-versus-stock classifier.
- **The turnover argument cuts in this lab's favour** for once: a five-year correlation
  window is the slowest-moving signal this repo would have, and at 15 bps per side that is
  a real advantage over anything estimated on a one-month window.
- The factor's leverage-to-beta-1 step is unreachable here (gross ≤ 1.0, long-only). Drop
  it; it is a scaling device for a long-short factor, not part of the signal.

## Related

- `notes/2026-08-18-defensive-equity-replication-and-construction.md` — the skeptical case
  on the low-risk family (Novy-Marx; Novy-Marx–Velikov), which argues the defensive
  premium is size/profitability wearing a volatility costume. **Read together with this
  note.** That critique bites hardest on the *volatility* component, which is also the
  component this paper finds does not survive. It does not directly address a
  volatility-neutral correlation sort, which is what BAC is — but the size loading
  documented here is exactly the channel Novy-Marx points at, so the tension is real and
  unresolved rather than dissolved.
- `notes/2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` and the rest of the
  limits-of-arbitrage cluster — the short-leg discount that must be applied to any
  long-short effect size quoted here.
- `notes/2026-09-24-long-only-minimum-variance-composition.md` — what a long-only
  variance minimiser does with exactly these inputs, and why it is a membership rule on
  beta.
- `notes/2026-09-24-diversification-ratio-most-diversified-portfolio.md` — the portfolio
  whose objective *is* the correlation term, and the decomposition that separates it from
  concentration.
- `experiments/learnings.md` [2026-09-23] — the lab's own co-movement selection result,
  and [2026-09-17] / [2026-09-22] for the volatility-level survivorship artifact this
  note's screen #2 is designed to avoid re-running into.
