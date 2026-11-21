---
title: "Price delay as a cross-sectional characteristic — a friction statistic computable from daily closes alone, whose premium the source itself localises to 0.02% of market value"
authors: Hou, Moskowitz
year: 2005
venue: "The Review of Financial Studies 18(3), 981–1020 — Tier 1 (peer-reviewed)"
url: https://doi.org/10.1093/rfs/hhi023
citations: 943 (Crossref `is-referenced-by-count`, checked 2026-11-21); 1,203 (OpenAlex by DOI, checked 2026-11-21)
sample_period: "NOT VERIFIED — the full text is unreachable (see Access). A 2005 RFS article cannot reach 2018, so the overlap flag below is false regardless of the exact window."
markets: "US (CRSP), per the abstract and the indexed record; not verified in detail"
tier: "Graded **C in use here**, and the gap between that and the venue is the point. Tier 1 venue, ~950–1,200 citations, and the *mechanism* is Tier A. But (i) the full text could not be obtained on four channels, so the construction below is second-hand, and (ii) the source's own abstract localises the premium to firms comprising **0.02% of market value** — a cell this panel excludes by construction, which makes the result unusable here however sound it is."
validation_overlap: false
published_post_2018: false
read: "**Abstract and indexed metadata only — the full text was NOT read.** Abstract verified from the RePEc/IDEAS record for the article (`ideas.repec.org/a/oup/rfinst/v18y2005i3p981-1020.html`), not from a search snippet. The construction recipe below is taken from a **full-text restatement in a source this folder did read in full** (Barinov 2014, filed tonight), and is flagged as second-hand throughout."
---

## Access

**Refused on four channels, and the refusals are worth recording because three of them are
channels this folder relies on.** (1) The publisher (OUP) is subscriber-only. (2) OpenAlex lists
**no open-access PDF location at all** for the DOI — only the publisher, an SSRN record with no
reachable file, and two CiteSeerX summary pages. (3) Both `core.ac.uk/download/<id>.pdf` candidates
returned **HTTP 403 with a 5,396-byte HTML body**, confirming the Cloudflare refusal this folder
recorded for `core.ac.uk` on 2026-11-19 — the host is still dark, and the one cheap retry per
session the standing rule allows has now been spent and failed. (4) Neither author's institutional
page surfaced a copy in search.

**The one thing that did work, and it is a method note.** The RePEc/IDEAS *article* record carries
the publisher's abstract in full and lists its own "no working-paper version found" status
explicitly. For a closed article whose preprint never materialised, **the RePEc article page is a
reliable abstract of record** and is strictly better than a search-result summary, because it is
the indexed text rather than a model's paraphrase of it. Use it to grade a source you cannot read,
and say so.

A separate refusal recorded tonight on the same hunt, since it belongs with these: **bepress /
Digital Commons `cgi/viewcontent.cgi?article=<n>&context=<series>` returns HTTP 403 with a
5,616-byte HTML body to an automated client**, even when OpenAlex names that exact URL as the
`best_oa_location`. This is the fourteenth "looks like an answer" mode: *an index asserting a green
open-access PDF is not evidence the file is fetchable*, and `scholarsarchive.byu.edu` is now a
recorded dark channel for this session. That is how the night's first-choice primary — Boyer,
Mitton & Vorkink's *Expected Idiosyncratic Skewness* (RFS 23(1), `10.1093/rfs/hhp041`, **808**
Crossref, checked 2026-11-21) — was lost; it is recorded as an unobtained pointer rather than
written up, because its value is entirely in a construction recipe that cannot be read from an
abstract.

## Mechanism

The idea is to measure, per stock, **how slowly its price incorporates market-wide information**,
and to read that delay as a summary statistic for the frictions affecting that stock. A stock whose
price responds to news only contemporaneously is unimpeded; a stock that keeps responding over
following weeks is impeded, and the delay measures by how much.

The abstract's claims, as indexed:

- The most delayed firms command a **large return premium** that is **not** explained by size,
  liquidity, or microstructure effects.
- Delay **captures part of the size effect** — i.e. it is a competitor to size, not an addition
  to it.
- **Idiosyncratic risk is priced only among the most delayed firms.** This is the clause this lab
  should read closely; see below.
- **Post-earnings-announcement drift increases monotonically in delay.**
- The authors attribute the effect to **investor-recognition** frictions (in the Merton 1987 sense
  — a stock few investors follow is held by few, and must offer more) rather than to trading costs.
- **The delayed firms comprise about 0.02% of market value** while generating substantial variation
  in average returns.

The economic story is therefore not a transaction-cost story. It is a *recognition* story: the
premium compensates for being unknown, and the measured delay is a symptom of being unknown rather
than of being expensive to trade. A later literature disputes exactly this, reading the delay
premium as systematic liquidity risk instead — that debate is noted here and not adjudicated,
since this folder holds neither side in full text.

## Construction recipe

**Second-hand — restated from Barinov's full text, not from the source.** For each firm, run a
firm-level regression of **weekly** returns on the contemporaneous **weekly market return**, then
the same regression with **four lags** of the market return added, and compare their fits:

```
D = 1 − R²(contemporaneous only) / R²(contemporaneous + 4 lags)
```

- `D = 0` means the lags add nothing: the price responds contemporaneously, no delay.
- `D → 1` means almost all of the explained variation arrives through the lags: heavy delay.

**Orientation caveat, and it is mine rather than the source's.** The restatement extracted from the
PDF printed the ratio with the *full*-model `R²` in the numerator, which cannot be right: the two
models are nested, so `R²(full) ≥ R²(contemporaneous)` always, and that orientation would make `D`
weakly negative for every stock. The form above is the only one consistent with the stated
definitions and with `D` being a delay, and it matches the measure's standard form in the wider
literature. **Anyone implementing this should re-derive the orientation from the nesting rather
than trusting either the quotation above or the extraction it came from.**

Further construction details — the estimation window, the rebalance cadence, the weighting, the
alternative delay definitions the source reportedly uses, and the breakpoints of the sort — are
**not in hand**, because they are not in the abstract. Barinov's use of it as a conditioning
variable implies an annually-updated firm characteristic estimated from roughly a year of weekly
returns, but that is an inference about his design, not a reading of this one.

## Robustness evidence (qualitative only)

- Heavily cited over two decades, in a Tier-1 venue, and used as an off-the-shelf attention proxy
  by later peer-reviewed work — which is itself a form of independent adoption, though not
  replication.
- **Tested against this effect and found unrelated to it**: Barinov double-sorts the turnover effect
  on price delay and reports no reliable relation in either CAPM or ICAPM alphas, and no relation
  between delay and the aggregate-volatility-risk loading. So delay and turnover are **distinct**
  frictions empirically, not two labels for one thing — a useful negative result, and one obtained
  from a full text.
- **The concentration claim is the governing robustness fact.** An effect generated by firms holding
  0.02% of market value is, by construction, an effect in the extreme micro tail. The source itself
  frames this as a strength of the *economics* (a tiny unrecognised segment explains a lot of return
  variation); for a portfolio on this panel it is disqualifying.
- No replication status located; no cost treatment located; multiple-testing treatment unknown. All
  three are unknown rather than absent, and the tier reflects the uncertainty.

## Implementability here

**The statistic is unusually well suited to this panel, and the premium it carries is not
available on it. Both halves of that sentence matter.**

**What fits, and it is rare.** The measure needs *nothing but the daily close panel and a market
proxy*. Weekly returns aggregate from daily closes; the market proxy can be an ETF id (explicitly
permitted by the protocol's guard) or the equal-weight eligible pool. It is a pure function of
returns, so it is immune to the as-of-fetch back-adjustment factor behind five `amihud126` nulls,
immune to currency and share-unit convention, and immune to the shares-outstanding problem that
makes the whole turnover literature uncomputable here. Estimated on a year of weekly returns it has
a formation horizon far beyond the 63-day floor the [2026-11-20] aim set, and as an
annually-updated characteristic it would rebalance slowly — squarely in the low-turnover corner v3
leaves nearly free. **On criteria (i), (iii) and (iv) it passes more cleanly than any mechanism this
folder has filed in weeks.**

**Why it is nevertheless refused.** Criterion (ii) and the panel's construction both fail it.

1. **The premium is localised to 0.02% of market value.** This universe is nine large-cap national
   indices, point-in-time — the top of the capitalisation distribution in nine countries. The cell
   that generates the delay premium does not exist in it. Per the README's standing rule, a
   mechanism whose own literature localises its effect to small or neglected names is excluded
   **by construction**, and a null measured here would be uninformative rather than evidence
   against the source. This is the strongest-form version of that rule the folder has yet filed:
   not "under-represented", but quantified by the source at two basis points of market value.
2. **The long-leg level is not in hand, and the leg that would be long is the unrecognised one.**
   A long-only book would have to buy the *most* delayed names. On this panel those are not
   neglected micro-caps; they are large-cap index members whose weekly betas happen to load on lags
   — a residual that mixes genuine slow incorporation with stale pricing from **non-overlapping
   trading sessions**. With nine markets across Tokyo, Hong Kong, Europe and the US in one panel,
   a Japanese name measured against a US-dominated market proxy will show high delay *for a time-zone
   reason*, and the v3 fill convention exists precisely because the US close is ~15 hours after
   Tokyo's. **On this panel the measure's cross-section would be dominated by geography, which the
   2026-10-13/14 learning already names as the confound in every whole-pool screen.**
3. **A delay sort is partly a size sort.** The abstract says delay captures part of the size effect.
   This panel's size dispersion within large-cap indices is compressed, so the component of the
   signal that is size is attenuated — which removes most of what the source says the signal is.

**What to take from it, free.** One reading rule, and one measurement the lab could run without a
trial if it ever wants to revisit this. The rule: **"priced only among the most delayed firms"** is
the general shape of this folder's recurring finding that an effect's conditioning variable is
often its real subject — idiosyncratic risk being priced *only* in the delayed tail is the same
structure as the turnover effect living *only* in the top band, and both say that the unconditional
cross-sectional statistic is the wrong summary. The measurement, if wanted: compute `D` on this
panel and regress it on region dummies. If region explains most of its cross-sectional variance,
the statistic is a time-zone indicator here and the vein closes permanently rather than
provisionally. That costs one function, scores no returns, and needs no holdout.

## Related

- `notes/2026-11-21-turnover-effect-uncertainty-not-liquidity.md` — the full-text source for the
  construction above, and the one that shows delay and turnover are empirically distinct frictions.
- `notes/2026-11-21-turnover-persistence-and-the-concave-premium-tokyo.md` — the band screen that
  would detect "priced only in the extreme tail" before a book is built.
- `notes/2026-11-06-investability-frictions-and-the-microcap-screen.md` and
  `notes/2026-11-06-illiquidity-premium-and-where-the-size-screen-sits.md` — the folder's existing
  statements of the rule that disqualifies this source, now with a quantified instance.
- `notes/2026-10-04-us-leads-the-world-country-lead-lag.md` — the folder's one prior mention of
  price delay, in passing, and the source of the time-zone objection in point 2.
