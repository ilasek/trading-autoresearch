---
title: "Winter Blues: A SAD Stock Market Cycle — the daylight mechanism for the six-month seasonal, and its refutation"
authors: Kamstra, Kramer, Levi (read in full); Jacobsen, Marquering (critique, abstract only)
year: 2003; 2008
venue: American Economic Review 93(1), 324–343 (Tier 1, peer-reviewed); Journal of Banking and Finance 32(4), 526–540 (Tier 1/2, peer-reviewed)
url: https://doi.org/10.1257/000282803321455322 ; https://doi.org/10.1016/j.jbankfin.2007.08.004
citations: "Kamstra–Kramer–Levi: 858 (Crossref `is-referenced-by-count`, checked 2026-10-04); 1103 (OpenAlex, checked 2026-10-04). Jacobsen–Marquering: 152 (Crossref) / 181 (OpenAlex), checked 2026-10-04."
sample_period: "Kamstra–Kramer–Levi: daily index returns, per-index start dates from 1928 (S&P 500) to 1991 (New Zealand), all ending 2000–2001. Jacobsen–Marquering: not read, not recorded."
markets: "Kamstra–Kramer–Levi: 12 indices in 9 countries — United States (S&P 500, NYSE, NASDAQ, AMEX), Sweden, Britain, Germany, Canada, Japan (Northern Hemisphere); New Zealand, Australia, South Africa (Southern Hemisphere). Latitudes 26°S to 59°N."
tier: "A for the primary on venue and citations, **downgraded in use to B** — not for its execution but because an independently-published Tier-1/2 critique of it, in the same literature, concludes its explanatory claim is likely spurious, and because the primary's own tests are one-sided and its strategy illustration explicitly neglects transaction costs. The critique was read as an abstract only and is used only for the claim its abstract makes."
validation_overlap: false
published_post_2018: false
---

## Access

**The primary was read in full, from a new channel.** `utoronto.scholaris.ca` (University of
Toronto's DSpace, the second author's institution) served the **typeset published AER PDF** on the
first try at HTTP 200 — a 459 KB, 9-page two-column file that parses cleanly with `pdftotext
-layout`. This is the [2026-10-03] "author's institutional library" lesson landing at a second
university and it is now worth treating as a standing route: **for any closed article, read
OpenAlex's `locations[].landing_page_url` list and try the co-authors' institutional repositories
before anything else.** OpenAlex listed two green locations for this DOI; the other one failed (next
paragraph), so trying both mattered.

**`econstor.eu` has gone behind Anubis and `research/README.md` is now wrong about it.** OpenAlex's
first green location was `econstor.eu/bitstream/10419/100871/1/wp2002-13.pdf` (the Federal Reserve
Bank of Atlanta working-paper version). It returned **HTTP 200 with a 7.9 KB
`Making sure you're not a bot!` body** served from `/.within.website/x/xess/` — Anubis, the
same software recorded at Frankfurt [2026-09-30] and AUEB [2026-10-03], now at a host the README
(2026-09-07 entry) still calls "a reliable channel and worth trying early". **Third Anubis host, and
the first that reverses a documented-good channel.** Note the failure mode once more looks like an
answer: HTTP 200, a file written to disk, and `file` reporting HTML rather than PDF is the only tell.

**The critique is closed and was read as an abstract only.** `10.1016/j.jbankfin.2007.08.004`:
Unpaywall `is_oa: false`, OpenAlex `oa_status: closed` with `any_repository_has_fulltext: false` and
only two `pure.eur.nl` records in its `locations` list. **Erasmus Pure served the complete publisher
abstract at HTTP 200**, which is the [2026-10-02] bepress-landing-page lesson generalised: a Pure
record is a reliable abstract source for a closed Elsevier article. Everything attributed to the
critique below is from that abstract, is flagged, and no methodological detail of it is claimed.

**One more host closed tonight: the ETH Research Collection.** `doi.org/10.3929/ethz-a-010689622`
redirected to `research-collection.ethz.ch/handle/20.500.11850/118883` and returned **HTTP 500**; its
DSpace REST endpoints returned **401** (`/server/api/core/items`) and **403**
(`/server/api/discover/search/objects`). Three distinct error classes from one host in one minute, so
this is a server/policy problem rather than a rate limit, and the KOF working paper behind it is
recorded as unread in `2026-10-04-us-leads-the-world-country-lead-lag.md`.

## Mechanism

This is the one developed economic mechanism in the literature for the six-month seasonal documented
in `2026-10-04-halloween-six-month-seasonal.md`, and its chain has three links, each of which the
authors source to an outside literature rather than assert:

1. **Seasonal affective disorder tracks hours of daylight.** Clinical evidence links depressive
   episodes to the fall and winter seasons of relatively short days, with severity increasing with
   latitude.
2. **Depression lowers risk tolerance.** Experimental psychology links depressed mood to reduced
   risk-taking, including in financial settings.
3. **Therefore a representative holder's required return varies with the length of the night.** When
   the marginal trader is more risk-averse, prices are lower and subsequent returns higher; the
   seasonal cycle in daylight translates into a seasonal cycle in expected returns.

**The mechanism's distinguishing content is not the calendar — it is the two cross-sectional
predictions the calendar cannot make.** (a) A **latitude gradient**: markets further from the equator
should show a stronger effect, because their daylight swing is larger. (b) A **hemisphere flip**: the
effect should be *six months out of phase* in the Southern Hemisphere, because fall and winter are.
Both are stated in the paper's own abstract as the compelling part of its evidence. **Any
implementation that does not test (a) or (b) is not testing this mechanism**, it is testing a calendar
dummy, and the two have different implications here.

The paper also builds in an **asymmetry around the winter solstice**, on two grounds: the clinical
literature reports the depressive effect is asymmetric around the solstice, and if SAD-affected
holders are themselves trading, the onset of fall and the recovery through winter should move prices
at different times. Operationally this becomes a separate fall dummy, and the authors report the
combination of a positive daylight coefficient and a negative fall coefficient means the effect is
**shifting returns from the fall into the winter** rather than creating them.

## Construction recipe

Everything needed to build the signal is here; it needs latitude and a calendar and nothing else.

**Hours of night.** For latitude `δ` and day-of-year `julian_t ∈ [1, 365]`:

    λ_t = 0.4102 · sin( (2π/365) · (julian_t − 80.25) )                  # solar declination angle
    H_t = 24 − 7.72 · arccos( −tan(2πδ/360) · tan(λ_t) )                 # Northern Hemisphere
    H_t =      7.72 · arccos( −tan(2πδ/360) · tan(λ_t) )                 # Southern Hemisphere

**The SAD regressor.** `SAD_t = H_t − 12` on trading days in **local** fall and winter, `0` otherwise,
where local fall/winter is September 21 – March 20 in the North and March 21 – September 20 in the
South. Subtracting 12 normalises against the annual mean night length at any latitude, so the variable
is 0 at each equinox, peaks at the local winter solstice, and is identically 0 through local spring and
summer. Its peak is **mechanically larger at higher latitude** — the paper's worked example is +6 at
Stockholm's 59°N — which is how the latitude gradient enters without a separate interaction term.

**The regression actually estimated** (one per market, daily, coefficients free to differ by market):

    r_t = μ + ρ₁r_{t−1} + ρ₂r_{t−2} + μ_Mon·D_Mon + μ_Tax·D_Tax + μ_SAD·SAD_t + μ_Fall·D_Fall
          + μ_Cloud·Cloud_t + μ_Precip·Precip_t + μ_Temp·Temp_t + ε_t

with lags added only as needed to clear residual autocorrelation and heteroskedasticity-robust
(MacKinnon–White) standard errors. `D_Tax` is the last trading day plus the first five of the local
tax year; `D_Fall` is the local autumn. The weather controls are the paper's own defence against the
confound the critique later presses.

**The trading form, and it is the implementable part.** The paper's illustration is a **pro-SAD
cross-hemisphere rotation**: pick one high-latitude market per hemisphere (their example is Sweden
and Australia), hold **100% of the Northern market through the Northern fall/winter, then rotate
100% into the Southern market through the Southern fall/winter**, i.e. reallocate the whole book
**twice a year** on the six-month returns corresponding to each index's local fall/winter. The
benchmark is a static 50/50 between the two. **Costs are explicitly neglected** ("For simplicity, we
neglect transaction costs"), and the significance tests throughout are **one-sided** — two
methodology-honesty marks that must be carried.

**Robustness the paper reports on its own construction.** Qualitatively unchanged under: hours of
night normalised to [0,1] or [−1,+1]; allowing the SAD measure to be non-zero in all four seasons;
moving or removing the solstice breakpoint; a maximum-likelihood Sign-GARCH specification; CRSP
equal-weighted and dividend-inclusive US indices in place of the price indices. The reported
magnitude is a positive annualised return attributable to the daylight term in **all** markets,
ranging **5.7% to 17.5%**, with the coefficient significant in all but one market; the regressions'
`R²` on daily data is **0.011 to 0.091**, which is the honest counterweight to that range and should
be quoted alongside it.

## Robustness evidence (qualitative only)

**The latitude gradient is reported as directional, not sharp.** The paper's own wording is that
countries "for the most part" and "tend to" show weaker, less significant daylight returns nearer the
equator. That is a monotonicity claim asserted over 9 countries without a monotonicity test — exactly
the gap `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` exists to flag — and it is the weaker
of the two cross-sectional predictions.

**The hemisphere flip is reported as confirmed, and the paper's own footnote qualifies it.** Pro-SAD
rotations are reported profitable between Australia and every Northern market, and between New
Zealand and every Northern market except the United States, but **mixed in sign for South Africa**,
which the authors attribute to large South African constituents being cross-listed gold producers in
London and New York. That is a *market-integration* caveat and it matters disproportionately here:
this universe is global, dividend-adjusted and USD-converted, and the same cross-listing logic
applies to many of its non-US names.

**The critique concludes the mechanism is spurious, and its stated grounds are the ones that bite.**
Jacobsen–Marquering (abstract only) examine this paper and Cao–Wei's temperature variant,
**confirm the underlying six-month seasonal** — lower summer-and-fall than winter-and-spring returns
in many countries, as in Bouman–Jacobsen — and find **"little evidence in favor of a SAD or
temperature explanation"**, reporting that **"a simple winter/summer dummy best describes this
seasonality"** and concluding that the weather–return correlation "might be spurious" and the mood
interpretation "premature". A published response by Kamstra–Kramer–Levi exists
(`10.1016/j.jbankfin.2008.09.011`, 37 Crossref citations) and was **not read**; this folder therefore
records the exchange as live rather than settled.

**A Tier-A-against-Tier-A tension, and it is the third of this shape in four nights.** [2026-10-01]
recorded the 40–60% vs ~12% discovery-window gap; [2026-10-02] recorded Hou–Xue–Zhang against
Jensen–Kelly–Pedersen. This one is structurally different from both and **better**, because the two
sides do not merely disagree on a constant — they make **opposite sign predictions about one cheap,
buildable portfolio.** On the daylight mechanism, a Southern-Hemisphere market has high expected
returns in the Northern summer. On a plain global Nov–Apr dummy, it does not: the companion note
records that the 108-market replication finds **positive November–April coefficients in Australia,
New Zealand and South Africa** — the same calendar phase as the North, not the opposite one — and
that restricted to markets with over ninety years of data Australia and South Africa are positive
though insignificant. **Both cannot be right, and this lab can find out which for free.**

## Implementability here

**The free screen comes first, and it is one measurement with no trial spent.** Split this universe's
instruments by the hemisphere of their listing (or of their ETF's underlying region) and estimate the
**November–April mean-return difference within each subset separately**, on train only, by the
companion note's one-dummy regression.

- If the Southern subset's Nov–Apr coefficient is **positive** (same phase as the North), the daylight
  mechanism is dead on this universe, the rotation below must **not** be built, and the lab has
  closed a Tier-A mechanism for zero trials.
- If it is **negative** (six months out of phase), the mechanism survives its sharpest test here and
  the rotation becomes the cheapest live candidate in `seasonality-calendar`.

The prior should be stated before the measurement, and honestly it leans against the mechanism:
`experiments/learnings.md` [Measured 2026-09-01] already found **Nov–Apr at +6.18 bps/day
(t = +3.58)** on the **whole global panel including its Southern-Hemisphere names**, which is only
consistent with a hemisphere flip if the Northern leg is strong enough to carry a diluted average —
possible, but it is the pooled version of exactly the question above, and the split is what
identifies it. This is the [2026-10-02] rule — *a confirmed mechanism with no rival mechanism
considered is an unidentified one* — applied where the identifying test is a **subset split** rather
than a re-weighting.

**If and only if the screen passes, the candidate is a two-rebalance hemisphere rotation**, and its
arithmetic is the reason it is worth naming at all. Long-only, gross 1.0 at all times, rotating
between a Southern-region sleeve (Australia / New Zealand / South Africa exposure, ETF-level where
available) and a high-latitude Northern sleeve, **twice a year**. At 15 bps/side that is roughly
**0.6%/yr** of turnover cost — against the **3.6%/yr** the lab measured for a monthly calendar
overlay and had to clear. It is also **not** the construction the lab closed: both
[Measured 2026-09-01] and [Measured 2026-09-02] close an overlay that **exits to cash**, and derive
the closure from `max_leverage = 1.0` plus a positive complement window. A rotation never holds cash,
so the no-leverage constraint does not bind and the complement-window sign condition does not apply.
State that explicitly in the hypothesis, because it is the only reason the family is not already shut.

**Four pitfalls, two of them disqualifying if ignored.**

1. **Prefer ETFs and say so.** `CLAUDE.md` and `program.md` both record that this universe's
   single-stock results are survivorship-inflated and ETF-level results are the most trustworthy here.
   A hemisphere rotation is naturally an ETF construction, which makes it one of the few candidates
   whose cleanest form is also its most trustworthy form.
2. **Cross-listing is the mechanism's own stated failure mode and this universe is full of it.** The
   paper's South Africa footnote is a warning that a market's *listing* latitude is not its holders'
   latitude. A Southern sleeve built from globally cross-listed large caps is testing nothing.
3. **Breadth is two bets a year.** Like any global calendar bet this has no cross-sectional breadth
   (`2026-08-19-fundamental-law-breadth-and-strategy-risk.md`); the deflated-Sharpe bar, not the
   gates, will be the binding constraint, and the honest prior on a resolvable `t` is low. Run it as a
   **scout**, which costs no holdout look.
4. **Do not import the latitude weighting.** The critique's conclusion is that a plain winter/summer
   dummy fits better than the daylight variable, and the primary's own robustness section reports the
   results are "roughly the same" across every normalisation of hours-of-night it tried. A measure
   whose normalisation does not matter is a measure carrying less information than it appears to:
   build the binary local-season rotation, **not** a continuous `H_t − 12` weighting, and treat any
   gain from the continuous form as a red flag rather than a refinement. This is the same
   use-every-screen-to-kill-never-to-forecast rule `experiments/learnings.md` records at seven axes.

## Related

- `2026-10-04-halloween-six-month-seasonal.md` — the effect this mechanism exists to explain, its
  108-market replication, and the Southern-Hemisphere coefficients that contradict the flip.
- `2026-09-02-return-seasonalities-common-factors.md`, `2026-08-29-same-calendar-month-seasonality.md`
  — the cross-sectional seasonality literature, a different object.
- `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — what the latitude-gradient claim is missing.
- `2026-09-10-currency-component-in-usd-converted-returns.md` — a hemisphere rotation on a USD panel
  is partly an FX rotation; that note is the precondition for reading its result.
- `2026-09-18-overnight-intraday-return-decomposition.md`, `2026-09-18-beta-at-night-versus-day.md` —
  the other place this folder has recorded a "time of day/night" partition of returns; unrelated
  mechanism, same temptation to over-fit a clock.
- `experiments/learnings.md`, [Measured 2026-09-01] and [Measured 2026-09-02] — the closures this
  construction is designed to sit outside of, and the +6.18 bps/day pooled Nov–Apr measurement that
  sets the prior for the free screen.
