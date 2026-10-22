---
title: "Regime Changes and Financial Markets" — what a Markov-switching model buys in asset returns, why the number of regimes is almost never tested, and the filtered-versus-smoothed distinction that makes most published regime pictures unusable in a backtest
authors: Ang, Timmermann
year: 2012
venue: Annual Review of Financial Economics 4, 313–337 (venue tier 1–2 — an invited Annual Review survey; read here in the NBER working-paper version, venue tier 2)
url: https://doi.org/10.1146/annurev-financial-110311-101808
citations: 371 (Crossref `is-referenced-by-count`, checked 2026-10-22, resolved on the first call)
sample_period: a survey; its own illustrative estimates use monthly U.S. equity, interest-rate and foreign-exchange series ending before the working paper's June 2011 circulation date, and the literature it reviews is pre-2011 throughout. No sample in it can touch 2018–2023.
markets: U.S. equities, U.S. interest rates, foreign exchange; the surveyed literature additionally covers international equity allocation
tier: A
validation_overlap: false
published_post_2018: false
read: full text of the NBER working-paper version, `nber.org/system/files/working_papers/w17182/w17182.pdf` (NBER WP 17182, June 2011; 272 KB → 86 KB of clean text via `pdftotext -layout`, 455 instances of `" the "`, no ASCII shift, no `( )` math dropout, title and author lines verified). The published Annual Review version was not obtained; section numbering below is the working paper's. **Hansen (1992)**, the standard reference for the non-standard likelihood-ratio problem discussed here, was **not obtained** — `users.ssc.wisc.edu/~bhansen/papers/jae_92.pdf` fetched cleanly (2.4 MB) but is a text-layerless scan and was not rendered; its Crossref record resolves (`10.1002/jae.3950070506`, Journal of Applied Econometrics, **593** citations, checked 2026-10-22) and it is cited below only as Ang–Timmermann cite it.
---

## Mechanism

This is the second half of the regime vein — the branch where the regime is a **latent state** that
persists and recurs, rather than a one-way break at a date. The canonical object is Hamilton's
Markov-switching model: an unobserved state `s_t ∈ {0,…,K−1}` evolves as a Markov chain with
transition matrix `P`, and the observed return is drawn from a distribution whose parameters depend
on `s_t`. Estimation is by maximum likelihood with a Bayesian filtering recursion (or by Gibbs
sampling, after Albert–Chib and Kim–Nelson).

**What the model is actually good at, and it is not timing.** The authors' case is a *descriptive*
one, and it is strong: a two-state switching model with constant parameters inside each state
mechanically reproduces a long list of return features that a single-state model cannot — fat
tails, heteroskedasticity, skewness, volatility clustering, and time-varying correlations. Their
own illustrative estimates make the point concrete in a way worth carrying: the fitted model
implies a **first-order autocorrelation in squared returns of about 0.77 while the autocorrelation
in returns themselves is essentially zero**. Regime switching generates persistence in second
moments without generating predictability in first moments. That is a statement about what the
model can represent, not about what it can forecast, and the distinction is the whole note.

Two further general regularities the survey reports as robust across the literature rather than as
one study's finding:

- **The high-volatility regime carries the lowest expected return**, found "since the earliest
  studies of regime switches on equity returns". The high-volatility state has the lowest Sharpe
  ratio and the low-volatility state the highest.
- **Regimes are highly persistent** — both self-transition probabilities close to one — which is
  what produces volatility clustering, and which also means a correctly identified regime is worth
  something for several periods.

Taken together these look like an argument for regime-conditional allocation, and the survey makes
that argument. The rest of this note is about the gap between that argument and anything
implementable.

## Construction recipe

**The model.** For a two-state model: `r_t = μ_{s_t} + φ_{s_t} r_{t−1} + σ_{s_t} ε_t`, with
`Pr(s_t = i | s_{t−1} = i) = p_ii`. Free parameters: two means, two volatilities, optionally two
autoregressive coefficients, and two transition probabilities. Estimate by maximum likelihood over
the full visible window; the likelihood is evaluated by the Hamilton filter.

**Filtered versus smoothed — this is the operational heart of the note.** The filter produces
`Pr(s_t | I_t)`, the probability of the state at `t` given information **up to `t`**. The smoother
produces `Pr(s_t | I_T)`, the probability of the state at `t` given the **entire sample through
`T`**. The authors are explicit that their regime pictures are the latter: the smoothed
probabilities are described as "conditioning on the whole sample".

The consequence is a lookahead of exactly the kind this repo's `causality_check` exists to catch.
**A smoothed regime probability at date `t` is a function of returns after `t`.** Any backtest that
assigns a position using smoothed probabilities is reading the future, and will look excellent.
This is not a subtle failure mode — it is the single most likely way a regime-switching candidate
in this lab would produce a spectacular, wrong train result. And it is worth stating that most of
the *visual* evidence for regimes in the published literature, the charts where the shaded
high-volatility periods line up compellingly with remembered history, is smoothed. The compelling
alignment is partly a product of having seen the end of the sample.

**What the filtered version actually delivers, in the authors' own assessment.** They illustrate
the filter on a simulated path drawn from a known two-state process — i.e. the most favourable
possible case, where the model is correctly specified and the parameters are the true ones. Their
verdict: the filtered probabilities "track the underlying regime quite accurately, but at times
miss an important regime change and at other times issue false alarms", and they draw the
conclusion themselves — "this emphasizes the difficulty associated with real-time tracking of the
underlying regime". **Missed changes and false alarms, under ideal conditions, with the true
parameters known.**

**Choosing the number of regimes — there is no good way, and the survey says so.** The number of
regimes "is often difficult to determine from data and as far as possible the choice should be
based on economic arguments". The reason tests are avoided is a clean identification failure:
under the null of a single regime, **the parameters of the second regime are not identified**, so
there are unidentified nuisance parameters under the null and the likelihood ratio statistic is
**not asymptotically `χ²`**. Davies (1977), Hansen (1992) and Cho–White (2007) address this; the
practical consequence the authors report is that "it is not uncommon to simply fix the number of
regimes at some value, typically two, rather than basing the decision on econometric tests."

That is the same structural problem as the breakdate case in the companion note — a parameter that
exists only under the alternative makes the standard null distribution wrong — and it has the same
moral: a statistic that looks significant against the textbook table is not.

**The allocation result and its binding condition.** The survey's asset-allocation section reports
substantial costs to ignoring regimes (Ang–Bekaert: an investor needs compensation of roughly two
to three cents per dollar of initial wealth to ignore regime changes when a risk-free asset is
available; Guidolin–Timmermann on skew and kurtosis preferences; Tu finding the cost material even
after accounting for parameter uncertainty). The condition attached to the central illustration is
stated plainly by the authors and is the sentence to remember: **"In Figure 5, the risk-return
trade-offs are known in each regime. Given the parameters, the investor can infer which regime
prevails at each time."** The quantified gains are gains to an investor who knows the regime
parameters and can identify the current state. The real-time version — filtered inference, with
estimated parameters — is acknowledged as a further problem rather than solved.

## Robustness evidence (qualitative only)

The *descriptive* claims are robust and multiply replicated: that returns exhibit regime-like
behaviour in volatility, that the high-volatility state has lower expected returns and lower Sharpe
ratios, and that regimes are persistent, are reported across equities, fixed income and foreign
exchange and across many studies and countries. The survey also notes that mean-reversion
coefficients differ across regimes even for series close to i.i.d. The authors have strong track
records in exactly this area, and an Annual Review survey is a reasonable proxy for settled
consensus as of its writing.

The *prescriptive* claims are weaker in a way the survey is honest about but does not foreground.
Every quantified allocation gain reviewed is computed in a setting where the regime process is
known or estimated on the full sample; the one real-time demonstration in the paper is a simulation
in which the filter, with true parameters, both misses changes and false-alarms. No out-of-sample,
cost-aware, real-time regime-timing result is reported in the survey. Transaction costs are not
modelled anywhere in it, which matters a great deal for a strategy whose whole content is switching.
Multiple testing is not discussed. For the purposes of this folder's rubric: Tier A as a survey of
what regime models *describe*, and no better than hypothesis fodder for what they might *earn*.

**Explicit tension with this lab's own record, and it resolves in the lab's favour.**
`experiments/learnings.md` records that three de-risking overlays — including a **binary SPY-trend
regime switch** — all cut train drawdown and lost more validation Sharpe than they saved, "mostly
via diluted upside or whipsaw turnover", and separately that "blending beats switching". A
literature review reporting large costs to ignoring regimes looks like a contradiction of that. It
is not, and the survey supplies the reconciliation itself: the literature's gains are
**known-regime** gains, and the lab's losses are **inferred-regime** losses. Whipsaw *is* the false
alarms the authors describe; dilution is partly the missed changes. The two records are consistent
once the filtered/smoothed and known/estimated distinctions are applied, and the lab's refutations
stand. The correct reading is not "regimes do not exist" — the descriptive evidence that they do is
strong — but **"the gap between a regime existing and a regime being tradeable in real time is
where all three of the lab's overlays died."**

## Implementability here

**Feasible, and that is the problem.** A two-state Gaussian switching model on a single series is a
handful of parameters fitted by EM or direct likelihood maximisation; `scipy.optimize` is enough and
`hmmlearn` is not needed. Runtime is not a constraint. It would fit comfortably inside the
protocol's budget even refitted walk-forward at every month-end on an index proxy. Nothing about
the engineering would stop a candidate from this vein being written tonight, which is precisely why
the conditions below matter more than usual.

**Four hard requirements, if anything from this vein is ever run.**

1. **Filtered probabilities only, never smoothed.** `Pr(s_t | I_t)`, computed from a model whose
   parameters were themselves estimated only on data up to `t`. `strategies/lib/walkforward.py`
   exists for this. A model fitted once on the whole visible window and filtered backwards is the
   classic lookahead the protocol's `causality_check` is built to catch, and here it would also be
   invisible in the output — the weights would simply look very good.
2. **Fix the number of states at two, in advance, and say so.** There is no valid test to choose it
   with, so choosing it by fit is an unpriced search over a hyperparameter. Two is what the
   literature defaults to and that default should be inherited rather than re-derived.
3. **Fix `random_state` and keep estimators single-threaded.** The likelihood surface of a switching
   model is multimodal and EM is start-dependent; the causality check compares holdings at `1e-6`
   and reads non-determinism as a peek. Also note **label switching** — the states are identified
   only up to permutation, so the mapping from state index to "high-volatility state" must be
   pinned by a rule (e.g. order states by fitted `σ`) and not by whichever label EM happened to
   assign on that refit.
4. **Budget for whipsaw before measuring anything else.** Under protocol v3, drift is held as shares
   and every trade that undoes it is charged, with per-name tiered costs plus transaction taxes. A
   state variable that false-alarms is a turnover generator. The lab's own cadence lesson applies
   in both directions: too slow and the trigger lags, too fast and it whipsaws.

**The honest recommendation, and it follows the acceptance criterion this session was aimed at.**
The open question that sent this session into the regime vein set a sharp bar — read it only if it
can produce something that is **not a timing overlay**. On this source, the timing overlay is
precisely what should *not* be built: the mechanism is real, the real-time identification is
demonstrably poor even under ideal conditions, and the lab has already paid three times for the
version of this that trades. What survives the bar is the diagnostic use in the two companion notes
and one further item from this source specifically:

- **A regime model as a null, not as a signal.** The survey's point that a two-state switching
  process mechanically generates fat tails, volatility clustering, skewness, time-varying
  correlations and high squared-return autocorrelation *with essentially zero autocorrelation in
  levels* makes it a **data-generating process to simulate under**. The lab's bootstrap intervals
  and random-selection nulls are built on resampling the panel's own history; a parametric
  regime-switching null is a different and harder one, and it is the natural stress test for any
  candidate whose edge might be an artifact of volatility clustering rather than of a mean effect.
  That is a use for which the known-parameter limitation is irrelevant, because nothing has to be
  identified in real time.

**One thing this source does *not* support, for the record.** It gives no basis for expecting a
regime overlay to improve a long-only equity book's Sharpe net of costs, and no result in it was
measured under a long-only constraint with transaction costs. Anyone importing the two-to-three
cents figure as a performance expectation would be doing exactly what `CLAUDE.md` forbids —
importing a literature number into a hypothesis — and it would also be wrong on its own terms,
since it is a known-regime quantity.

## Related

- `2026-10-22-breakdate-inference-unknown-timing.md` — the same identification pathology in the
  break setting: a parameter unidentified under the null makes the textbook distribution wrong.
  Read for the general form of the problem.
- `2026-10-22-multiple-changepoint-estimation-bai-perron-pelt.md` — the discrete-break alternative
  to a latent recurring state, and the diagnostic uses that survive this session's acceptance bar.
- `2026-08-17-forecast-combination-why-averaging-beats-selecting.md` — the standing counter-proposal
  to switching at all, and the one with this lab's own measurements behind it.
- `experiments/learnings.md`, "De-risking overlays on momentum reliably backfire out-of-sample" and
  "Blending beats switching" — the refutations this source is in apparent tension with. The tension
  is recorded and resolved above (known-regime gains versus inferred-regime losses); the lab's
  results are not contradicted.
- `SUMMARY.md`, "Forecasting the variance instead of the mean" — the existing treatment of what a
  volatility-scaling overlay buys. A regime model's volatility state is a close cousin and the
  overlap should be checked before any candidate is written.
