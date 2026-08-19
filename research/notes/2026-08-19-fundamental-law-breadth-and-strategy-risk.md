---
title: "The Fundamental Law of Active Management" + "The fundamental law of active management: Redux" (with the author's earlier working-paper derivation)
authors: Grinold (1989); Ding, Martin (2017); Ding (2010, working paper "The Fundamental Law of Active Management: Time Series Dynamics and Cross-Sectional Properties")
year: 1989, 2017, 2010
venue: Journal of Portfolio Management 15(3), 30–37 (venue tier 1 practitioner-academic); Journal of Empirical Finance 43, 91–114 (venue tier 1, peer-reviewed, open access); author-hosted working paper (venue tier 3)
url: https://doi.org/10.3905/jpm.1989.409211 ; https://doi.org/10.1016/j.jempfin.2017.05.005 ; https://math.nyu.edu/inmemoriam/avellaneda/FundamentalLawFT.pdf
citations: Grinold (1989) 311 (Semantic Scholar by DOI, checked 2026-08-19); Ding–Martin (2017) 15 (Crossref cited-by, checked 2026-08-19 — not indexed by the Semantic Scholar DOI endpoint, and OpenAlex's daily budget was exhausted this session)
sample_period: theory, market-agnostic. The working paper's empirical calibration of one nuisance parameter uses Russell 1000/2000/3000 universes, 1978-12 to 2009-08. The published version's empirical study sample was NOT verified — only its first two pages were readable.
markets: US equity universes for the calibration; the derivation itself is market-agnostic
tier: A on Grinold's standing and on the algebra of the generalisation; B on the Redux paper's empirical study, which was not read
validation_overlap: false
published_post_2018: false
---

## Mechanism

Where the bagging literature answers "why does averaging perturbed fits help?" in
prediction-error vocabulary, this literature answers the same question in portfolio
vocabulary, and it does something the lab needs more: it says **which term in the
risk-adjusted-return identity a given design change actually moves.**

Grinold's law states that an active portfolio's information ratio is approximately

```
IR ≈ IC · √BR
```

where `IC` is the information coefficient (the correlation between the signal and subsequent
residual returns — "skill") and `BR` is **breadth, the number of independent forecasts of
exceptional returns made per year.** Grinold presents it as an approximation "based on
assumptions that are not quite true", and the accompanying result — alpha equals residual
volatility times IC times score — is what turns a standardised score into a position size.

The law's practical history is a cautionary tale about the word *independent*. Grinold
himself discusses at length that only independent bets may be counted; practitioners
routinely substitute the number of names in the universe, and the resulting predictions are
wildly optimistic. Ding gives the worked arithmetic: a signal with a monthly IC of 0.03 over a
1000-name universe implies an annualised IR of 3.29, against Grinold's own remark that an
observed IR above 1.5 is rare. Two independent corrections have been proposed, and they act on
different parts of the formula:

**(a) Constraints leak IR — the transfer coefficient.** Clarke, de Silva and Thorley
generalise the law to `IR ≈ TC · IC · √BR`, where the transfer coefficient `TC` is the
cross-sectional correlation between risk-adjusted expected residual returns and risk-adjusted
active weights — i.e. how faithfully the signal survives the trip into actual portfolio
weights. Constraints named as costing TC include sector/country exposure limits and,
explicitly, **long-only**. Their simulations put typical TC in the **0.3–0.8** range, which is
where the practitioner rule of thumb "halve whatever the fundamental law tells you" comes
from. *(Clarke et al. is not open-access and was not read first-hand this session; these
statements are as reported by Ding, who follows their framework and notation.)*

**(b) Skill is not constant, and its variance is the binding term — "strategy risk".** The
original law assumes the IC is the same across securities and constant over time. In practice
the realised cross-sectional IC fluctuates around its mean. Qian and Hua named this **strategy
risk** and derived the limiting form `IR = mean(IC) / σ_IC`. Ding's generalisation nests both:

```
IR = mean(IC) / sqrt( σ_IC² + φ/N ),      φ ≥ 1
```

with `N` the number of assets and `φ` a nuisance constant reflecting dispersion in residual
volatilities. The three special cases are worth memorising because they are the whole story:

- `σ_IC = 0` (skill perfectly constant) recovers Grinold: IR grows as `√N`, without limit.
- `N → ∞` recovers Qian–Hua: **IR → mean(IC)/σ_IC — an absolute ceiling that no amount of
  breadth can breach.** Ding calls it "the Chinese Wall": as long as `IC/σ_IC` does not
  improve, performance does not improve however much breadth is added.
- Intermediate `N`: the idiosyncratic term `φ/N` diminishes as the universe grows, so the
  marginal value of breadth falls away and `σ_IC` takes over as the dominant term.

Ding's own one-line summary is the usable form: **"play often (increase N) when N is small,
but play precisely (low σ_IC) and play well (high IC) when N is already large"** — and his
stated headline result is that *variation in IC has a much bigger impact on IR than breadth
does for a typical investment universe.*

## Construction recipe

There is no strategy to build here; the law is an accounting identity for where risk-adjusted
return comes from. What it prescribes is a **decomposition to apply to a design change before
committing to it**. Any proposed modification moves one or more of four quantities:

| Term | What raises it | What the law says about the payoff |
|---|---|---|
| `mean(IC)` | a better signal | linear in IR; the only unbounded lever |
| `σ_IC` | *reduced* by averaging weakly-correlated skill draws | dominates IR once `N` is moderate; the ceiling term |
| `N` | more instruments, more *independent* bets | `√N`, saturating; worthless once `φ/N ≪ σ_IC²` |
| `TC` | fewer binding portfolio constraints | linear scalar; 0.3–0.8 typical under real constraints |

Two construction cautions inside the framework itself. First, breadth must count *independent*
forecasts: two dependent bets are not two bets, and neither source offers a tractable recipe
for counting them in practice — Ding calls this "still not a straightforward exercise". Second,
the derivations assume active weights come from quadratic-utility optimisation using a
conditional mean forecast and the *matching* conditional forecast-error covariance matrix.
Ding's central methodological complaint about the earlier literature is that practitioners
pair an alpha model with a third-party risk model that is detached from it, which is precisely
why their ex-ante tracking error and ex-post tracking error disagree.

## Robustness evidence (qualitative only)

- The law itself is a derivation, not an empirical regularity, so it does not decay. What has
  changed over three decades is the derivation's *assumptions*, in a clear direction: each
  successive paper (Clarke et al.; Qian–Hua; Ye; Ding–Martin) relaxes one unrealistic
  assumption and each time the predicted IR comes **down**. That monotone direction of
  revision is itself the most useful robustness fact here.
- Ding–Martin is peer-reviewed and open-access, and positions itself as nesting the prior
  versions as special cases. Its citation count is low in absolute terms (15 by Crossref);
  the underlying Grinold result is the heavily cited one, and the ideas the note leans on
  (transfer coefficient, strategy risk) each have their own primary sources.
- Weakness, recorded rather than smoothed: the *empirical* half of Ding–Martin — a comparison
  of factor-model choices — was not readable this session (ScienceDirect serves a bot
  challenge, as documented in `research/README.md`), so only the framing, the literature
  review and the derivation's logic are first-hand, the last via the author's earlier working
  paper. Nothing in this note rests on the published paper's empirical results.
- Grinold (1989) itself was not read first-hand (paywalled practitioner journal). Its formula,
  its "count only independent bets" caveat and its "IR above 1.5 is rare" remark are all
  quoted here from Ding's direct citations of it, with page references in the source.

## Implementability here

**1. This is the cleanest available account of the lab's temporal-breadth result, and it says
the lab has been describing the mechanism with the wrong noun.** The repo's records read
"breadth only pays when it comes from decorrelated formation dates, not from more names chosen
at one date", with nominal breadth widening measured as a no-op. Under this identity those are
two different terms of the same formula. Adding names at one date raises `N` — a `√N` lever
that has already saturated on a ~145-instrument universe, where `φ/N` is small relative to a
plausible `σ_IC²`. Averaging the *same* selection procedure across weakly-correlated formation
dates does not raise `N` at all; it averages several draws of the realised IC, which lowers
**`σ_IC`** — the term that dominates IR once `N` is moderate, and the term that sets the hard
ceiling. So the lab's two measurements are not a puzzle; they are two levers of very different
marginal value, and the literature says which is which. **Flag: the mapping from "formation
vintages" to "draws of IC" is the lab's inference. Neither source discusses tranching,
overlapping formation dates, or portfolio averaging of any kind.**

**2. It hands the existing decorrelation diagnostic a quantitative target rather than a
threshold.** The lab already gates vintage-diversity ideas on rank correlation between score
vectors (0.66 passed, 0.89 killed an ensemble). Under this framing the gate is measuring
exactly the right thing for the right reason: the `σ_IC` of an equal-weighted average of `K`
vintages falls with the average *pairwise correlation* of those vintages' ICs, and falls not at
all if they are perfectly correlated. That converts "correlation must be low enough" from a
rule of thumb into a statement about which term of IR is being bought.

**3. A hard warning against a tempting free diagnostic.** The natural next move is "just
measure the per-vintage IC series and its standard deviation". **That is not a free
holdings-only diagnostic — it scores returns.** The lab's exemption for cheap diagnostics
covers statistics of the weight matrix and of trigger firing dates, which touch no returns.
Computing an IC requires correlating scores with subsequent returns, which is a
signal-evaluation on a data split and should be treated with the same discipline as a
backtest. Recorded explicitly so a future session does not smuggle a return-scoring exercise
in under the diagnostic exemption.

**4. The long-only constraint has a name and a number now.** `TC` between 0.3 and 0.8 under
realistic constraints, with long-only named among the constraints that cost it. The repo runs
long-only, gross ≤ 1.0, ≤25% per position — the tighter end of that range. This is the
quantitative form of the folder's standing "long-short results do not transfer by default"
principle, and it is the more useful form: the leak is a *multiplicative scalar on IR*, not a
change of sign, so a long-only implementation of a sound cross-sectional signal is expected to
be weaker, not broken. (The two cases already recorded where a long-short mechanism does not
merely weaken but disappears — momentum crash management, time-series momentum "crisis alpha" —
remain the separate and more serious category: there the mechanism lives in the short leg, and
no transfer coefficient describes that.)

**5. Do not import any IR number, and do not read "IR above 1.5 is rare" as a comment on the
champion.** The entire framework is *benchmark-relative*: IC is measured against residual
returns after removing beta-adjusted benchmark returns, and IR is active return over tracking
error. The repo's gate scores the **total** net Sharpe of a fully-invested long-only book,
which includes the market risk premium and market volatility. The two statistics are not
comparable, and a champion Sharpe above 1 is not evidence of anything unusual under this
literature. Record this before someone reads the ceiling result as an alarm.

**6. The framework's own machinery is the expensive kind, and should not be adopted.** The
derivations assume mean-variance-optimal active weights from a conditional forecast-error
covariance matrix — exactly the noisily-estimated-parameter class the folder's first candidate
screen rules out, and the class that produced both of the lab's inverse-vol refutations. Use
this literature as a **decomposition for reasoning about where a change acts**, never as a
construction recipe.

## Related

- `notes/2026-08-19-bagging-averaging-unstable-predictors.md` — the same question in
  prediction-error vocabulary. The two accounts agree on the precondition (the averaged
  components must be less than perfectly correlated) and disagree in scope: Breiman requires
  the base procedure to be *unstable*, this literature requires only that skill be
  *time-varying*, which is weaker and always true.
- `notes/2026-08-17-averaging-over-estimation-windows.md` — the third account of the same lab
  mechanism, from forecasting under structural breaks.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — why the conditional-covariance machinery
  this framework assumes should not be built here.
- `notes/2026-08-17-cross-sectional-vs-time-series-construction.md` — the other place where
  naming the right benchmark decides what a measured gap means.
- `experiments/learnings.md`, entries on overlapping formation tranches and on lookback-length
  vintage diversity — the results this note reinterprets.
