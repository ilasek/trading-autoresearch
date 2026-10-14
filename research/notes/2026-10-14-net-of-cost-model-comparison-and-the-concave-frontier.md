---
title: "Comparing Factor Models with Price-Impact Costs"
authors: Li, DeMiguel, Martín-Utrera
year: 2024 (working-paper version read, dated December 2022)
venue: "Journal of Financial Economics 162, 103949 — venue tier 1. Read as the Lancaster FinEc 2023 conference working-paper version; the published version was not fetched"
url: https://doi.org/10.1016/j.jfineco.2024.103949 · full text read at https://wp.lancs.ac.uk/finec2023/files/2023/01/FEC-2023-068-Victor-DeMiguel.pdf
citations: "3 (Crossref is-referenced-by-count, checked 2026-10-14) — a recent article, so the count carries almost no information; the tier below rests on venue and on the fact that the central claim is a proof"
sample_period: "January 1980 – December 2020 (empirical section). The theoretical results are sample-free"
markets: "US equity factor portfolios (q-factor, FFC4, FF5, FF6, and a 20-factor high-dimensional model)"
tier: "B — tier-1 venue and the key result is a proposition rather than an estimate, but the empirical half is single-market, recent, unreplicated, and its sample overlaps this lab's validation window. The proposition is used below; the empirical rankings are not"
validation_overlap: true
published_post_2018: true
---

## Access

Read in full as the FinEc 2023 conference version (687 KB; `pdftotext -layout` → 189 KB clean
text; `" the "` count 1,337, `( )`-dropout check zero, all displayed algebra intact including the
propositions and the asymptotic variance expressions). Two decoys on the way: a 2024 conference
site served a **genuine 1.1 MB PDF of the same title that is a six-page slide deck, not the
paper** — `file` reports a valid PDF and the byte count looks like a working paper, so the only
tells are the page count and the content — and an EFMA mirror of the same paper returned
**HTTP 503 with a 326-byte `Service Unavailable` HTML body**.

**One source in this note's chain was not read and is recorded as a pointer, not a claim.**
Detzel, Novy-Marx & Velikov, *Model Comparison with Transaction Costs*, **Journal of Finance
78(3), 1743–1775 (2023), doi:10.1111/jofi.13225, 80 citations (Crossref) / 99 (OpenAlex), both
checked 2026-10-14** — the paper that first applied the squared-Sharpe criterion to *net* returns
— could not be obtained. Channels spent: Wiley's `pdfdirect` endpoint, which OpenAlex lists as a
**bronze OA location**, returned **HTTP 403 with a 5.5 KB Cloudflare body** (so an `is_oa: true`
flag is not a promise the file is fetchable — a fourth instance of the warning
`research/README.md` already carries); all three co-authors' own sites list the paper with **only
a DOI link and no self-hosted PDF** (`rnm.simon.rochester.edu` hosts four other PDFs and not this
one; `andrewdetzel.com` links the DOI; Penn State Pure holds a record with no file); and SSRN is
the known 403. What *was* obtained is its **verbatim abstract**, from the Penn State Pure record,
and the present paper's own two-sentence description of its method. Everything attributed to it
below comes from one of those two and is flagged at the point of use. Its abstract's own words:
"Failing to account for transaction costs materially impacts inferences drawn when evaluating
asset pricing models, biasing tests in favor of those employing high-cost factors."

## Mechanism

The question is the one `notes/2026-10-14-which-alpha-the-sufficient-statistic-for-beating-a-benchmark.md`
answers without costs: **which of two portfolios offers the better investment opportunity set?**
Barillas–Shanken prove that the maximum squared Sharpe ratio is a *sufficient statistic* for that
comparison. This paper establishes exactly when that remains true once trading is charged, and the
answer is a clean three-way split by the **shape of the cost function**:

- **No costs.** The efficient frontier is a straight line in the mean–standard-deviation diagram.
  Every portfolio on it has the same Sharpe ratio, so one number characterises the whole set.
- **Proportional costs** (cost linear in the dollar amount traded). The frontier is **still a
  straight line**, lower down: mean, standard deviation *and* cost all scale with the size of the
  position, so the net Sharpe ratio is constant along the frontier and **one number still
  characterises the set.** This is the regime in which (per the abstract above, and this paper's
  description of it) Detzel–Novy-Marx–Velikov compare models on the squared Sharpe ratio of net
  returns, and the authors say explicitly that their own criterion "is equivalent to the squared
  Sharpe ratio in the cases with proportional costs and without trading costs."
- **Price-impact costs** (cost growing *faster* than linearly: their Definition 2 is
  `f(cθ) > c f(θ)` for `c > 1`). **Proposition 3:** the frontier is **strictly concave**, every
  portfolio on it has a *different* net Sharpe ratio, and all of them are below the no-cost maximum
  Sharpe ratio. A single Sharpe number therefore **cannot** characterise the opportunity set, and
  the Barillas–Shanken criterion stops being sufficient. The comparison must instead be made at a
  **stated risk aversion**, on mean–variance utility net of costs — which also means the answer can
  change with the amount of capital deployed.

**Why the shape is the whole story, in one line.** Mean and variance are homogeneous in position
size; a linear cost is too, so it rescales the line. A superlinear cost is not, so it bends it.

**The identity worth carrying out of the paper.** With quadratic price-impact costs — the standard
assumption, impact linear in the amount traded — the dollar cost of holding factor portfolio `θ` is
`½ θ′ X̃′ D X̃ θ` where `D` is a **diagonal** matrix of per-stock impact parameters, and the
per-period cost matrix `Λ*ₜ = X̃ₜ′ Dₜ X̃ₜ` enters the mean–variance problem *exactly like extra
covariance*:

> `θ* = (Σ + Λ)⁻¹ μ` and `U = μ′ (Σ + Λ)⁻¹ μ`, with `Λ = Λ*/γ`

i.e. **optimising net of quadratic trading costs is the same operation as optimising gross with an
inflated covariance matrix**, where the inflation is the cost matrix divided by absolute risk
aversion. Two corollaries the authors draw: the cost matrix is *not* diagonal in factor space even
though `D` is diagonal in stock space, which is exactly **trading diversification** (trades in
different factors cancel at the stock level); and the risk-aversion parameter `γ` sets the relative
weight of variance against cost, so a less risk-averse investor is effectively charged more.

**Their generalisation of Barillas–Shanken.** Test assets remain irrelevant under price-impact
costs too — the comparison reduces to the models' own maximum net-of-cost utilities.

**Their statistical test, and when it has power.** They derive asymptotic distributions for the
difference of two models' net utilities, for nested and non-nested pairs, extending Kan–Robotti
and Barillas–Kan–Robotti–Shanken. The closed-form variance yields a result worth remembering
whenever two books are compared: **rejection is easier when the two portfolios' returns are
positively correlated, when each portfolio's return is positively correlated with the other's
rebalancing trades, and when the two portfolios' rebalancing trades are positively correlated.**
Comparing *similar* books is statistically easier than comparing dissimilar ones — the paired
structure, not the effect size, is what buys the power.

## Construction recipe

Not a strategy; a comparison procedure. To compare two books `A` and `B` when trading is charged:

1. **Classify the cost function first.** Is the charge per unit traded independent of the amount
   traded (proportional) or increasing in it (price impact)? Nothing else in the procedure can be
   chosen before this.
2. **Proportional:** compute each book's return **net of costs**, then compare maximum squared
   Sharpe ratios exactly as in the no-cost case. One number per book; no risk-aversion parameter;
   scale-free.
3. **Price impact:** fix `γ` (absolute risk aversion) and the capital deployed, estimate the
   per-stock impact parameters into `D`, form `Λ* = X̃′ D X̃` in the space of the books being
   compared, and compare `μ′(Σ + Λ*/γ)⁻¹μ`. Report the comparison **as a function of `γ`**, because
   the ranking can and does change with it.
4. **Test the difference** with their nested/non-nested asymptotics rather than eyeballing the two
   utilities; expect more power when the books trade similar names in similar directions.
5. **Do not shortcut step 1 by assuming proportional.** Their motivation is empirical: for large
   institutions, price impact — not spreads — is the dominant component of trading cost.

## Robustness evidence (qualitative only)

- **Proposition 3 is a proof** and carries to any superlinear cost function, any market, any
  sample. The equivalence of their criterion to net squared Sharpe under proportional costs is
  likewise algebraic.
- **The empirical half is the weak half, and it is not used below.** One market, one recent sample
  that overlaps this lab's validation window, one impact-cost specification, no replication, and a
  citation count too low to carry information. Its qualitative lesson is nevertheless mechanism-like
  and is recorded without numbers: **which model wins can invert once costs are charged, and
  turnover alone does not predict the inversion — the *liquidity of the names each model has to
  trade* matters independently.** A model whose factors tilt toward smaller, less liquid stocks pays
  more per unit of turnover.
- **Second qualitative finding, also recorded without numbers.** The ranking depends on risk
  aversion: a high-dimensional many-factor model wins only at low absolute risk aversion, because
  that is where the cost term's weight relative to variance is highest and trading diversification
  across many factors pays most. The authors tie this to DeMiguel–Martín-Utrera–Nogales–Uppal's
  trading-diversification result, which this folder already holds.
- **Known limitation the authors state.** Quadratic impact is an assumption, not a measurement;
  their Definition 2 covers any superlinear shape but the empirics use the quadratic one.

## Implementability here

- **The headline is a scope statement, and it says the lab is in the easy regime — for a reason
  that is a property of the protocol, not of the world.** Protocol v3 charges, per name, a liquidity
  tier (bps per side from trailing median USD volume) plus the listing market's transaction tax.
  Every one of those is **proportional**: the charge per dollar traded does not increase with the
  size of the trade, and the protocol has no notion of deployed capital. By this paper's own
  equivalence, the lab is therefore in the regime where **net squared Sharpe is a sufficient
  statistic, the comparison is scale-free, and no risk-aversion parameter is needed.** v3's skill
  statistic — a difference of net Sharpe ratios — is thus internally coherent, and the
  `Which Alpha?` algebra applies to it **on net returns** with nothing added.
- **The flip side, stated as a protocol-level consequence rather than a task.** That coherence is
  purchased by the cost model's shape. If price impact were ever added — or if the liquidity tier
  were made to depend on trade size rather than on the name — then *(i)* "skill" would stop being
  scale-free and would require a stated book size and risk aversion, *(ii)* the efficient frontier
  would be concave, so two candidates could swap order depending on the assumed capital, and
  *(iii)* books tilted toward illiquid names would be penalised far more steeply than the current
  40-bps bottom tier penalises them. This is an `engine/`-level observation and the learning agent
  may not act on it; it belongs in the human's queue beside `#217`.
- **It gives the lab's refuted illiquidity premium a second, independent reason to stay refused.**
  `experiments/learnings.md` (2026-10-13/14) records a within-market price-impact premium real on
  train and absent on validation, and explicitly refuses to flip the sign to trade the liquid half.
  This paper's empirical lesson — that the liquidity of the names traded matters *beyond* turnover —
  says the v3 cost model, having no impact term, **understates** the cost of the illiquid book
  rather than overstating it. So the negative is robust to the cost model being made more realistic,
  and the only direction the cost model could move is against that candidate.
- **The transferable construction idea is the covariance identity, and it is cheap.** `(Σ + Λ)⁻¹μ`
  says that penalising turnover inside a selection step is formally the same as inflating the
  covariance matrix along the directions that are expensive to trade. The lab already has the
  constraint-side version of this statement
  (`notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`: a binding weight constraint
  *is* a covariance shrinkage), so the pair is now complete: **constraints and trading costs both
  enter a mean-variance problem as covariance modifications.** For a long-only book under
  proportional costs the practical form is not a matrix inverse at all — it is the no-trade band the
  lab has already measured as its one construction win
  (`notes/2026-10-08-no-trade-bands-under-proportional-costs.md`), and this paper explains why the
  band and not a quadratic penalty: the band is the optimal policy for *proportional* costs, the
  `(Σ + Λ)⁻¹` partial move is the optimal policy for *quadratic* ones, and v3 has the former.
- **What this does not license.** No candidate, no trial, and no change to how costs are charged.
  The note's whole content is: the comparison statistic the lab already uses is the right one *given
  the cost model it has*, and the reason is a proposition rather than a convention.
- **Family placement.** Cross-family methodology; `portfolio-learning` if filed under one.

## Related

- `notes/2026-10-14-which-alpha-the-sufficient-statistic-for-beating-a-benchmark.md` — the
  no-cost criterion whose scope this note fixes.
- `notes/2026-10-14-net-expected-returns-of-the-anomaly-zoo.md` — the third link in tonight's
  chain: what the net statistic's *level* turns out to be once it is computed honestly.
- `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — the constraint-side version of
  the same "it enters as covariance" identity.
- `notes/2026-10-08-no-trade-bands-under-proportional-costs.md`,
  `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the policy that the
  proportional-cost shape actually implies, and the lab's measured win from it.
- `notes/2026-08-20-trading-diversification-combining-signals.md` — the trading-diversification
  result this paper's `Λ*` makes algebraic, and which its high-dimensional model is built on.
- `notes/2026-08-27-market-impact-functional-form-and-trade-rate.md`,
  `notes/2026-08-27-live-execution-costs-implementation-shortfall.md` — where the superlinear shape
  comes from, and what it costs in practice.
- `notes/2026-09-23-spanning-under-short-sales-and-costs.md` — the other place this folder has had
  to ask what costs do to a spanning comparison.
