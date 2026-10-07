---
title: "Is it the weather? — the full JBF exchange, and why the hemisphere sign test cannot settle it"
authors: Jacobsen, Marquering (critique, 2008; response, 2009); Kamstra, Kramer, Levi (comment, 2009)
year: 2008; 2009; 2009
venue: Journal of Banking and Finance 32(4), 526–540; JBF 33(3), 578–582 (Comment); JBF 33(3), 583–587 (Response) — Tier 1/2, peer-reviewed, all three
url: https://doi.org/10.1016/j.jbankfin.2007.08.004 · https://doi.org/10.1016/j.jbankfin.2008.09.013 · https://doi.org/10.1016/j.jbankfin.2008.09.011
citations: "Jacobsen–Marquering 2008 — 152 (Crossref `is-referenced-by-count`, checked 2026-10-05); 105 (Semantic Scholar, checked 2026-10-05). Kamstra–Kramer–Levi Comment — 27 (Crossref) / 37 (Semantic Scholar) / 28 (OpenAlex), checked 2026-10-05. Jacobsen–Marquering Response — 37 (Crossref) / 47 (Semantic Scholar) / 43 (OpenAlex), checked 2026-10-05."
sample_period: "1970-01 to 2004-05 (MSCI value-weighted country indices, monthly; many country series start 1988 or later). Both the critique and the Comment work on this same panel."
markets: 48 countries, MSCI value-weighted total-return indices; 7 of them Southern Hemisphere; 10 of them within 20° of the equator
tier: "B for the exchange as a body of evidence. Both sides are Tier-1/2 venues and the critique is well cited, but the central empirical claim of the critique could not be replicated by the authors it criticises, and the Comment's own counter-estimates have never been independently replicated either. Nothing here should be treated as settled fact; the **methodological** content below is what survives, and it is Tier A in the sense that both sides agree on it."
validation_overlap: false
published_post_2018: false
read: "Kamstra–Kramer–Levi **Comment in full** (TSpace pre-print of the published JBF Comment, `utoronto.scholaris.ca`, typeset and complete with abstract, four sections and reference list). Jacobsen–Marquering's argument **in full from the 2004 ERIM working-paper version** (`repub.eur.nl/pub/1816/`, 30pp) of what became the 2008 JBF article — same abstract wording as the published record, so the argument is first-hand, but table-level detail may have moved between the WP and the published version and nothing below depends on a table number. Jacobsen–Marquering's 2009 **Response was NOT read** (SSRN 403)."
---

## Access, and a correction to this folder's own record

**The DOI this folder recorded on 2026-10-04 as "a published response by Kamstra–Kramer–Levi" is
not theirs.** `10.1016/j.jbankfin.2008.09.011` resolves at Crossref to *"Is it the weather?
**Response**"* by **Jacobsen and Marquering**, JBF 33(3), 583–587. The exchange has three parts,
not two, and they sit consecutively in one 2009 issue:

| Piece | Authors | DOI | Pages | Read? |
|---|---|---|---|---|
| *Is it the weather?* | Jacobsen, Marquering | `10.1016/j.jbankfin.2007.08.004` | 32(4), 526–540 | argument read, from the 2004 ERIM WP |
| *Is it the weather? **Comment*** | Kamstra, Kramer, Levi | `10.1016/j.jbankfin.2008.09.013` | 33(3), 578–582 | **yes, in full** |
| *Is it the weather? **Response*** | Jacobsen, Marquering | `10.1016/j.jbankfin.2008.09.011` | 33(3), 583–587 | **no** |

The Comment's DOI was not in this folder at all and was found by a Crossref *journal* query
(`api.crossref.org/journals/0378-4266/works?filter=from-pub-date:…&query.bibliographic=weather+comment`)
after a title search failed. **That query form is the transferable find**: when you know the
journal and the year of a comment-and-reply pair, enumerate the issue rather than searching the
title, because a reply's title is a near-duplicate of the article's and ranks badly.

Three channel results, two of them new:

- **`utoronto.scholaris.ca` served the Comment on the first try**, reached from OpenAlex's
  `locations[].landing_page_url` list. Second consecutive night this host has served a closed
  Tier-1/2 article's full text; it is now a confirmed channel, not a lucky hit.
- **`repub.eur.nl` DOES serve files, and the 2026-10-04 entry saying otherwise needs narrowing.**
  That entry recorded "a Pure record named a handle that resolved to a landing page with no
  bitstream link at all". True of the handle route; **not** true of the direct path. RePEc's
  record page for the ERIM working paper (`ideas.repec.org/p/ems/eureri/1816.html`) names the exact
  file, and `repub.eur.nl/pub/<id>/<filename>.pdf` returned HTTP 200 with a parseable 30-page PDF.
  **The lesson is to read the download URL out of the RePEc record rather than to resolve the
  handle.**
- **SSRN again refused the automated client** (HTTP 403, 5.6 KB Cloudflare body) on the
  `Delivery.cfm` URL that OpenAlex lists as the Response's only green location, so the Response is
  recorded as unread. **A sixth and seventh clean Semantic Scholar `not found` for real, indexed
  DOIs** showed up tonight on two unrelated papers (see the other two notes); Crossref was again
  never rate-limited.

## Mechanism — what the two sides are actually arguing about

Neither side disputes the **existence** of a six-month seasonal in international equity index
returns; the critique states in its own abstract that it *confirms* it. The argument is entirely
about **identification**: whether a variable with an annual summer/winter shape, fitted to returns
with an annual summer/winter shape, is evidence of the mechanism that variable is named after.

**The critique's argument is a placebo argument, and that is the whole of its force.** Jacobsen and
Marquering take two variables with no plausible causal channel to equity risk premia — **US monthly
ice-cream production** (with a one-month lag, on the stated pretext that ice cream is a comfort food
and comfort-food consumption proxies depressed mood, hence risk aversion) and **detrended monthly
outbound UK airline travel** (pretext: vacationers do not trade) — and show that each "explains" the
same seasonality in most of the 48 countries, with the right sign and wide significance; airline
travel carries the predicted negative sign in *every* country in their panel. Their conclusion is
not that daylight is irrelevant but that **the time-series fit is uninformative**: any regressor with
a strong annual shape will produce it, so the weather–return correlation "might be spurious" and the
mood reading is "premature".

They add two cross-sectional checks against the mechanism and both come out against it: the fitted
SAD and temperature coefficients get **larger, not smaller, closer to the equator** (they single out
Singapore, whose monthly temperature standard deviation is under one degree, and Colombia and
Malaysia for daylight), and Southern-Hemisphere countries show **the Northern phase**, not the
reversed one — of their seven Southern-Hemisphere markets, four have a statistically significant
SAD coefficient of the *wrong* sign for the mechanism, while no Northern market does.

**The Comment's reply is that the critique's regression cannot test the mechanism at all**, on five
specific grounds, and these are the part worth carrying:

1. **A half-year dummy and a length-of-night variable are not rival explanations in one
   regression — the dummy nests the other's low-frequency content.** The critique's headline is that
   adding a Nov–Apr dummy kills the SAD variable's significance. KKL's position is that this is what
   a nesting regressor does, not a refutation.
2. **The critique dropped the fall dummy, and the mechanism is not testable without it.** KKL's
   model is a *flow* model, not a *stock* model: what moves prices is the rate at which holders
   become more (or less) risk-averse, not how many are affected at a point in time. Clinically,
   **onset peaks in September–October and recovery peaks in March**, so the prediction is **negative
   fall returns and positive winter-into-spring returns** — returns *shifted* across the year, not
   created. A specification with a single daylight term and no fall term restricts those two to be
   equal and cannot express the hypothesis. (This also answers the "depression peaks in
   December–February, not in the fall" objection: peak *stock* is the wrong moment.)
3. **Ten of the critique's 48 countries lie within 20° of the equator**, where the annual daylight
   swing is about ±1 hour, and the mechanism predicts nothing there. Including them, plus markets
   that experienced hyperinflation in-sample and markets dominated by a single commodity, loads the
   panel with countries where the null is the hypothesis.
4. **An orthogonalisation that favours one hypothesis.** KKL report (after corresponding with the
   authors, and say the detail is absent from the published paper) that the critique's world-index
   control is first orthogonalised with respect to the **sell-in-May dummy only**. A market return
   contains both seasonals; purging it of one and not the other mechanically advantages the one
   purged. If a market return is used at all, it must be orthogonalised with respect to **every**
   seasonal variable under test.
5. **Monthly data for a daily-varying regressor**, plus ad-hoc month dummies (a January dummy
   applied to countries whose tax year does not start in January; an October dummy for an anomaly
   KKL say no literature documents) that absorb exactly the months where the mechanism's action is.

KKL also report that **the critique's latitude table contains arithmetic errors** — latitudes
printed with more than 60 minutes in a degree. **I verified this directly in the working-paper
version's Table 1**, which lists entries of the form `33°85'S`, `50°80'N`, `55°68'N` and one
malformed `4896'N`. It is a small thing and KKL treat it as such, but it is checkable and it checks
out.

**What KKL concede, and it is the most important sentence in the exchange for this lab.** In the
Comment's own words, *"even southern hemisphere exchanges are somewhat problematic to the extent
that international equity markets are integrated and northern hemisphere investors (who comprise the
bulk of international wealth and investors) dominate mature markets like New Zealand and Australia.
(This likely explains the somewhat weaker results we found in the southern hemisphere countries we
originally considered.)"*

**And the critique says the same thing, unprompted, about its own strongest result**: *"due to cross
correlation between countries, temperature and SAD effects in for instance the United States might
be 'exported' to other parts in the world and be stronger than local reversed effects. It could well
be that a Northern Hemisphere SAD effect is imported to Australia…"*

## Construction recipe

Nothing new to build from the exchange itself; what it supplies is a **replacement specification**
and a **replacement discriminator**.

**The specification KKL now recommend over their own 2003 one.** They state that the length-of-night
variable plus fall dummy should be superseded by a single regressor built from the **clinical
incidence of SAD onset and recovery** in affected populations — no trigonometry, no ad-hoc fall
dummy — and that it performs at least as well. They name a public source for the series at daily and
monthly frequency (an author page; this folder has not fetched it and makes no claim it is still
live). For this lab the practical content is the *shape*, which the Comment states in words and
which can be written down without the file: **a variable that is negative through the onset window
peaking around September–October, crosses zero around the turn of the year, and is positive through
the recovery window peaking around March.**

**The discriminator the Comment supplies, and it is new to this folder.** KKL state the mechanism's
cross-asset implication explicitly: if the channel is **time-varying risk aversion**, then *low-risk*
securities must show the **opposing** seasonal to equities — higher returns on safe assets exactly
when SAD-affected holders are shunning risky ones. They cite their own companion work on Treasury
returns and on mutual-fund flows between safe and risky categories as having found it.

That is a **within-market, cross-risk-level** prediction. It does not involve hemispheres, latitudes
or cross-listing, and the integration escape clause above **cannot neutralise it**: integration
exports the *timing* of a Northern seasonal to other places, but it gives no reason for safe and
risky assets *in the same place* to seasonalise in opposite directions. A plain calendar dummy
predicts no risk gradient at all — it is a shift in the index, so it should appear with the same sign
in everything the index contains.

## Robustness evidence (qualitative only)

- **The critique's headline result failed replication by the authors it criticises.** KKL report
  that, estimating the critique's own model on the critique's own data at the critique's own
  frequency, they recover **systematically larger** SAD coefficients and t-statistics, with several
  major markets significant where the critique reports them insignificant. No third party has
  adjudicated this, and the Response (unread here) is presumably where the critique answers it.
  **Record the exchange as unresolved on its central empirical claim, in both directions.**
- **The placebo result is not in dispute and nobody has tried to rebut it.** KKL's Comment does not
  contest that ice-cream production and airline travel fit the seasonal; it contests what follows
  from the daylight regression, not the placebos. Treat the placebo finding as the sturdiest fact in
  the exchange.
- **Both sides agree the hemisphere test is confounded by market integration** (quotations above).
  That agreement is the single most robust thing in this literature about the Southern Hemisphere and
  it is a *negative* result about a test, not a result about markets.
- **The two sides also agree on the underlying seasonal's existence**, which is why neither of them
  is evidence for or against the six-month effect this folder records separately.

## Implementability here

**First: #193 as this folder stated it on 2026-10-04 is not a valid discriminator, and the entry
claiming it "cannot come back ambiguous" should be read as withdrawn.** That entry's argument was
that the daylight mechanism requires a *negative* Southern Nov–Apr coefficient while a plain calendar
effect requires a *positive* one, so the sign identifies. **Both sides of the literature state in
print that it does not**, for the same reason, and each states it about their own preferred
conclusion. A positive Southern Nov–Apr coefficient on this universe is predicted by the calendar
theory directly *and* by the daylight theory via importation, so the measurement has no power.

The point bites harder here than in either paper, because **this universe is close to the worst
available panel for that test**: it is global, dividend-adjusted, **USD-converted**, ETF-heavy and
built from current large-cap constituents — i.e. exactly the names and the wrapper through which
Northern capital holds Southern markets. Whatever residual power the test has in a panel of 48 local
indices, it has less here.

**The measurement is still worth taking — but as a description, not as a test, and its cost is the
honest reason to take it.** Splitting the panel by listing hemisphere and reading the Nov–Apr mean
difference in each subset costs no trial and tells the lab whether its own seasonal leg is a global
constant or a Northern one, which matters for *any* calendar construction. State before running it
that **neither sign refutes anything** — otherwise a positive Southern coefficient will be written up
as a kill it cannot support.

**Second: #194's licence is weaker than it looked, and the honest statement is that it has none from
this literature.** The cross-hemisphere rotation was admissible as a candidate *because* a free sign
test was going to decide whether its destination existed. With the test disarmed, the rotation is a
two-bets-a-year calendar trade with no surviving identification, no cross-sectional breadth
(`2026-08-19-fundamental-law-breadth-and-strategy-risk.md`) and a prior that already leans against it
from this lab's own pooled measurement. **Do not build it.** The rotation's one genuine virtue — that
it never holds cash, so it sits outside both of the lab's calendar closures — is an argument about
*constraints*, not about *signal*, and it does not supply the missing destination.

**Third, and this is the thing to actually build if the family is worked at all: the risk-gradient
test.** The mechanism is a claim about the price of risk, so it predicts a **monotone gradient in the
seasonal across risk levels within the same market**, and the plain calendar dummy predicts none.
Concretely, on the Northern subset of this universe and on train only: sort names by a risk proxy
the lab already computes and trusts (trailing beta to the universe, or a range-based volatility from
`strategies/lib/features.py`), then estimate the same Nov–Apr mean difference **inside each bucket**.

- A seasonal that **rises monotonically with the risk proxy** is the risk-aversion signature, and it
  is also immediately a *construction*: overweight low-risk names in the onset window and high-risk
  names in the recovery window, gross 1.0 throughout, **no cash leg** — a rotation along the risk axis
  rather than the hemisphere axis.
- A seasonal that is **flat across buckets** says the effect is a level shift in the index, which is
  what the critique argues, and closes the mechanism on this universe for good.

Four cautions, and the first is disqualifying if ignored.

1. **Run a placebo, and pre-register it.** This is the critique's whole contribution and it applies
   to the risk-gradient test exactly as it applies to the daylight regression: *any* annual-shaped
   regressor will fit. The gradient across risk buckets is the discriminating quantity — the
   significance of the seasonal *within* any one bucket is not evidence of anything. The lab has the
   habit already (`experiments/learnings.md` records a seasonal leg surviving its own placebo); this
   is the same discipline arriving from the literature rather than from the board.
2. **The lab's existing volatility sort is survivorship-contaminated on this universe and the
   learnings file says so.** A risk-bucket split inherits that contamination. Prefer **beta to the
   universe** over a volatility *level*, and prefer **ETF-level buckets** where the universe allows,
   per `program.md`'s own ranking of what is trustworthy here.
3. **Do not re-use the monotonicity claim without a monotonicity test.**
   `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` exists for precisely the shape of claim
   this test makes, and the daylight paper's own latitude gradient is the cautionary example: asserted
   over nine countries, never tested.
4. **Carry `2026-09-10-currency-component-in-usd-converted-returns.md` into any of this.** On a USD
   panel a seasonal in a non-US sleeve is partly a seasonal in a currency, and both sides of this
   exchange were working on local or MSCI-USD index returns without that decomposition.

**What definitely does not transfer.** Nothing about latitude weighting (the 2026-10-04 anti-candidate
stands and the Comment strengthens it: KKL themselves now prefer a different regressor). Nothing
about temperature. And no magnitude from either side — the whole exchange is about whether the
magnitudes mean what they are named after.

## Related

- `2026-10-04-sad-daylight-seasonal-mechanism.md` — the primary this exchange is about; its
  "Robustness evidence" section records the Response as unread and mis-attributes its DOI, and its
  "Implementability" section proposes the hemisphere screen this note withdraws. **Read this note
  after it.**
- `2026-10-04-halloween-six-month-seasonal.md` — the effect both sides agree exists, and the
  108-market replication whose Southern-Hemisphere coefficients this note re-reads.
- `2026-09-02-return-seasonalities-common-factors.md`, `2026-08-29-same-calendar-month-seasonality.md`
  — the cross-sectional seasonality literature, which is a different object and is not touched by
  this exchange.
- `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — the test the risk-gradient construction
  needs and the latitude claim never got.
- `2026-09-10-currency-component-in-usd-converted-returns.md` — the precondition for reading any
  regional or hemispheric seasonal on this panel.
- `2026-10-01-limits-of-p-hacking-publication-bias.md` — the general form of the critique's placebo
  argument; this is a concrete, published instance of it with two deliberately absurd regressors.
- `experiments/learnings.md`, [Measured 2026-09-01] and [Measured 2026-09-02] — the two calendar
  closures, and the pooled Nov–Apr measurement that the hemisphere split was supposed to decompose.
