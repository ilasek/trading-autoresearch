---
title: "The Liquidity-Adjusted CAPM — three liquidity betas, and their collinearity with the level"
authors: Acharya, Pedersen
year: 2005
venue: Journal of Financial Economics 77(2), 375–410 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1016/j.jfineco.2004.06.007
citations: "2919 (Semantic Scholar by DOI, checked 2026-09-29); 2107 (Crossref by DOI, same
  date). The Semantic Scholar record carries an empty `venue` field for this DOI while
  resolving the title and count correctly — worth knowing before trusting that field anywhere."
sample_period: 1962/1963–1999 (monthly, from daily CRSP data)
markets: US only — NYSE and AMEX common shares, sorted into 25 illiquidity portfolios
tier: A
validation_overlap: false
published_post_2018: false
---

**Read in full** as the published JFE article (36 pp., typeset version of record served by
`cis.upenn.edu`), cross-checked against NBER Working Paper 10814 (September 2004) for the
appendix. Both parsed cleanly. The equations quoted below are from the published text.

This is the second of tonight's two notes on the liquidity-*risk* channel that
`notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` and
`notes/2026-09-04-commonality-in-liquidity-across-countries.md` each explicitly set aside as an
unopened literature. It is the theory-grounded member of the pair: where
`notes/2026-09-29-liquidity-risk-priced-innovations.md` starts from a measure and asks whether
its beta is priced, this one derives what *should* be priced from an equilibrium model and then
tests the restriction. **Its most useful output for this lab is a negative one, and it is stated
by the authors themselves: all three liquidity risks are strongly collinear with the illiquidity
LEVEL.** This lab closed the level channel on a direct measurement.

## Mechanism

**The model.** Risk-averse agents in an overlapping-generations economy trade securities whose
illiquidity `c_i` (a per-share cost of selling) varies randomly over time. Solved explicitly,
the model yields a CAPM in which the required return on a security rises in **(a)** its expected
illiquidity `E(c_i)` and **(b)** its *net* beta — the covariance of its illiquidity-net return
`r_i − c_i` with the market's illiquidity-net return `r_M − c_M`, scaled by the variance of the
latter. The first term is the static Amihud–Mendelson channel: illiquid assets must
compensate holders for expected trading costs. The second is the new content.

**The decomposition, which is the whole point.** The net beta splits into the ordinary market
beta plus three distinct liquidity risks:

    E(r_i) − r_f  =  E(c_i)  +  λ·( β1 + β2 − β3 − β4 )

with (all covariances scaled by `var(r_M − c_M)`):

- `β1 = cov(r_i, r_M)` — ordinary market risk.
- `β2 = cov(c_i, c_M)` — **commonality in liquidity**. A security whose own trading cost rises
  when everyone's does is worse to hold: you pay the cost exactly when it is highest. Positive
  premium.
- `β3 = cov(r_i, c_M)` — **return sensitivity to market illiquidity**. A security that pays off
  when market illiquidity spikes is a hedge against the bad state, so it is *cheap* to hold:
  it earns **less**. Enters with a minus sign.
- `β4 = cov(c_i, r_M)` — **liquidity sensitivity to market returns**. A security whose own cost
  of selling rises when the market falls is worse to hold, because that is when you may need to
  sell. Enters with a minus sign (the covariance itself is typically negative, so the
  contribution to required return is positive).

The signs are the economics, and they are what a naive "liquidity risk" score gets wrong:
`β3` and `β4` are *rewarded in opposite directions from* `β2` in raw covariance terms, and only
the combination `β1 + β2 − β3 − β4` is the priced object. The model has one free parameter
(`λ`), the same single degree of freedom as the standard CAPM.

## Construction recipe

**Step 1 — per-name illiquidity from daily data.** The paper instruments the unobservable cost
`c_i` with Amihud's ILLIQ:

    ILLIQ_it = (1/Days_it) · Σ_d |R_id| / (dollar volume)_id

**Step 2 — normalise it into cost units and cap it.**

    c_it = min( 0.25 + 0.30 · ILLIQ_it · P^M_{t−1} ,  30.00 )   [percent]

where `P^M_{t−1}` is the ratio of the market portfolio's capitalisation at the end of month
`t−1` to its capitalisation in the series' first month. Two things are happening here and both
matter: the `P^M` factor makes the series **stationary** in the face of secular growth in dollar
volumes (the same problem the `m_t/m_1` scaling solves in the Pástor–Stambaugh construction),
and the affine `0.25 + 0.30·` calibration puts the measure on the scale of an effective
half-spread, which is what licenses reading `c` as a per-trade cost at all. The 30% cap is an
explicit outlier control.

**Step 3 — work at the portfolio level, not the name level.** The paper forms 25
illiquidity-sorted portfolios and computes all four betas on *portfolio* series. This is not
presentational: individual-name liquidity betas are too noisy to sort on, which is the same
problem the other note's step 6 tries to solve with predicted betas. Portfolio illiquidity is
the weighted average of member `c_it`, with the un-normalised member values truncated at the cap
before averaging.

**Step 4 — illiquidity innovations, from an AR(2).** Market illiquidity is highly persistent
(the paper reports first-order autocorrelation near 0.9 at monthly frequency), so the betas must
be computed on *innovations*. Predict market illiquidity with

    c^M_t  =  a0 + a1·c^M_{t−1} + a2·c^M_{t−2} + u_t

taking the residual `u_t` as the innovation `c^M_t − E_{t−1}(c^M_t)`. **Construction detail worth
copying:** the *same* `P^M_{t−1}` date is used in all three terms, so that the regression
measures innovations in illiquidity and not changes in the market-size deflator. Portfolio-level
innovations are computed the same way with the same specification. The authors report the
results are robust to the innovation specification, and note it is similar in spirit to
Pástor–Stambaugh's.

**Step 5 — price it.** Estimate the four betas from monthly series, form
`β_net = β1 + β2 − β3 − β4`, and test the one-parameter restriction cross-sectionally against
the unrestricted four-lambda alternative.

## Robustness evidence (qualitative only)

- **The restriction does better than the standard CAPM on the same degree of freedom**, judged
  by cross-sectional `R²` and specification-test p-values, on portfolios sorted by illiquidity,
  by illiquidity variation, and by size. It **cannot** explain the book-to-market effect.
- **The collinearity finding, which the authors foreground and which is the reason this note
  matters here.** A security with high average illiquidity `c_i` also tends to have high `β2`,
  and large-magnitude (negative) `β3` and `β4`. In their words, illiquid securities also *have*
  high liquidity risk — consistent with flight-to-liquidity — and this collinearity
  "complicates the task of distinguishing statistically the relative return impacts of
  liquidity, liquidity risk, and market risk." The reported correlation between `β3` and `β4`
  across the test portfolios is high (≈0.73). There is, they say, *some* evidence that the total
  effect of the three liquidity risks matters over and above market risk and the liquidity
  level — which is a careful way of saying the decomposition is not cleanly identified in the
  data.
- **The two literatures are measuring different things.** The paper reports that the
  correlation between its market illiquidity innovation and the Pástor–Stambaugh aggregate
  liquidity innovation is only about −0.33 (the negative sign is expected: one series is
  liquidity, the other illiquidity). Two Tier 1 constructions of "the aggregate liquidity state"
  share roughly a tenth of their variance. Do not treat either as *the* liquidity factor.
- **Single market, single sample, no out-of-sample country evidence**, and no commissioned
  replication of the kind the companion note has. Costs are the *subject* rather than a modelled
  friction: the tests are on gross returns, with the illiquidity level entering as a
  characteristic.

## Implementability here

**Reachable.** Steps 1–4 need only `|R|`, `dollar_volume` and a market aggregate — all in `aux`.
ILLIQ is already implemented in this repo's history (`lv_illiq_*` candidates), so the marginal
work is the `P^M` deflator, the AR(2) innovation series, and the covariances.

**The three reasons this folder does not rank a candidate from it highly.**

1. **The authors' own collinearity result predicts this lab's existing null.** `learnings.md`
   [2026-09-24] closed `liquidity-volume` on the mean channel using an illiquidity-*level*
   score: `F₁` nowhere near rejecting, appraisal ratio +0.078/yr, and the best hindsight blend
   weight moving the tangency Sharpe by +0.0028. If, as this paper reports, `β2`, `β3` and `β4`
   are each strongly collinear with `E(c)`, then a book sorted on any of them is a *noisier*
   version of the score that already produced that null. The lab's own vocabulary for this is
   exact: it would be the level channel in costume, the fourth instance of a pattern
   `learnings.md` [2026-09-27] already records three of.
2. **Any honest test therefore has to be of the orthogonalised part**, and the lab has closed
   the `neutralize` operator on evidence (`learnings.md` [2026-09-12]). A pre-registered
   orthogonality screen against the existing ILLIQ score (the shape of `learnings.md`
   [2026-09-22]) is the *minimum* precondition, and the prior should be that it fails — on a
   139-name panel the residual of a noisy beta after removing a noisy level is mostly noise.
3. **`β_net` needs a sign convention no score-blending shortcut will give you.** `β2 − β3 − β4`
   is not "average the three liquidity risks"; two enter negatively. A candidate that
   rank-averages three liquidity-risk scores is testing a different model from this one, and
   should not cite this paper.

**What it is worth, concretely.** Two things, both free:

- **A construction correction for anything this lab builds from a persistent panel
  characteristic.** Steps 2 and 4 together are a reusable recipe: deflate a dollar-denominated
  characteristic by a market-size ratio to make it stationary, then take AR innovations with the
  deflator *held at one date* so the innovation is in the characteristic and not in the
  deflator. This lab has built several scores from ILLIQ levels and from volume; whether any of
  them accidentally rode a secular volume trend is a free diagnostic.
- **A statement of what "liquidity risk" would have to be to be new here.** Not a sorted book:
  a *state variable* whose innovations are orthogonal to the level score and to market returns.
  The paper's own numbers say that object is small.

## Related

- `notes/2026-09-29-liquidity-risk-priced-innovations.md` — the companion, its commissioned
  replications, and the ten-of-ten non-significant premium result. Read the two together: this
  paper says the risk betas are collinear with the level, and that one says the premium on the
  measure-based beta does not survive construction variation.
- `notes/2026-09-29-funding-liquidity-and-margin-spirals.md` — the mechanism that generates
  `β2`: a single funding state variable driving all names' costs at once.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — ILLIQ itself, the level
  channel, and its replication record.
- `notes/2026-09-04-commonality-in-liquidity-across-countries.md` — commonality measured
  directly, and the warning that ILLIQ levels are not comparable across countries, which bears
  on step 2's affine calibration in a 15-region universe.
- `notes/2026-09-22-limits-of-arbitrage-performance-based.md`,
  `notes/2026-09-22-arbitrage-risk-substitute-portfolios.md` — the other channel by which a
  funding/arbitrage-capacity story reaches expected returns, and the one the lab's seated
  champion already uses.
