---
title: "Survivorship Bias in Performance Studies — with: Inference about Survivors; and (second-hand) Survival"
authors: Brown, Goetzmann, Ibbotson & Ross; Stambaugh; Brown, Goetzmann & Ross
year: 1992; 2011; 1995
venue: Review of Financial Studies 5(4), 553–580 (tier 1); Quarterly Journal of Finance 1(3), 423–464 (tier 2, peer-reviewed but low-circulation); Journal of Finance 50(3), 853–873 (tier 1)
url: https://doi.org/10.1093/rfs/5.4.553 ; https://doi.org/10.1142/S2010139211000158 ; https://doi.org/10.1111/j.1540-6261.1995.tb04039.x
citations: "BGIR 1992: 1,161 (OpenAlex, checked 2026-08-26; Semantic Scholar DOI endpoint 1,115). Stambaugh 2011: 22 (OpenAlex, checked 2026-08-26; Crossref is-referenced-by-count 5). BGR 1995: 303 (OpenAlex, checked 2026-08-26)"
sample_period: "BGIR: no historical estimation sample — a Monte Carlo calibrated to a 1926–1989 equity-premium distribution and to the cross-sectional beta/residual-risk dispersion of a 1976–1988 money-manager panel. Stambaugh: no historical sample — Bayesian analysis plus a calibrated hedge-fund illustration. BGR 1995: analytical, with a century-scale illustration"
markets: US equity mutual-fund and money-manager cross-sections (BGIR); asset-agnostic analytics (Stambaugh, BGR)
tier: A for BGIR (tier-1 venue, four-figure citations, the result is a proof-plus-simulation and cannot decay); B for Stambaugh (rigorous and tier-1 authorship, but thinly cited and no empirical study); BGR 1995 recorded **second-hand** — closed access, no repository copy found, summarised from its published abstract only
validation_overlap: false
published_post_2018: false
---

## Mechanism

The folder's first source on the axis `learnings.md` has carried as a permanent caveat since day
one and has never sourced: what conditioning a sample on survival actually does. The headline is
that **the lab's caveat has the emphasis in the wrong place.**

**The truncation mechanism (BGIR).** Suppose assets differ in their risk (beta and, crucially,
residual volatility) and the sample retains only those whose realised return cleared some bar.
Truncation from below does two things at once. It shifts the *first* moment of the survivors'
return distribution upward — the obvious effect, and the one the lab's caveat names. But it also
reshapes the *joint* distribution of return and volatility among survivors, because a high-residual-
risk asset needs a lucky draw to clear the bar and a low-risk asset does not. Conditional on
survival, therefore, observed return carries information about volatility, and volatility carries
information about future observed return. **Truncation by survivorship induces a spurious
relationship between volatility and return**, and through it a spurious appearance of
*predictability* — persistence in relative performance where the data-generating process has none.

**The sign is set by the selection rule, and it is not always the same sign.** BGIR's appendix
proves the second half of this and it is the part usually forgotten. If the selection rule conditions
on **early / sequential** performance — the asset must survive a review at the end of each
sub-period — the induced effect is **persistence**. If instead it conditions on **overall,
whole-sample cumulative** performance, the induced effect is **reversal**: among assets selected on
their total two-period return, a good first period makes a good second period *less* likely, because
the selection had to be met somehow and a weak first half implies a strong second half. The authors
state plainly that "the net effect of these two forces must be resolved empirically" and depends on
"the exact form of the selection rules and the potential dispersion of the spread parameter". There
is no universal direction to a survivorship correction.

**The level effect and the inference effect are different sizes, and it is the inference effect that
is large.** In BGIR's own simulation the effect of survivorship on average risk-adjusted return is
small: about 0.4–0.6% per year for a 5–10% annual performance cut and 0.8% for a 20% cut, consistent
with the independent estimates they cite. But with only a **5%** cut per year, a cross-sectional
regression of successive risk-adjusted performance measures rejects the (true) hypothesis of no
persistence **more than half the time**, with mean and median t-statistics above 2. At a 10% cut,
three quarters of the simulated test statistics lie above the median of their theoretical null
distribution. The authors' summary of the size of this is the sentence to carry: *"Even a small
degree of truncation by survivorship will induce an unacceptably high probability of false inference
of persistence in performance."*

**BGIR themselves extend the claim past performance measurement.** Their conclusion states the
mechanism "has implications for empirical tests of asset pricing models and in particular for studies
of so-called anomalies", and a footnote draws out the specific case that survival should induce a
correlation between **size** and average risk-adjusted return, because smaller firms carry more
residual risk. So the result is not fund-specific; it is a property of any cross-section whose
membership depended on realised return.

**BGR 1995 (second-hand).** The companion result on the time-series side. Per its published
abstract, empirical analysis of returns implicitly conditions on securities surviving into the
sample; that conditioning "induces a spurious relationship between observed return and total risk for
those securities that survive to be included in the sample"; and an **ex ante** risk premium of zero
can generate a large **ex post** positive premium purely by conditioning on the market surviving an
absorbing lower bound over a century. Recorded here only at that level — the paper is closed access
with no repository copy, and nothing beyond the abstract is claimed for it.

**The counterweight, and it is a real one (Stambaugh).** The obvious inference from the above — "the
survivors' sample mean overstates the truth, so subtract the survival bias" — is shown to be wrong in
general, and the reason is a distinction between two quantities that are usually conflated:

- **Survival bias** (a sampling property): `E[a | survived] − α > 0`, where `a` is the survivor's
  sample mean and `α` its true expected return. This is real and can be substantial.
- **The correct inference** (a posterior): `E[α | a]`, what an investor who holds *this* sample
  should believe about *this* survivor's expected return.

Stambaugh's result is that these come apart. In the base case — a fixed survival threshold, and
**no commonality** across assets in the prior uncertainty about their parameters — `E[α | a] = a`
**exactly**, even though `a` carries a substantial sampling bias. Once you condition on the
survivor's actual return series, the additional fact that it survived tells you nothing further: the
sample mean is a sufficient statistic. The same holds under a *relative* survival criterion (the
better of two assets survives) when the two assets' alphas are drawn independently — the loser's
cumulative return acts as a randomly drawn threshold that is independent of the survivor's `α`.

What makes conditioning matter is **commonality**: the degree to which learning one asset's parameter
would revise your beliefs about another's. At the opposite extreme, where all assets share a single
unknown `α`, knowing the survivor beat an asset *with the same expected return* is genuine evidence
that its returns exceeded that value, and `E[α | a] < a` — by 2.7% in his worked example, which is
also exactly the sampling bias in that case. Hence the paper's own summary: **"Survival bias, as
typically computed, generally gives too severe an adjustment for survival unless one assumes that
expected returns on all assets, dead and alive, are equal to a common value that is completely
unknown."** Commonality in *style* (surviving assets resembling each other beyond their factor
loadings) pushes in the same direction, increasing survival effects.

The direction of the effect on **alpha** is also not fixed: conditioning on survival "usually lowers,
but can sometimes raise, a surviving asset's inferred alpha".

## Construction recipe

Neither source is a strategy. What they supply is a pre-trial checklist for reading any result
obtained on a survivorship-conditioned universe:

1. **Name the selection rule and its cadence.** Sequential/periodic survival review → expect induced
   **persistence**. Selection on whole-period cumulative performance → expect induced **reversal**.
   A universe defined by *membership at the end of the sample* is closer to the first: index
   membership is re-reviewed on a fixed cadence and a name that falls far enough leaves.
2. **Separate the two quantities being biased.** A level claim (this book earns X) and a persistence
   claim (past relative winners keep winning) are corrupted by different amounts, and the persistence
   claim is corrupted far more per unit of truncation.
3. **Ask how much commonality you are willing to assume** across the universe's instruments before
   applying any survivorship discount. Maximum discount ⇔ you believe all instruments, dead and
   alive, share one completely unknown expected return. Zero discount ⇔ you believe their expected
   returns are drawn independently.
4. **Risk-normalise before comparing.** BGIR's closing conjecture — offered as a conjecture, not a
   result — is that normalising performance measures by the **residual standard deviation** may be
   relatively robust to this misspecification, since the misspecification enters through
   cross-sectional dispersion in residual risk.

## Robustness evidence (qualitative only)

BGIR is a tier-1 publication with four-figure citations across two indices; its central claim is a
Monte Carlo of a stated data-generating process plus an analytical appendix, so it is a mathematical
result about an estimator and cannot decay in the McLean–Pontiff sense. Its calibration is the one
soft spot the authors flag themselves: the dispersion of beta and residual risk used in the
simulation was measured on *surviving* managers, so the inputs to the experiment are themselves
truncated. Both directions of that error are discussed in the paper's own footnotes; the induced
persistence is not sensitive to it in sign, only in magnitude.

Stambaugh is analytically rigorous and by a tier-1 author, but is thinly cited (22 / 5 across two
indices) and carries no empirical study — its illustration is a calibrated hedge-fund example. Treat
its *distinctions* as sound and its *magnitudes* as illustrative. It has not, as far as this session
could find, been independently replicated or contested.

BGR 1995 is well cited (303) and tier-1, but is recorded here from its abstract alone.

No source here reports a decay pattern, because none of them documents a tradeable effect; they
document properties of estimators.

## Implementability here

Not a candidate. Three consequences, in decreasing confidence.

**(a) The lab's permanent caveat is aimed at the smaller of the two problems.** `learnings.md` says:
"the universe is today's constituents. Single-stock alpha (especially momentum/quality tilts on
stocks) will look better than it was." That is a **level** claim. Both sources here say the level
distortion is the more forgiving one — BGIR measure it at well under a percent a year in their
calibration, and Stambaugh shows the standard adjustment for it is generally *too severe*. The claim
that survives untouched, and is the one the caveat does not make, is about **inference**: truncation
on realised return manufactures apparent cross-sectional persistence, which is precisely and
exclusively what a cross-sectional momentum strategy asserts. The champion's entire mechanism is the
one this literature says a survivorship-conditioned sample fabricates most readily. The caveat's
parenthetical ("especially momentum") is right for a reason it does not state.

**(b) The sign is a function of the selection rule, so it is checkable rather than assumable.** This
repo's universe is defined by membership in global indices *today*, and index membership is reviewed
on a recurring cadence with removal for sustained relative decline. Under BGIR's taxonomy that is a
**sequential** cut, the case that induces **persistence** — not the whole-sample cumulative cut that
induces reversal. So the induced direction here is the one that flatters momentum, and it would
flatter a reversal strategy correspondingly *less*. Recorded as a possible partial account of a
standing asymmetry in the lab's record — momentum works on this universe, short-horizon reversal has
been refuted twice — but only as one candidate account among several: the reversal refutations already
have a sufficient mechanism (`notes/2026-08-17-short-term-reversal-as-liquidity-provision.md`), and
this note supplies no evidence about relative magnitudes.

**(c) The discount is a judgement about commonality, and here that judgement points toward a large
one.** Stambaugh's relief is not a licence to ignore survivorship. It is largest when the assets'
expected returns are drawn independently and vanishes as they share a common unknown value. This
repo's ~145 instruments are large, liquid, global stocks and ETFs that share a dominant market
factor and would not plausibly be assigned independent priors over their expected returns. High
assumed commonality ⇒ the near-full survival adjustment is closer to correct **here** than the paper's
general result might suggest. The right way to use Stambaugh is as the reason the discount is a
stated assumption rather than a reflex — not as a reason to shrink it.

**One boundary that must be stated first.** Both papers reason about inference on an *asset's*
expected return or alpha. The lab's object is a *strategy's* net Sharpe on a book rebuilt from a
fixed instrument list. The step from "survivorship corrupts cross-sectional persistence inference"
to "the champion's validation Sharpe is inflated by amount X" is not made by any source read here,
and no magnitude for this repo can be taken from these papers. What transfers is the direction and
the identification of which claim is at risk, not a number.

**Not a proposed measurement.** The obvious follow-up — estimate the induced persistence on this
repo's universe by simulation — requires scoring returns, so it falls outside the folder's
holdings-only free-diagnostic exemption and would have to be a deliberate, journalled measurement.
It is also, unlike the diagnostics in candidates #23 and #28, not computable at all without a
survivorship-free universe, which this repo does not have and `program.md` lists as a
human-approval-gated future upgrade.

## Related

- `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the same problem measured
  rather than modelled, on the exact data construction this repo uses (a backtest run on today's
  index constituents), plus the mechanism by which index membership selects on past return.
- `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md` — what the surviving universe's
  return distribution looks like, and why the median stock's absence from it matters.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the other reason an in-sample effect
  overstates what is available forward; independent of, and additive to, this one.
- `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md` — the sufficient mechanism already
  on file for the lab's reversal refutations, which point (b) above must not be read as replacing.
- `experiments/learnings.md` → "Data & methodology caveats (permanent)", first bullet — the caveat
  this note re-aims rather than contradicts.
