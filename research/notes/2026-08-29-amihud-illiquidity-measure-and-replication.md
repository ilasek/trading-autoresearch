---
title: "Amihud's ILLIQ: the original, its commissioned replication, and the author's reply"
authors: Amihud (2002); Harris, Amato (2019); Amihud (2019)
year: 2002 / 2019 / 2019
venue: Journal of Financial Markets 5(1), 31–56 (tier 1); Critical Finance Review 8(1–2), 173–202 (tier 1–2, a journal whose stated purpose is commissioned replication); Critical Finance Review 8(1–2), 203–221
url: https://doi.org/10.1016/S1386-4181(01)00024-6 · https://doi.org/10.1561/104.00000058 · https://doi.org/10.1561/104.00000073
citations: Amihud 2002 — 6073 (Semantic Scholar DOI endpoint, checked 2026-08-29); Harris–Amato 2019 — 27 (Crossref `is-referenced-by-count`, checked 2026-08-29); Amihud 2019 — 43 (Crossref, checked 2026-08-29)
sample_period: Amihud 2002 — 1963–1997; Harris–Amato — 1963–1997 replicated, extended to 2015; Amihud 2019 — 1964–2017 (Period I 1964–1997, Period II 1998–2017)
markets: NYSE (Amihud 2002) / NYSE–AMEX common stocks (Amihud 2019); Harris–Amato use the current CRSP version of the same universe
tier: A (the cluster; the 2002 paper alone would be A, and the commissioned replication is what makes the cluster unusually well-evidenced in both directions)
validation_overlap: false
published_post_2018: true (for the two 2019 papers; the 2002 original is pre-2018)
read: full text for all three — Amihud 2002 from `cis.upenn.edu/~mkearns/finread/amihud.pdf` (the typeset JFM article with journal header and pagination); both CFR papers from the journal's own author-editor mirror `cfr.ivo-welch.info/published/papers/`
---

## Mechanism

**Why illiquidity should be priced.** A stock that costs more to trade must offer a higher gross
expected return for an investor to hold it — the Amihud–Mendelson (1986) clientele argument. The
measure `ILLIQ` is a proxy for the *price impact* half of that cost: the average daily percentage
price move per dollar traded, which is Kyle's λ estimated from daily data instead of from
transactions. Amihud validates the proxy directly, regressing `ILLIQ` cross-sectionally on
intraday-estimated Kyle λ and the fixed bid-ask cost component and reporting a strong positive
relation.

**Why the measure exists in this form at all** — Amihud's own account in the 2019 reply, and the
most useful sentence in the cluster for a lab constrained to daily data. It "was developed out of
necessity": at the time, effective spreads and Kyle's λ could be computed from intraday data for
about 13 years, while `ILLIQ` could be computed from daily CRSP data for 34. **It is a long-history
substitute for a better measure, not a better measure.** Amihud says so; the replication tests it.

**The second, less-copied half of the 2002 paper.** The cross-sectional result was not new even in
2002 (Amihud says so explicitly — it repeats Amihud–Mendelson 1986). The new result was the
*time-series* one: aggregate market illiquidity is highly autoregressive, so an increase in it is
expected to persist, which raises subsequent expected returns and therefore **lowers prices now**.
Realised returns are negatively related to contemporaneous *unexpected* illiquidity, and that
sensitivity is greater for smaller, less liquid stocks — which is the seed of the
illiquidity-*risk* literature (Pástor–Stambaugh 2003, Acharya–Pedersen 2005) rather than the
illiquidity-*level* one. A cross-sectional ILLIQ sort captures the level story only.

## Construction recipe

**`ILLIQ` (Amihud 2002, eq. 1).** For stock `i` in year `y`:

    ILLIQ[i,y] = (1/D[i,y]) * sum over days d of ( |R[i,y,d]| / VOLD[i,y,d] )

where `R` is the daily return and `VOLD` the **dollar** volume that day. Note the shape: it is the
**mean of the daily ratios**, not the ratio of the means. (Whether that distinction matters is the
replication's central question — see below.) Amihud multiplies by 10⁶ for readability. The annual
value from year `y` is used to explain returns in year `y+1`.

**Screens, which are a substantial part of the recipe.** Amihud 2002 requires: return *and volume*
data for **more than 200 days** in the prior year, and the stock listed at year end; end-of-year
price **above $5** (tick-size noise); market-capitalisation data available (this is what excludes
ADRs and derivative securities); and stocks in the **top and bottom 1% of the `ILLIQ` distribution
dropped as outliers**. Between 1,061 and 2,291 stocks survive in any year. The 2019 reply adds the
day-level screens the 2002 paper handled less explicitly: delete stock-days with a negative price
(a negative price on CRSP flags a bid-ask midpoint rather than a trade), with **volume under 100
shares**, or with a return below −100%; delete the **single highest daily `ILLIQ` value each year**;
require price between $5 and $1,000; and use the 12 months **ending in November**, so the signal is
lagged before it is used.

**The IML factor (Amihud 2019), and the construction detail that matters most here.** Because
`ILLIQ` and return volatility are **positively correlated** — the numerator is an absolute return —
an unconditional `ILLIQ` sort is partly a volatility sort. Amihud's factor construction therefore
sorts **volatility first**:

1. Sort stocks into **three portfolios by `SD`**, the standard deviation of daily returns over the
   same trailing 12 months.
2. **Within each volatility tercile**, sort into **five portfolios by `ILLIQ`** → 15 portfolios.
3. Each portfolio is **capitalisation-weighted** using the previous month's market caps, and
   re-sorted annually using November-ending inputs while portfolios are formed each month.
4. `IML` = average return of the three high-`ILLIQ` quintiles minus the average return of the three
   low-`ILLIQ` quintiles, i.e. **the illiquidity spread taken at held-constant volatility**.

Amihud says he double-sorts "because these two variables are positively correlated, each having its
own effect on expected returns", following the Fama–French HML construction for the same reason.
**This is the single most transferable line in the cluster for this lab.**

## Robustness evidence (qualitative only)

**The replication (Harris–Amato, commissioned by the journal, replication data published).**

1. **The original replicates.** Using the current CRSP version and Amihud's own definitions,
   filters and footnoted details, the results are "quantitatively very close and qualitatively the
   same". The authors note small differences but "none that causes us to question the integrity of
   the published study". By the folder's rubric this is about as good as a replication verdict gets.
2. **The effect decays out of the original sample.** Applying the same methods to the data after
   Amihud's sample ends, the cross-sectional relation between illiquidity and returns is much
   weaker, and in the time-series analysis **only the *unexpected* component of illiquidity remains
   related to index returns**, where the original found both expected and unexpected components
   priced. Harris–Amato cite Ben-Rephael–Kadan–Wohl (2015), who independently report a declining
   liquidity premium over four decades. This is a textbook McLean–Pontiff-shaped result and should
   be read against `2026-08-17-mclean-pontiff-publication-decay.md`.
3. **`ILLIQ` is not better than much simpler measures built from the same two data series.** In a
   horserace against alternatives computable from daily returns and volume alone — the **ratio of
   mean |return| to mean dollar volume**, mean |return| alone, inverse mean volume, **log mean
   dollar volume**, and the Kyle–Obizhaeva invariance measure (cube root of return variance over
   average dollar volume) — Amihud's measure has among the *lowest* average R² in every subgroup
   and both specifications, though its t-statistic is consistently among the highest. The best
   proxies by average R² are the **invariance measure and log average dollar volume**.
4. **And the daily pairing contributes nothing.** The ratio of means is ~92% cross-sectionally
   correlated with `ILLIQ` and delivers essentially identical coefficients, t-statistics and R².
   Replacing `ILLIQ` with the ratio of means plus *the difference between the two* shows that
   almost all explanatory power sits in the ratio of means. The authors' conclusion: "almost all
   the explanatory power of Amihud's illiquidity measure is due to its ability to characterize the
   ratio of the two means and not to the correlation of absolute daily returns with daily trading
   volumes" — **which is precisely the feature Amihud's motivation rests on.** Lou–Shu (2017, RFS)
   are cited as reaching a similar conclusion.
5. **A warning about the numerator.** Taken alone, mean absolute return enters with a *negative*
   and often insignificant coefficient, and Harris–Amato call this "simply a re-identification of
   the low-volatility effect" — it loses significance once return standard deviation is a control.
   So the |return| numerator is a volatility proxy first and a liquidity proxy second.

**The author's reply (Amihud 2019).** Amihud does not contest the replication. He constructs `IML`
over 1964–2017 and reports it as positive and significant risk-adjusted over the full span, **lower
in the period after his 2002 paper but still positive and significant**, with the predicted response
to market-illiquidity shocks intact. He also re-states the point the cross-sectional literature
usually drops: the *risk* channel (covariance with illiquidity shocks) is a separate and
independently priced thing from the *level* channel, and small illiquid stocks carry more of it.
Reading the exchange as a whole: the level effect survives as a smaller, volatility-controlled
factor; the specific functional form of `ILLIQ` does not survive as uniquely informative.

**Where this cluster stands on the rubric.** Multi-decade (1963–2017 across the three papers),
single market (US), costs not modelled in any of the three, multiple testing not addressed, but
**independently replicated with published data and with an author reply in the same issue** — a
combination almost nothing else in this folder has.

## Implementability here

The lab has already run one `liquidity-volume` scout: a single sort on trailing-quarter Amihud
`ILLIQ`, recorded as `FAMILY_LEAD` at 1.0× annual turnover and the most decorrelated non-trivial
result the lab holds. This cluster says four specific things about what to do next, and one of
them is a caution about that result.

- **The single sort is confounded with volatility, and the literature's own fix is one line.**
  Amihud sorts on `SD` first and takes the `ILLIQ` spread *within* volatility terciles, for exactly
  the reason that applies here. This lab has separately refuted low-vol tilts on this universe
  (`learnings.md`), which makes the confound consequential in both directions: an unconditional
  `ILLIQ` sort might be *helped* by an unintended volatility tilt or *dragged* by one, and the
  existing scout cannot tell which. **The cheapest informative next trial in this family is the
  volatility-conditional version of the sort the lab has already run** — same signal, sorted within
  trailing-volatility terciles — because it is the one variant that separates the two effects
  rather than adding a knob. This is not a parameter sweep; it is a decomposition.
- **Test whether the signal is really just dollar volume.** Harris–Amato find log mean dollar
  volume among the best proxies and the daily |R|/volume pairing worthless, and Amihud's own reply
  does not rebut it. This repo receives `dollar_volume` directly in the `aux` panel. A sort on
  **log mean dollar volume** (or on the ratio of mean |return| to mean dollar volume) is trivially
  cheaper to compute, much smoother, and — on the replication's evidence — should perform at least
  as well. If it does, the family's real signal is a size/activity proxy, not price impact, and
  the lab should say so; if it does not, that is a genuine disagreement with a tier-1 replication
  and worth recording as such.
- **Port the screens, adapted.** The `$5` price floor, the 200-day data requirement and the
  `ILLIQ` outlier trim are not decoration — they are how the measure is kept from being dominated
  by tick noise and near-zero-volume days. Two of them transfer directly and matter more here than
  in CRSP: **volume is not forward-filled in this repo's panel and is NaN on foreign holidays**, so
  a naive `|R|/dollar_volume` on a 15-region universe will produce spurious infinities on every
  foreign holiday. Amihud's day-level screens (drop days with volume under 100 shares; drop the
  single largest daily `ILLIQ` each year) are the literature's own answer to that failure mode.
  The `$5` floor has no analogue on an ETF-heavy adjusted-close universe and should be dropped
  rather than transplanted.
- **Expect decay, and treat the flags as live.** The cross-sectional effect is documented as
  materially weaker after the original sample, by both the replication and an independent citation.
  Whatever this family's leaderboard entry is worth, the literature's prior is that it is worth
  *less* than the original paper's magnitude, not more. Nothing here licenses a performance
  expectation, and `CLAUDE.md` forbids importing one anyway.

**Known pitfalls specific to this repo.** (a) `ILLIQ` is a level in units of return-per-dollar and
its cross-sectional distribution is extremely right-skewed and scale-dependent; rank-transform it
cross-sectionally before use (cf. `2026-08-29-machine-learning-cross-section-comparative.md`), never
threshold it on a raw value. (b) The universe is 42 ETFs and ~100 large global stocks — the
illiquid tail of CRSP that carries this effect does not exist here, so the reachable spread is
between "liquid" and "slightly less liquid" and should be expected to be compressed. (c) Volume is
a **share count in native units**; `dollar_volume` is the close-in-USD times that count, so the
denominator is already currency-consistent, but the *share* count is not comparable across
instruments and must never be used unnormalised. (d) Survivorship bias interacts badly with this
family: today's constituents are the survivors, and illiquidity is a survival hazard, so a
long-only illiquidity tilt on a current-constituent universe is exactly the construction
`2026-08-26-survivorship-conditioning-and-spurious-persistence.md` warns about.

## Related

- `2026-08-29-machine-learning-cross-section-comparative.md` — ranks liquidity as the
  **second** most informative feature group after price trends, and lists Amihud `ILLIQ`, dollar
  volume, turnover and zero-trading-days as members. The two notes agree that the group matters and
  disagree about whether this particular member is the right representative of it.
- `2026-08-17-short-term-reversal-as-liquidity-provision.md` — the other side of the same coin:
  short-horizon reversal as compensation for supplying liquidity rather than for holding illiquid
  assets.
- `2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — why an illiquidity tilt is
  the family most exposed to this repo's permanent data caveat.
- `2026-08-27-live-execution-costs-implementation-shortfall.md`,
  `2026-08-27-market-impact-functional-form-and-trade-rate.md` — price impact measured from actual
  fills, i.e. the quantity `ILLIQ` is a daily-data proxy *for*.
- `2026-08-17-mclean-pontiff-publication-decay.md` — the frame for the replication's decay finding.
