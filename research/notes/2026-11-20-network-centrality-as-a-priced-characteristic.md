---
title: "Network Centrality and the Cross Section of Stock Returns"
authors: Ahern
year: 2013
venue: unpublished working paper (SSRN; this version dated 15 November 2012) — venue tier 2
url: https://doi.org/10.2139/ssrn.2197370 — read in full from a conference-series copy at https://marriott.byu.edu/upload/series/1/docs/45835.pdf (274 KB, `pdftotext -layout` → 112 KB of clean text, 621 instances of `" the "`, zero `( )` dropout)
citations: 78 (Crossref `is-referenced-by-count`, checked 2026-11-20); no journal version of this title is indexed in Crossref as of that date
sample_period: network from the 1997 US input-output tables (a single snapshot); stock returns January 1998 – December 2002
markets: US only; 483 BEA sectors, matched to CRSP firms by 1997 NAICS codes
tier: C
validation_overlap: false
published_post_2018: false
---

**Read in full**: the network construction from the social-accounting matrix, the centrality
definition, the quintile sorts (levered, unlevered, equal- and value-weighted), the double sorts on
size and on customer/supplier concentration, the factor-model time-series regressions, and the
cross-sectional regressions with their control set.

Second note of the 2026-11-20 session. It is the canonical statement of the **other** way to use a
network in the cross-section: not as a weighting scheme for peers' past returns
(`notes/2026-11-20-peer-momentum-influence-weighted-peer-returns.md`) but as a **characteristic**
of the name itself. It is recorded here mainly to establish that **this reading has no
pre-signable direction**, and the grading below says so against the folder's own rubric rather
than against the lab's priors.

## Mechanism

A genuinely attractive economic story, and the reason the vein is worth a note even though the
evidence is weak. Standard factor models identify systematic risk *statistically* — from ex-post
covariances — and so say which stocks are risky without saying why. The paper's proposal is that a
firm's exposure to systematic risk can be read off **stable ex-ante fundamentals**: macroeconomic
fluctuations are the aggregation of sector-specific shocks (Long–Plosser; Acemoglu–Carvalho–
Ozdaglar–Tahbaz-Salehi), shocks propagate along real trade links, and so a sector sitting at the
**centre** of the trade network is exposed to many more of them than a peripheral one. Centrality
is therefore a *cause* of systematic risk, and central sectors should earn higher average returns
as compensation.

Note the sign logic carefully, because it is what makes the characteristic unusable as stated: the
prediction is a **risk premium**, not a mispricing. A book that buys central names is supposed to
earn more *because it bears more risk*.

## Construction recipe

**The network.** Build a social accounting matrix from the 1997 BEA detail-level input-output
`Make` and `Use` tables, appended with households and government from the national accounts, over
**483 sectors**; entries are dollar trade flows between sectors. Normalise to expenditure shares.

**Centrality.** **Eigenvector centrality** of that weighted directed trade network — a sector is
central when it trades with sectors that are themselves central.

**The book.** Sort sectors into quintiles on centrality (formed once, from the 1997 snapshot), map
CRSP firms to sectors by 1997 NAICS codes through the BEA concordance, and hold value-weighted
sector portfolios. Rebalancing is effectively **annual or slower** — centrality comes from tables
the BEA updates every five years — so as a book this is a genuinely **slow, low-turnover**
construction, which is the one design property the current research aim asks for.

**Reported controls.** Average firm size, leverage (returns are also reported unlevered using
debt-to-equity and marginal tax rates), eight-firm sales concentration, customer-sector and
supplier-sector concentration, industry scope, and the market-model beta estimated on the five
years preceding the network snapshot.

## Robustness evidence (qualitative only)

- **The claimed effect is very large and the long leg's level is stated.** Firm-level average
  returns run about **1.2%/month in the lowest centrality quintile against about 2.4%/month in the
  highest** — the paper itself converts the extreme-quintile gap to roughly **12 percentage points
  a year**, with about 3 points a year even between the second and fourth quintiles. In value-
  weighted factor regressions the market-model alpha rises from about **0.47%/month** in the least
  central quintile to about **1.5%/month** in the most central, and the four-factor alpha from
  about 0.08% to about 1.5%.
- **It is not firm size.** Size is insignificant in the cross-sectional regressions, the
  size-centrality double sorts keep the centrality pattern inside size quintiles, and the paper
  reports no significant relation between a sector's average firm size and its centrality.
- **Partly, it is beta.** Market betas rise with centrality in the market model and the difference
  between the extreme quintiles is significant there — which is what the risk story predicts —
  though the difference does not survive the addition of the three other factors, and the SMB, HML
  and UMD loadings show no pattern across quintiles. A further detail the paper flags honestly: the
  regression `R²` rises from under 50% in the least central quintile to 96% in the most central, so
  the factor models fit central sectors well and peripheral ones badly.
- **The rubric gaps are severe, and they are what sets the tier.** The sample is a **single
  five-year window** of returns against a **single network snapshot**: there is no multi-decade
  evidence, no subperiod stability test, and no out-of-sample country. It is **US only**. It is
  **unpublished** — 78 Crossref citations after more than a decade, with no indexed journal
  version. **No transaction costs are modelled.** Multiple testing is not addressed. Monthly
  average returns above 2% at the sector level over a five-year window are the kind of magnitude
  that a five-year window can manufacture, and the paper offers no way to tell the two apart.
- **The sign does not replicate across network definitions, which is the decisive point.** Three
  further literatures reach *opposite* conclusions on related networks — a negative
  centrality-return relation in a supply-chain network measured by PageRank, a negative relation
  for central economies in a global trade network, and a positive one in a return-correlation
  network. **None of those was fetched or read tonight**, and they are recorded below as named
  unobtained pointers rather than as evidence; what they establish even at that level is that
  nobody should treat "central earns more" as a settled sign. The cash-flow-network result of
  Buraschi–Porchia (central firms, higher expected returns) is cited inside this paper and also not
  read.

## Implementability here

**Directly: not at all.** The signal is built from input-output tables, i.e. fundamentals-adjacent
data this repo does not have and `program.md` lists as an unapproved future upgrade. There is no
daily-OHLCV route to a *trade* network.

**By substitution: only onto an object whose sign this source cannot supply.** The reachable
substitute is a centrality computed from the names' own price or volatility series — the
variance-decomposition network of
`notes/2026-11-20-variance-decomposition-connectedness-as-network-degree.md`, or simply average
pairwise correlation. Two reasons that substitution does not inherit this paper's prediction:

1. **A different network is a different object, by the measurement literature's own warning.**
   Diebold–Yilmaz state that connectedness "will not, and should not, be robust to choice of
   reference universe"; a fortiori it is not robust to replacing real trade flows with return
   co-movement. The empirical record above is that the sign flips with the network definition, so
   the substitution is not a cheap proxy for the same quantity.
2. **A price-based centrality is this lab's closed axis in costume, and the paper's own mechanism
   says so.** Degree centrality in a co-movement network *is* a weighted average co-movement with
   the other names, which is average correlation, which is the main ingredient of beta — the
   decomposition this folder already holds in
   `notes/2026-09-24-betting-against-correlation-decomposing-beta.md` and
   `notes/2026-10-06-betaless-variance-decomposition-and-average-correlation.md`. And the paper's
   claim is explicitly that the premium **is** compensation for systematic risk. The lab has
   measured that **Sharpe is flat in beta on this panel** (2026-10-09/10, reproduced a fifth time
   on 2026-11-20): a characteristic whose payoff is a beta premium cannot generate skill against a
   fully-invested equal-weight pool here, because the pool already carries beta ≈ 1. A central-name
   book would be expected to earn more *and be worse in Sharpe*, and a peripheral-name book is the
   de-risking construction the record closed.

**Verdict: an ANTI-CANDIDATE, on three independent grounds, any one sufficient.** (i) Tier C
evidence — one five-year window, one network snapshot, one market, unpublished, no costs. (ii) The
sign is not replicated across network definitions, so the lab cannot pre-sign the direction, and
its own rules require a pre-signed direction before a trial. (iii) The reachable implementation is
an average-correlation/beta ranking, which is closed by measurement on this panel. **Do not spend
a trial on centrality as a characteristic.** If the vein is taken up at all, it is as the
*weighting scheme* of the peer-momentum note, where the direction comes from the continuation
effect and not from centrality itself.

**One piece worth keeping.** The paper's framing — *read a name's risk exposure off a stable
ex-ante structural variable rather than off its own ex-post covariance* — is a good idea that
survives its evidence, and it is the only thing in this note that could ever become a candidate
here. The lab's equivalent of "stable ex-ante structure" would have to be built from the price
panel, which returns it to problem (2) above; the honest conclusion is that this repo's data cannot
express the idea.

## Related

- The tradeable half of the same vein: `notes/2026-11-20-peer-momentum-influence-weighted-peer-returns.md`.
- The instrument and its reference-universe warning: `notes/2026-11-20-variance-decomposition-connectedness-as-network-degree.md`.
- Why a price-based centrality collapses onto beta:
  `notes/2026-09-24-betting-against-correlation-decomposing-beta.md`,
  `notes/2026-10-06-betaless-variance-decomposition-and-average-correlation.md`,
  `notes/2026-09-17-downside-beta-and-the-volatility-confound.md`.
- The measurement that closes the de-risking class on this panel: `experiments/learnings.md`
  2026-10-09/10 ("Sharpe is flat in beta on this panel, so risk-reduction is not a source of
  skill") and 2026-11-20 (fifth reproduction).
- Named unobtained pointers from tonight, none to be re-hunted without a reason: the supply-chain
  PageRank result, the global-trade-network country-level result (*Journal of International Money
  and Finance*, 2025), the return-correlation-network centrality result, and Buraschi–Porchia on
  cash-flow networks.
