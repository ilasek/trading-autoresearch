---
title: "Winner–Loser Reversals in National Stock Market Indices: Can They be Explained?" — read for the long-horizon end of country-index predictability, for a clean negative result on the risk explanation, and for the small-country localisation measured on a large-market subgroup that matches this lab's panel
authors: Richards
year: 1997
venue: The Journal of Finance (venue tier 1); read as IMF Working Paper WP/97/182
url: https://doi.org/10.1111/j.1540-6261.1997.tb02755.x
citations: 135 (Crossref `is-referenced-by-count` on the Wiley DOI, checked 2026-11-02), plus 45 on the duplicate JSTOR record `10.2307/2329478` — the work's citations are split across two Crossref records and the honest total is roughly 180. The IMF working paper carries its own DOI, `10.5089/9781451859232.001`.
sample_period: 1969-12 – 1995-12, end-quarter data; horizons k simulated from 3 to 60 months
markets: 16 national equity market return indices
tier: A
validation_overlap: false
published_post_2018: false
read: full text of IMF Working Paper WP/97/182 (December 1997), `imf.org/external/pubs/ft/wp/wp97182.pdf`, served first try (1.19 MB, 22 pages). **It is a text-layerless scan** — `pdffonts` prints an empty font table and `pdftotext` extracts 22 characters from 22 pages — so it was rendered with `pdftoppm -png -r 130 -gray` and read visually. Pages read: contents (2), Summary (3), Methodology and Data (5–6), Other Explanations (11–12), Conclusion (13–14). The tables and figures were **not** read; no number below comes from a table. The published JF version was not obtained (OpenAlex reports `oa_status: closed`, `any_repository_has_fulltext: false`, publisher DOI the only location).
---

## Mechanism

The long-horizon counterpart to short-horizon country-index continuation: over multi-year
ranking and test periods, national indices that were **losers** subsequently outperform national
indices that were **winners**. The paper's contribution is less the effect — which Richards
(1995) had already documented — than the serious attempt to kill it with risk, and the failure
of that attempt.

The candidate explanation the paper tests and rejects is that the loser countries are simply
riskier, so the reversal is a premium rather than a mispricing. The framework is explicitly
**international**: the paper assumes (on the strength of prior conditional-CAPM evidence) that
these markets were integrated over the sample, and therefore prices risk with **common
international factors** rather than with each country's own domestic moments — which is the
right null for a global cross-section and is unusual for a long-horizon contrarian study of its
era.

The behavioural mechanism left standing is **sentiment-driven cross-border flow**, and it is
genuinely a country-level story rather than a stock-level one relabelled: investor flows into
country and region funds track recent country performance, country-fund premia and discounts
swing with sentiment about foreign countries, and even "prudent" institutional allocators have a
career-risk reason to favour countries with strong recent returns and avoid recent poor
performers. Richards also makes the unusual observation that **increasing cross-border flows
could *increase* mispricing** rather than arbitrage it away, because they supply more investors
to "jump on the bandwagon" — a mechanism that does not predict decay with liberalisation.

## Construction recipe

- Treat the **16 national index return series as 16 assets**.
- Compute each country's total return over a `k`-month **ranking period**; sort into **four
  portfolios of four countries** each. Lowest-return quartile = losers (portfolio one), highest =
  winners (portfolio four).
- Weight **by market capitalisation at the end of the ranking period** — not equally. (This is
  the conservative choice and the paper flags it as such; see the robustness section.)
- Hold for a `k`-month **test period** and measure performance. `k` is simulated from **3 to 60
  months**.
- The **contrarian** (zero-net-investment) portfolio is *loser minus winner*.
- Returns over each `k`-month window are **buy-and-hold** over the whole window, not sums of
  monthly percentage returns; portfolio averages across test outcomes use the **geometric** mean
  of return relatives rather than the arithmetic mean of percentage returns, as a response to the
  skewness problem in long-horizon returns.
- Risk is tested two ways: (i) differences in **risk exposures** of winner and loser portfolios,
  with risk measured as covariance with the world market return and with other candidate factors;
  (ii) whether losers underperform winners specifically in **adverse states of the world**, proxied
  by large declines in the world index and by economic recessions.

## Robustness evidence (qualitative only)

- **Where the effect lives in horizon.** Reversals are **strongest around the 3-year horizon**.
  Combined with the short-horizon continuation documented in
  `2026-11-02-country-index-momentum-and-the-currency-component.md`, the country-index term
  structure is: continuation at 2–4 weeks, fragile at 12-1 months, reversal at ~3 years.
- **The risk explanation fails on every test the paper runs.** There is no evidence that prior
  losers' test-period returns were riskier than prior winners' — not by standard deviation, not
  by correlation with the world market return, not by other risk factors, and not by performance
  in adverse states of the world. This is a clean, explicitly-sought negative result, and it is
  the reason the paper is cited.
- **The effect localises to small markets, and this is measured two ways.** Splitting each ranked
  portfolio's time series by whether its constituents' share of world capitalisation was below or
  above the median, reversals are **roughly twice as large** in the periods when the extreme
  portfolios held mainly smaller countries. And splitting the 16 countries into the **eight
  largest** (US, Japan, UK, Canada, Germany, France, Australia, Switzerland) versus the eight
  smaller, the 3-year contrarian test-period return is **roughly 1.7× larger in the smaller-market
  group** — *but the difference is **not statistically significant***, because eight-country
  halves split into two-country portfolios give very wide confidence intervals. The ranking-period
  dispersion is likewise about 1.4× larger among the smaller markets, which Richards reads as
  country-specific shocks being larger, and less internationally transmitted, in small markets.
- **The effect is not confined to small markets.** The large-market subgroup still shows a
  positive 3-year contrarian return, at roughly 60% of the small-market one. The honest summary
  is a **gradient, not a threshold**.
- **A selection check the paper runs on itself:** the average share of world capitalisation in
  each portfolio at test-period start shows no marked country-size bias in which countries get
  selected into the extremes, and cap-weighting already reduces any such bias relative to equal
  weighting.
- **What the paper does not claim.** Richards does not resolve the anomaly. The conclusion names
  the short sample, the small number of countries, possible imperfect integration, and the lack
  of an agreed asset-pricing model as jointly preventing a verdict between mispricing and
  unmodelled risk.
- **The gap.** As with the other two sources in this cluster, **no transaction costs are
  modelled**, and the contrarian portfolio is a zero-net-investment long-short. Tier A is on
  venue, citations, the breadth of the risk tests and the explicit international framework.

## Implementability here

**The headline is a refusal, and it is arithmetic rather than judgement.** The effect is
strongest at a **3-year ranking and 3-year test horizon**. This lab's validation split is
2018–2023 — **six years**, i.e. **two non-overlapping 3-year test periods**. A strategy whose
signal needs 36 months of ranking history and whose payoff is measured over 36-month holding
windows cannot be evaluated on that split at any useful power, whatever its merit; overlapping
windows would supply more rows but almost no independent information, and the engine's bootstrap
interval would be measuring autocorrelation rather than skill. **Long-horizon country reversal is
refused on window width, before any question about whether the effect is real.** This is worth
stating plainly because it is the same binding constraint the 2026-11-01/02 nightly named from
the lab's own side — "the width of the validation window and the breadth of a large-cap-only
panel" — now reached independently from the literature.

**What the note is actually for, then, is two transferable facts.**

1. **The small-market localisation is confirmed by a second, independent, much older source.**
   `2026-11-02-multiverse-of-country-level-research-designs.md` reaches it across 13,824 designs
   over 1973–2022; Richards reaches it in 1997 over 1970–95 with 16 countries and a completely
   different method. When two sources 29 years apart with no methodological overlap agree that
   country-level predictability is concentrated in small, less-integrated markets, the folder
   should treat that as the structural fact about this family rather than as one study's quirk.
   **But Richards also supplies the hedge the multiverse paper does not:** his large-market
   eight-country subgroup — which is close to this lab's nine-index panel in composition — still
   shows a positive contrarian return, and his small-versus-large difference is **not
   significant**. So the correct statement is "the gradient runs against this panel", not "the
   effect is absent from this panel."
2. **Cap-weighting is the conservative choice and Richards took it.** His effect survives
   cap-weighting within the extreme portfolios, which is the same test
   `2026-11-02-country-index-momentum-and-the-currency-component.md` reports the short-horizon
   effect surviving, and the one the multiverse paper reports most country effects failing. The
   three together say: **weighting toward large markets shrinks country-level effects reliably,
   and kills them in the long-horizon value/size signals but not in the momentum-family ones.**

**One thing not to do.** Do not read "reversal at 3 years, continuation at 2–4 weeks" as a
licence to build a combined long/short-horizon country book. That is two bets, one of which is
untestable on this validation window, and the lab's standing anti-candidate list already refuses
blends whose case is a tighter error bar.

## Related

- `2026-11-02-country-index-momentum-and-the-currency-component.md` — the short-horizon end of
  the same term structure, and the source of the long-leg finding that makes the short-horizon
  end interesting to a long-only lab. Its companion pointer (Bhojraj–Swaminathan, abstract only)
  independently reports reversals in the two years after a momentum year, which is this paper's
  horizon reached from the other direction.
- `2026-11-02-multiverse-of-country-level-research-designs.md` — carries the discount for this
  whole family and independently finds the same small-market localisation. Note that its `LtRev`
  signal (return over t-60..t-13, Low-minus-High) **is** this paper's construction, and that it
  is not among the four signals that survive its multiverse — which is a real tension with this
  paper's Tier-A standing and should be recorded as such: a 1997 result that survived its own
  risk tests does not survive a 2026 design sweep.
- `2026-08-17-mclean-pontiff-publication-decay.md` — applies with unusual force to a 1997
  published anomaly.
- `experiments/learnings.md` — the lab's long-horizon reversal work is all at the **stock**
  level and under v1; nothing there measures a country-index reversal, so this is not a
  re-import of a refuted idea.
