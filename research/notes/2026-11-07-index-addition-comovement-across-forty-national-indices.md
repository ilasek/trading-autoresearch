---
title: "Comovement of Newly Added Stocks with National Market Indices: Evidence from Around the World (read as IMF Working Paper 11/47, 'Additions to Market Indices and the Comovement of Stock Returns Around the World')"
authors: Claessens, Yafeh
year: 2013 (published; online 2012). Working paper read: March 2011
venue: Review of Finance 17(1), 203–227 (peer-reviewed, European Finance Association journal); working paper = IMF Working Paper 11/47
url: https://doi.org/10.1093/rof/rfs001
citations: 58 (Crossref `is-referenced-by-count`, checked 2026-11-07)
sample_period: 2001–2010
markets: 40 national markets, developed and emerging — index additions to each country's main index, including the CAC 40, DAX, FTSE 100, AEX, Hang Seng and Nikkei 225
tier: A — peer-reviewed venue, full text read, forty markets rather than one, and the design pits two named theories against each other with the losing one still reported as partly supported
validation_overlap: false (sample ends 2010)
published_post_2018: false
read: full text, IMF working-paper version (967 KB PDF, 35 pages → 103 KB of clean text, 649 instances of `" the "`, title line verified)
---

## Access

Read from **`imf.org/external/pubs/ft/wp/<year>/wp<yynn>.pdf`** on the first try. The IMF
working-paper series is a **flat, fully derivable path** — once the series number is known
(`11/47` → `wp1147.pdf`), nothing has to be guessed or read out of a landing page, which makes it
better-behaved than every author- and institution-hosted channel `research/README.md` records. Worth
keeping for international-finance topics generally.

OpenAlex reports the published *Review of Finance* article as `oa_status: green` with its only
`oa_url` pointing at **SSRN** (a known refusal), and lists no other repository. So the published
version was **not** read; the IMF working paper was. Note also that the two versions carry
**different titles and reversed author order** in different catalogues, which is the 2026-10-01
FEDS lesson again: resolve by DOI or author, never by title.

**What was read is the working paper.** Its abstract, forty-market sample, four comovement measures
and two competing explanations match the published article's title and abstract, but table numbers
and any revisions made in review were not seen.

## Mechanism

This is the **generalisation test** for the index-demand channel, and it is the source this folder
needed: the US index-effect literature it already holds is one country and one committee, and
`2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` explicitly leaves the non-US
case open.

The question is whether a stock's return starts comoving more with its national index *because it
was admitted to that index*, absent any change in the firm. Two accounts compete:

- **Demand / category-habitat.** Investors allocate by category, and an index is a category. On
  admission, capital that treats "members of this index" as its habitat starts holding the name, and
  correlated habitat-level flows impart a common return component. This is the same channel as
  `2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md`, here identified
  cross-country instead of cross-weight.
- **Information diffusion.** Members absorb economy-wide news faster — more analyst coverage, more
  attention — so a member's return loads more on the market because it is *updating* faster, not
  because it is being *traded* more.

The answer is mostly the first, with the second not dismissed. The discriminating evidence is
structural rather than statistical, and this is the part worth carrying:

**The admission effect is weaker when the index is concentrated.** If a handful of names carry most
of an index's capitalisation, there is little reason to replicate the index — buying the few largest
names tracks it well enough — so habitat-driven demand for a *newly added, small* member is weak.
If an index is dispersed, replicating it means buying everything in it, and admission brings real
flow. Magnitude, as a mechanism size: a top-five weight higher by 10 percentage points goes with a
post-admission beta increase lower by about 0.03, against a sample-average daily beta increase of
about 0.07 — so the moderator is of the same order as the effect. Information diffusion has no
reason to care about index concentration, which is what makes the test discriminating.

Two further results in the same direction: the effect is stronger where investors prone to
index-based investing are more present, and it strengthens across the sample alongside the growth of
index-tracking capital. (The paper's year-by-year detail includes a dated interruption to that
trend; `research/README.md`'s anti-lookahead rule 1 excludes event narratives, so it is omitted
here and the trend is recorded only as the mechanism-linked monotone statement.)

The information side is not empty: post-admission **analyst coverage and turnover** rise in the
large majority of markets, and comovement is related to those increases — but controlling for them
leaves the concentration and investor-base findings intact, and the paper reports the
information-side magnitudes as small.

One result the paper flags as fitting **neither** theory cleanly, and it is the one most relevant
here: **the comovement increase is larger for names whose pre-admission beta was low**, highly
significant in both daily and weekly data. Larger firms also show bigger increases — and the paper
pre-empts the obvious objection by noting this cannot be a weight artefact, because the comovement
is measured against the index *excluding the added firm*.

## Construction recipe

The measurement design, which is the transferable part:

1. **One index per country** — the country's main index, the natural habitat. The paper is explicit
   that choosing a *non*-primary index biases the test **against** finding an effect, which is the
   right direction for a bias to run.
2. **Univariate beta of the added name against the rest of its index**, with the added firm
   **excluded** from the index return so its own weight cannot manufacture the result. This exclusion
   is the single most important detail; without it the whole finding is mechanical.
3. **Pre-window: daily data for the three months ending 90 days before admission.** The 90-day
   stand-off is deliberate — it keeps announcement and rumour out of the "before" period.
4. **Post-window: daily data for the three months after admission.**
5. **Two outcome measures, not one:** the change in beta and the change in `R²`. They answer
   different questions (loading versus explained share) and the paper reports both throughout.
6. **A second frequency as a cross-check:** betas and `R²` from **weekly** data over the 52 weeks
   before and after, which is less sensitive to event-window turbulence. Comparing frequencies is
   itself one of the tests between the two theories.
7. **Cross-sectional stage:** regress the four changes on index concentration (top-five weight), a
   time trend, country financial and economic development, and firm-level pre-admission beta,
   leverage and size.

A methodological note the paper makes and this folder should reuse: a bivariate
member-versus-non-member decomposition (as in the US and Nikkei studies) is **not feasible in most
countries**, because the non-index part of the market is small and its returns often unavailable.
Designs that work in deep markets do not port to shallow ones.

## Robustness evidence (qualitative only)

- **Breadth is the robustness.** Beta rises in 30 of 40 markets on daily data and 26 on weekly;
  `R²` rises in 32 (daily) and 34 (weekly). The paper tests the sign count against a binomial null
  rather than eyeballing it.
- **Heterogeneity is reported, not buried.** The effect is consistent and significant in some
  markets, weak in others, and the group with zero or negative measured effects is identified by
  name (the Scandinavian markets) — where turnover nonetheless rises. A note that said "index
  addition raises comovement everywhere" would be misreporting this paper.
- **Small-sample honesty.** Several countries have very few admissions and the paper says their
  per-country numbers should be read with caution. Inclusion counts per market range from single
  digits to a couple of hundred.
- **Development is not the moderator.** Neither GDP per capita nor market-capitalisation-to-GDP is
  significant in any specification — so this is not a developed-versus-emerging story, which makes
  the concentration result harder to explain away.
- **Measurement caveat the authors raise.** Short daily windows around an event buy sample size at
  the cost of precision and are exposed to elevated event-time volatility; the weekly design is the
  stated remedy.
- **Replication standing.** This *is* the out-of-sample replication of the US/UK/Canada/Japan
  addition-comovement results, and it confirms them in direction while locating the moderator that
  the single-country studies could not see. Treat it as replication evidence rather than as a new
  effect.

## Implementability here

This is the most directly relevant of tonight's three notes, because **the event it studies is
visible in this repo's contract** — and the first thing to establish is exactly how much of it is
visible.

**What is observable.** `eligible` is a dates × columns boolean, `True` where the name was an index
member. A column's **first `True` is an admission event**, and the lab sees it without naming a
stock or reading a membership file. That makes "time since first eligible" a legitimate, causal,
contract-supplied conditioning variable.

**What is not, and this is binding.** `program.md` states that *a column appears in `prices` only
once the name has been eligible*. So the **pre-admission window does not exist in the visible
panel**, and the paper's central design — the *change* in beta from a pre-window ending 90 days
before admission to a post-window after it — **cannot be reproduced**. Only the post-admission side
is available. A candidate can ask "do newly admitted names behave differently from seasoned
members?"; it cannot ask "did this name's beta rise when it was admitted?". Any construction phrased
as the latter is measuring a truncation artefact, and the 90-day stand-off the paper insists on is
unavailable in the same stroke.

**Two further constraints on porting the findings:**

- **The moderator is not measurable by a candidate.** Index concentration is the paper's key
  variable, and it needs per-index membership and capitalisation weights — both outside the
  contract. The panel's nine indices differ enormously in exactly this dimension (a 50-name index
  and a 500-name index are not the same habitat), so the finding predicts the admission effect is
  **heterogeneous across this panel's indices** — and a candidate has no sanctioned way to tell
  which index a name belongs to, so it cannot condition on the moderator. Admission effects here are
  therefore a **mixture across nine different regimes**, which attenuates whatever is measured.
- **The eight non-US indices are only tracked from 2009.** Admission events for them are visible
  only over part of the sample, with the S&P 500 from 1996. So the composition of "newly eligible"
  names shifts across the train window for a reason that has nothing to do with markets — and this
  compounds the pre-2009 coverage thinness `program.md` already warns about.

**What a candidate could actually do with this, stated as a hypothesis rather than a
recommendation.** The reachable claim is a **cohort** claim, not an event claim: names in their
first months of eligibility should, per the demand channel, carry a *higher* loading on the pool and
*less* idiosyncratic variance than seasoned members, with elevated turnover. All three sides of that
are measurable from the contract — pool beta and `R²` from `prices`, turnover from `aux`'s `volume`
and `dollar_volume`. A `liquidity-volume` or `portfolio-learning` scout could test whether a
newly-eligible cohort is distinguishable from a seasoned cohort on those three, which is a question
about the panel's structure rather than a return prediction, and that is the honest framing.

Three cautions before anyone writes it:

1. **The low-pre-beta result cuts against using this as a return signal.** The biggest comovement
   increases accrue to *previously low-beta* names, and the folder's low-risk literature
   (`2026-08-18-low-risk-investing-industry-neutral.md`,
   `2026-08-18-defensive-equity-replication-and-construction.md`) says low-beta names are where the
   measured premium lives. An admission-conditioned long book would be buying names whose beta is
   about to rise, i.e. shedding the defensive exposure, with no compensating return claim in this
   paper. This paper contains **no** return prediction at all — it is about second moments. Nothing
   in it licenses an expected-return hypothesis, and `research/README.md`'s rule about not importing
   performance expectations from the literature applies with full force.
2. **The random-portfolio gate absorbs much of it.** Protocol v2's hard gate draws 200 random
   portfolios from the same point-in-time pool with the same holdings schedule. A cohort effect
   shared by all newly-eligible names is partly in the null already.
3. **It overlaps an existing level effect.** `2026-09-13-listing-age-as-a-level-effect.md` and
   `2026-11-06-index-membership-is-not-an-information-free-selection.md` already give this folder
   reasons why recently-admitted names differ. Time-since-first-eligible is a *single* variable that
   proxies for admission comovement, listing age, and the selection the committee performed. A trial
   keyed on it cannot attribute its result to any one of them — which is a reason to write it as a
   **scout** and say so in the hypothesis, not as a challenger.

## Related

- `2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md` — the single-market,
  cross-weight version of the same demand channel. This note is its generalisation test, and the
  generalisation holds in direction.
- `2026-11-07-free-float-redefinition-as-a-benchmark-change.md` — the third side: the rule changing
  rather than a name being admitted to it, and the source of the warning that an admission window
  also contains an anticipatory arbitrage footprint.
- `2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` — the US index-effect note
  that named the non-US case as its open question. This note answers it: the comovement half of the
  effect is a global phenomenon, moderated by index concentration.
- `2026-11-06-index-membership-is-not-an-information-free-selection.md`,
  `2026-11-06-illiquidity-premium-and-where-the-size-screen-sits.md`,
  `2026-11-06-investability-frictions-and-the-microcap-screen.md` — the panel-admission cluster this
  extends beyond the S&P 500.
- `2026-09-13-listing-age-as-a-level-effect.md` — the confound a time-since-eligible candidate
  cannot separate itself from.
- `2026-09-13-analyst-coverage-and-the-speed-of-bad-news.md`,
  `2026-09-05-price-delay-market-frictions.md` — the information-diffusion channel this paper
  measures and finds secondary.
- `2026-10-13-equal-weighting-and-the-rebalancing-component.md` — index concentration as a
  construction variable, from the weighting side rather than the habitat side.
