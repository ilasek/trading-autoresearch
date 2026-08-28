---
title: "Individualism and Momentum around the World"
authors: Chui, Titman, Wei
year: 2010
venue: The Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/j.1540-6261.2009.01532.x
citations: 1148 (Crossref `is-referenced-by-count`, checked 2026-08-28); 1231 (Semantic Scholar DOI endpoint, same date, which dates the record to the 2004 working paper)
sample_period: February 1980 – June 2003 (individualism-sorted tests start February 1984)
markets: 41 countries, >20,000 individual stocks (Datastream International, including its "Dead" stocks list; CRSP for the US), returns in USD
tier: A
validation_overlap: false
published_post_2018: false
read: full text of the **November 2004 working-paper version** (National Taiwan University conference proceedings mirror, `fin.ntu.edu.tw/~conference/conference2004/…`). The published JF 2010 version was not obtained; construction details and sample below are from the working paper, and two findings marked below are taken from the published abstract only
---

## Mechanism

The paper explains **cross-country variation** in momentum, not momentum itself. Its premise is
Daniel–Hirshleifer–Subrahmanyam: momentum arises from overconfidence and self-attribution bias,
under which investors overweight private signals and take credit for confirming outcomes, pushing
prices past fundamentals in the direction of recent news. If those biases have a cultural
component, momentum should be stronger where the culture supports them. The proxy is Hofstede's
**individualism index** — the degree to which people define themselves by internal attributes
that differentiate them from others — which the psychology literature ties to self-attribution
bias. The prediction is a positive cross-country relation between individualism and momentum
profits, and the paper finds one.

The mechanism content worth carrying is narrower than the headline. The authors are describing a
**cross-sectional prior over markets**: the same signal should pay differently in different
investor populations, and the difference should track measurable features of those populations
rather than of the stocks. The published abstract adds that momentum profits also relate
positively to analyst forecast dispersion, transaction costs and the market's familiarity to
foreigners, and **negatively to firm size and volatility** — i.e. the same size gradient the
other international sources report, established here across countries rather than within them.
(Those two relations are from the published abstract; the working paper read here does not carry
the transaction-cost variable.)

## Construction recipe

Deliberately coarse, because many of the 41 countries are small:

- **Signal**: cumulative past **six-month** return, ranked **within each country**.
- **Groups**: top and bottom **terciles** rather than Jegadeesh–Titman deciles, explicitly because
  most country samples are too small for deciles.
- **Skip**: one month between the ranking period and the holding period, to blunt bid-ask bounce
  and lead-lag effects.
- **Holding**: six months, **equal-weighted**, with overlapping vintages — the winner book in any
  month is the equal-weighted combination of the six most recent monthly winner portfolios. Same
  overlapping-tranche machinery as Jegadeesh–Titman and Rouwenhorst; this is now the fourth
  independent source using it as the default.
- **Two ways of aggregating countries**, and the distinction is the useful part:
  - **Country-average**: form the momentum portfolio inside each country, then average the
    country-level long-short returns.
  - **Country-neutral**: pool the countries' winner portfolios into a single global winner book
    (and likewise for losers), so the book holds every country in fixed proportion.
  The two produce closely comparable spreads, with the country-neutral book's t-statistic in the
  same range as the country-average one's.
- **Universe hygiene**: at least 30 qualifying stocks per country and at least five years of
  portfolio history (this is what reduces 55 Datastream countries to 41); stocks need at least
  eight months of return history; the bottom 5th percentile of each country's market cap is
  deleted each month; Datastream's **"Dead" stocks list is included** to alleviate survival bias.
- **Currency**: all returns measured in **USD**.

## Robustness evidence (qualitative only)

- Momentum profits **increase monotonically** across the low / middle / high individualism
  country groups, for both the country-average and country-neutral aggregations, and the gap
  between the top-30% and bottom-30% individualism groups is of the same order as the entire
  momentum premium reported in comparable samples — a cross-country difference large enough to be
  the difference between an effect and no effect, not a second-order tilt.
- The relation survives controls for the standard cross-country market-quality variables:
  common-law versus civil-law legal origin, anti-director rights, a corruption perception index,
  accounting standards quality, and the risk of earnings management. Some of those variables also
  explain cross-country momentum, but less strongly and less robustly than individualism.
- A **bootstrap** in which the country-level explanatory variables are randomly reassigned across
  countries indicates the individualism coefficient is unlikely to be a chance artifact of the
  cross-country regression.
- Robust to an alternative individualism measure from the GLOBE project.
- **The counterweight, and it is from a tier-1 source in this folder.** Fama–French (2012)
  explicitly decline this explanation on two grounds: the psychological argument is reversible
  (low individualism could equally *produce* momentum if prices react slowly to information), and
  a Hotelling `T²` test on their four regions fails to reject equality of expected momentum
  returns across regions at the 90% level — so the Japanese exception, the case this hypothesis is
  most often invoked to explain, may simply be noise. The two papers are not testing the same
  thing (41 countries with a continuous cultural regressor versus 4 regions with a joint equality
  test), so both can be right about their own statistic; but the disagreement about whether
  cross-market momentum differences are real is unresolved in what has been read here, and the
  later paper is the skeptical one.
- **Multiple testing** is not addressed beyond the bootstrap, and the cultural-variable literature
  is a large space of country-level regressors — Hofstede alone supplies five dimensions, of which
  one is selected here on a stated a-priori argument. The stated argument is genuine, but it is
  the kind of selection the folder's own prior-weighting machinery (candidate #31) exists to
  discount.

## Implementability here

Low direct buildability, real interpretive value, and one clear anti-candidate.

- **There is no build here.** The repo cannot condition on culture: Hofstede's index is a
  country-level constant, the universe has no country field, and per-country instrument counts
  would be single digits. Even if it could, the construction would be a fitted country-level
  weight on a cross-sectional regressor estimated over the same window as the signal — screen
  #1's class exactly.
- **Anti-candidate: do not down-weight or exclude any regional bloc on this evidence.** The
  temptation the paper creates is to drop or shrink low-individualism (broadly, East Asian) names
  from the momentum basket. Three reasons not to: the effect is measured on long-short
  within-country books, not on a long-only global basket; Fama–French's equality test says the
  regional differences may not be distinguishable from noise at all; and any such exclusion is a
  free parameter chosen from a source whose own sample ends long before this repo's data. If a
  regional grouping is used here at all, use it for **neutralised ranking** (which is a variance
  argument with a named confound — see the Rouwenhorst note) rather than for exclusion (which is
  a mean argument resting on this disputed result).
- **What does transfer: the country-neutral aggregation is validated a second time.** This paper
  builds its global book by pooling within-country winner portfolios, and gets a spread and a
  significance level comparable to averaging country-level strategies. Together with Rouwenhorst
  and Fama–French, three of the four international sources read this session assemble a global
  momentum book from **locally-ranked components**. None of them ranks one pooled global
  cross-section, which is what this repo does.
- **The size relation is the fourth independent statement of the same discount** — momentum
  profits relate negatively to firm size across countries, matching Rouwenhorst's size deciles,
  Fama–French's size gradient and Asness–Moskowitz–Pedersen's conservatism caveat. This repo's
  large-cap universe should carry the low end of every published momentum expectation.
- **One caution the published abstract adds and the folder should keep**: momentum profits relate
  **positively to transaction costs** across countries. Cross-country momentum is strongest where
  trading is most expensive, which is the same selection the cost-side literature found within
  the US cross-section (momentum sorts toward expensive names). It is a reason to discount
  cross-country momentum evidence *further* for a cost-paying book, not a reason to seek out
  expensive markets.
- **Provenance caveat.** Everything above except the two abstract-sourced relations comes from the
  2004 working paper. The published version has additional variables and may differ in sample
  detail; the sample period, universe filters and portfolio mechanics recorded here are the
  working paper's and should be re-checked against the published article before anything leans on
  a specific number.

## Related

- `notes/2026-08-28-local-versus-global-factor-construction.md` — the source that disputes this
  one's central interpretation; read the two together.
- `notes/2026-08-28-international-momentum-country-neutral.md` — the country-neutral construction,
  with the variance decomposition that makes it worth building.
- `notes/2026-08-25-prior-weighted-multiple-testing.md` and
  `notes/2026-08-25-bayesianized-p-values-prior-odds.md` — the machinery for discounting a
  hypothesis whose motivating variable was selected from a menu.
- `notes/2026-08-27-momentum-net-of-costs-debate.md` — the within-US version of "momentum sorts
  toward expensive names".
