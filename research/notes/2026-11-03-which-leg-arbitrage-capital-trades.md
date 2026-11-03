---
title: "Arbitrage Trading: The Long and the Short of It"
authors: Chen, Da, Huang
year: 2019
venue: Review of Financial Studies 32(4), 1608–1646 (venue tier 1); advance article August 2018
url: https://doi.org/10.1093/rfs/hhy097 — typeset RFS advance article read in full from the second author's Notre Dame faculty page, `academicweb.nd.edu/~zda/NAT.pdf`
citations: 124 (Crossref `is-referenced-by-count`, checked 2026-11-03); 116 (OpenAlex, same date; OpenAlex misreports the publication year as 2015). Semantic Scholar returned HTTP 429 to every DOI call this session.
sample_period: 1990:Q1–2015:Q4 (quarterly); June 2006–March 2011 for the daily analysis
markets: US equities above the NYSE size breakpoint (small stocks excluded), 13F hedge-fund holdings and exchange-reported short interest
tier: A
validation_overlap: false
published_post_2018: true
---

Third source for the [2026-11-02] aim, and the one that satisfies its acceptance criterion
literally: *"admit a source only if it reports a long-leg-only or long-only-constrained
result."* This paper measures the long and the short side of arbitrage activity with
**different data on each side** and reports each one's return predictability separately, so
the reachable leg is a number rather than an inference.

Genuine zero before tonight: `Chen, Da` **0**, `Zhi Da` **0**, `net arbitrage trading`
**0** across 255 notes.

**Anti-lookahead note on what is deliberately omitted.** This paper has a substantial
crisis-period section (its Hypothesis 4, and a dedicated sub-period analysis) and several
statements of the form "this anomaly's returns were small during the later part of the
sample". **None of that is recorded here**, per `research/README.md`'s ban on event
narratives and period-attributed performance. Every figure below is a full-sample estimate.

## Mechanism

**The idea.** Arbitrageurs are the agents who correct mispricing, so *observing them trade*
should predict the correction. But the long and short sides of arbitrage leave traces in
different datasets — long positions in institutional holdings, short positions in short
interest — and each dataset alone is contaminated: hedge-fund buying is mixed with ordinary
long-only demand, and short interest is mixed with hedging. **Differencing the two cleans
both**, because a stock that arbitrageurs are buying *and* not shorting is the unambiguous
case. The economics the paper tests are the standard limits-to-arbitrage ones: arbitrageurs
are informed about mispricing; mispricing persists where limits to arbitrage bind; and
correction is gradual rather than instant.

**Why it is a statement about legs and not just about a signal.** The paper's organising
observation is that the *same* mispricing, in the *same* cross-section, is visible on two
sides that are not symmetric — different data, different frictions, different participants.
A long-only investor can act on one of them. So the paper's leg-level tables are, read
sideways, a measurement of the share of correctable mispricing that sits where a long-only
book can reach it.

**The result that matters most for this lab, and it is the opposite sign from the folder's
standing discount.** After a five-factor risk adjustment the **traded long leg alone is
significant**: among underpriced names (low mispricing score) that arbitrageurs are buying,
the daily alpha is **+0.017%** (t = 2.51) at a ten-day horizon, against **−0.021%**
(t = −2.69) for the traded short leg. The long leg therefore carries roughly **45%** of the
traded long-minus-short alpha of **0.038%/day** (t = 2.72) — a minority, as the folder's
discount says, but **not a lopsided minority and not a null.** The matching not-traded
portfolios are insignificant on both legs (long leg +0.008%/day, t ≈ 1.5; long-minus-short
0.013%/day, t = 1.37).

**The second result, which is a negative and binds this lab harder than the first.**
Replacing hedge-fund holdings with **general institutional ownership removes the return
predictability entirely.** The informative quantity is *who* is trading, not *how much*
trading there is. The paper's own framing is that hedge funds are the sophisticated subset
and other institutions are not.

## Construction recipe

Quarterly version:

1. `HF_i` = fraction of stock *i*'s shares outstanding held by hedge funds, from 13F filings
   of advisers identified as hedge-fund managers. `SI_i` = short interest as a fraction of
   shares outstanding, from exchange files (set to zero where absent).
2. **Abnormalise each against its own recent history**: `AHF` = current quarter's `HF` minus
   its average over the previous four quarters; `ASI` likewise for `SI`. This is a
   within-name change, not a cross-sectional level — the level is persistent and
   uninformative, the change is not.
3. `NAT = AHF − ASI`. Form quintiles at each quarter end; hold one quarter.
4. Exclude stocks below the NYSE size breakpoint.

Daily version (their Section 4, the one with the leg-level table):

- `AHF` at day *t* = linearly decayed sum of net hedge-fund buys over the past 30 days
  (weight 1 on day *t*, 29/30 on *t−1*, …, 1/30 on *t−29*).
- `ASI` at day *t* = short interest minus its average over the past 30 days, from daily
  securities-lending data.
- Rank both 1–100 across stocks each day; `NAT` = the **difference of the two ranks**. Quintile
  sort, hold 5 / 10 / 20 trading days. Exclude stocks priced under $5.
- Leg analysis: split on the median mispricing score, then within each half use the 20th and
  80th `NAT` percentiles; the "traded long leg" is low-mispricing × high-`NAT`.

Headline estimates (full sample): quarterly `NAT` high-minus-low excess return **0.73%/month**
(t = 8.56) in the first quarter after formation, **0.40%** (t = 4.43) in the second, **0.17%**
(t = 1.90) in the third, ~zero in the fourth, **with no long-run reversal** — which the
authors use to argue the effect is information rather than temporary price pressure.
Fama–MacBeth coefficients with ten characteristic controls: `AHF` **0.11** (t = 4.24), `ASI`
**−0.13** (t = −4.45), `NAT` **0.18** (t = 6.65). Conditioning the ten anomalies on being
arbitrageur-traded raises their average first-quarter quintile spread from **0.29%/month**
(t = 4.44) to **0.88%** (t = 7.95).

## Robustness evidence (qualitative only)

- **Causal identification, which is unusual in this literature.** The authors use
  Regulation SHO's randomised pilot — a genuine exogenous relaxation of short-selling
  frictions for a random subset of stocks — to show the predictability is stronger where
  limits to arbitrage bind. A random assignment is much stronger evidence than the
  cross-sectional proxies this effect is usually tested with.
- **Two frequencies, two datasets.** The quarterly 13F result is reproduced with daily
  securities-lending and trade data. The decay profile (three quarters, no reversal) is
  independently consistent with transaction-level institutional-trading evidence the authors
  cite.
- **Robustness reported:** including smaller stocks, excluding stocks with zero holdings or
  zero short interest, alternative scaling of `HF` and `SI`, a looser definition of
  "arbitrageur-traded", and sub-samples. The institutional-ownership substitution is reported
  as a *failure*, which is the right way round.
- **Honest gaps.** (i) **Transaction costs are not modeled anywhere** — every magnitude above
  is gross, and a quarterly-rebalanced quintile book on US stocks is not cheap. This is the
  fourth consecutive session in which the night's main source does not cost its own strategy.
  (ii) **No multiple-testing adjustment**; the ten anomalies and the mispricing composite are
  taken from prior work rather than searched, which mitigates but does not remove it.
  (iii) The effect is a **conditioning** result — it tells you where anomaly returns are, not
  that `NAT` is a standalone tradable alpha net of costs. (iv) 13F data arrive with a
  reporting delay of ~45 days, which the authors note makes their quarterly result
  conservative but also means a real-time implementation is not the one they measure.
- **Tier A** on venue (RFS), citation count (124 Crossref) and identification, with the cost
  omission flagged.

## Implementability here

**Not implementable, and the reason is not a detail.** The signal requires 13F institutional
holdings and securities-lending/short-interest data. This lab has daily OHLCV only. There is
no construction in this note.

**What it is for, in three parts.**

**1. It weakens — and does not overturn — this folder's standing long-only discount.** The
folder's strongest discount comes from `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md`
(Stambaugh–Yu–Yuan): the short leg carries most of an anomaly's abnormal return, so a
long-only book should expect the minority share. This paper is the first source here that
**measures the reachable leg on its own and finds it significant** — about 45% of the traded
spread, five-factor-adjusted, t = 2.51. The honest revision is therefore the same shape as
the [2026-11-02] documentation correction: **the gradient runs against the long leg, but the
long leg is not a null.** A long-only null remains weaker evidence against an effect than a
long–short null would be; it is not *no* evidence.

**2. The obvious price-only proxy is already refuted here, and this paper explains why — so
the lab's null is a confirmation, not a tension.** The natural reachable adaptation is to
condition a long-only book on abnormal volume or a volume shock, as a proxy for informed
capital arriving. `experiments/learnings.md` records that whole axis as a null on clean
instruments across twelve sessions (volume shock 21d **−0.0038**, 63d −0.0021, turnover
trend −0.0041, volume dispersion +0.0000). **This paper predicts exactly that outcome**: its
institutional-ownership substitution test shows that replacing the *identity* of the trader
with a broader measure of trading destroys the predictability. Volume is an even broader
measure. So the mechanism is **structurally unreachable on price-only data** rather than
untested, and no session should spend a trial on a volume-conditioned re-test of it on the
strength of this paper. Record it that way: the lab's measured null and this paper's reported
null are the same finding from two directions.

**3. One free interpretation rule the lab can use tonight, at no cost.** The paper's
anomaly-conditioning result says the long-leg return of a published anomaly is concentrated
in a minority subset of its long portfolio that cannot be identified from prices. The
consequence for hypothesis writing is specific: **when a candidate's motivation is a
published cross-sectional anomaly, the reachable quantity is not the published long-leg
return but the long-leg return averaged over the whole band, including the majority of names
where the correction does not happen.** That is a second, independent haircut stacked on top
of the long-only one — and it should be stated in the hypothesis line rather than discovered
in the trial. Two cautions on using it: it is a *discount*, not a screen (there is no
price-only way to identify the traded subset), and it must not be stacked naively with the
Stambaugh–Yu–Yuan discount, since both are partly measuring the same thing — the same
caution as `#362`.

## Related

- `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md` — the discount this note
  partially softens.
- `notes/2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` — Stambaugh–Yu–Yuan's arbitrage
  asymmetry: *why* the short side carries more. This paper's mispricing composite (`MISP`) is
  that paper's measure, so the two are directly linked and the overlap should be remembered
  when the discounts are combined.
- `notes/2026-11-03-attainable-underweight-and-the-long-only-constraint.md` and
  `notes/2026-11-03-no-short-constraint-cost-and-panel-breadth.md` — tonight's other two:
  the same question asked in weights and in attainable Sharpe rather than in measured returns.
- `notes/2026-09-07-high-volume-return-premium.md` and `notes/2026-08-31-amihud-volume-component-decomposition.md`
  — the volume-based mechanisms the lab screened to a null, and which this note explains
  should not be revisited as a proxy for this effect.
- `experiments/learnings.md` (2026-10-24/25) — the twelve-session `liquidity-volume` null
  that part 2 above reinterprets as agreement with this paper rather than tension with it.
