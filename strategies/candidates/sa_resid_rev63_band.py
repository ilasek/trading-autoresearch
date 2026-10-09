"""63-day residual reversal, 100 names, monthly decisions, inside a retention band.

THE CLAIM IN ONE LINE. The mechanism the v2 board found is real on this panel and was
killed by its *execution bill*, not by its signal -- so run the same mechanism at a
seventh of the turnover and see whether what is left is positive.

WHAT v3 ACTUALLY REFUTED, AND WHAT IT DID NOT. `reports/protocol-v3-methodology.md`
re-measured `sa_pca_resid_reversion` (21-day formation, top 30, equal weight, monthly,
**22x one-way turnover a year**) from validation Sharpe 0.597 to 0.453 against a pool at
0.452: skill +0.00, -0.22 at 2x costs, negative train skill in both sub-periods. The
audit's own reading is that the collapse came from the execution convention -- same-close
fills, free drift, one flat 15 bps on a book tilted toward illiquid, 71%-non-US,
stamp-duty-paying names. **That is a verdict on a 22x-turnover construction, not on
residual reversal.** Tonight's first trial measured the other half of that arithmetic
directly: at 1.2x turnover a year the entire v3 cost bill is ~14 bps/yr, and doubling the
liquidity tier moved skill by 0.014. The cost model is only lethal to books that trade.

TONIGHT'S FREE SCREENS, WHICH ARE WHY THIS FILE EXISTS (train 1997-2017 only, 244-246
month-ends, no portfolio formed and no return, Sharpe or drawdown computed outside
`run_experiment.py`; journal F4-F6).

*F4 -- which formation horizon carries the level effect.* Top-100 slice, forward 63-day
excess over the eligible pool's mean on the same date, reported as a LEVEL because
tonight's first lesson is that a rank IC cannot screen a hypothesis about magnitudes:

    score            k      IC      t   top100 excess bps/63d    t    beta_top  beta_pool
    resid5pc_rev    21   +0.0223  +4.12          +35.2         +2.52    +0.963    +0.988
    resid5pc_rev    63   +0.0288  +4.99          +38.3         +2.83    +0.974    +0.988
    resid5pc_rev   126   +0.0178  +3.22          +29.6         +2.15    +0.973    +0.988
    resid5pc_rev   252   +0.0113  +1.51          +19.8         +1.32    +0.955    +0.988
    raw_rev         63   +0.0218  +2.09          +54.4         +1.93    +1.033    +0.988
    raw_rev        252   -0.0070  -0.49          +17.9         +0.44    +1.076    +0.989

Two things. **The 63-day residual horizon dominates the 21-day one the v2 lead used** on
both the IC and the level, which matters because a 63-day formation decays more slowly
and therefore turns over less. And **the residual version is beta-neutral (0.974 against
the pool's 0.988) while the raw version is not (1.033-1.076)** -- after tonight's low-vol
result, a slice that earns its excess at the pool's own beta is the only kind worth
trading, because Sharpe is flat in beta on this panel and a beta-loaded excess is not an
excess at all.

*F6 -- the retention band, and the reason this is a mechanism and not a knob.* Protocol v3
charges proportional costs (bps per side plus ad valorem tax), and under proportional
costs the optimal policy is provably **not** "trade to target": it is to trade the minimum
that keeps the book inside a no-trade band, with width scaling as the cube root of the
cost (`research/notes/2026-10-08-no-trade-bands-under-proportional-costs.md`, Muhle-Karbe
-Reppen-Soner; the aim-portfolio partial-move rule this folder already covered solves the
*quadratic*-cost problem and is the answer to a cost geometry v3 does not have). The
long-only discrete version of a band is a retention buffer: hold the top K, but keep a
name already held while it is still inside the top B. Measured on the monthly grid, held
book's forward 21-day excess over the pool, 246 dates:

    buffer B   turn/yr   fwd21 excess bps     t    ann gross   cost @35bps   net bps/yr
       100       5.43          +17.5        +2.32     +210         190           +20
       150       4.07          +20.9        +2.69     +251         143          +108
       200       3.15          +22.2        +3.03     +266         110          +156
       300       1.92          +11.9        +1.69     +143          67           +76
       500       1.25           +6.8        +1.23      +82          44           +38
       800       0.17          +15.7        +2.52     +188           6          +182

**The band does what the theory says it does, and more: it cuts turnover by 42% and
RAISES the held book's excess** (+17.5 to +22.2, t +2.32 to +3.03). It is not a trade-off
between cost and signal here -- the names a band declines to sell are names whose score
has decayed but not reversed, and churning them was paying to replace a good holding with
a marginally better one.

**B = 200 is taken, on a stated criterion, and B = 800 is refused as an artifact.** The
criterion -- highest net-of-modelled-cost excess -- was fixed before the column was read.
B = 800's +182 is spurious: at 0.17x turnover a year the book essentially never changes
after its first fill, so its 246 monthly observations are one draw repeated and its
t-statistic is meaningless. That autocorrelation inflates every row to some degree (a
B = 200 book still carries ~74% of itself month to month), so **every t in the table above
should be read as an upper bound**, and none of them is the trial's evidence -- the trial's
evidence is the skill interval `run_experiment.py` computes with a paired block bootstrap.

ONE MORE FREE FINDING, RECORDED BECAUSE IT KILLS A FAMILY CHEAPLY RATHER THAN BECAUSE IT
HELPS THIS CANDIDATE. The same screen splits the monthly excess by calendar position: at
B = 150 the held book earns **+43.9 bps (t +3.32, n 82) in the month following a
quarter-end against +9.4 bps (t +0.99, n 164) in other months**, and F5 found the forward
*63-day* excess from a quarter-end is only +17.7 bps -- so the effect is concentrated in
the three weeks after quarter-end and gives part of it back over the rest of the quarter.
That is a flow story and it is tempting as a `seasonality-calendar` trial. It is not
tradeable here, for a structural reason worth stating once: **v3 measures Sharpe on
returns in excess of T-bills and the pool is fully invested, so any strategy that sits in
cash forfeits the equity premium while the pool keeps earning it.** A book in cash for
nine months a year would need an active return several times the size of this one to
reach the pool's 0.34. The calendar concentration is therefore a reason to rebalance
monthly -- every month's decision gets a fresh signal -- and not a timing trade.

WHY THIS IS STILL A `statistical-arbitrage` TRIAL AND NOT A RELABELLING. It is the same
family and the same mechanism as the v2 lead, openly: a 5-component residual reversion.
The v3 board is empty, so there is no family lead for it to wear the label of, and the
honest statement of the claim is that **this is the v2 mechanism re-engineered for v3's
cost model** -- 63-day formation instead of 21, 100 names instead of 30, a band instead of
a clean sweep, 3.2x turnover instead of 22x. If it scores, the finding is about execution
design; if it does not, the v3 audit's verdict extends from one construction to the
mechanism, which is a stronger and more useful negative than the audit alone supports.

PRE-REGISTERED PREDICTION. Validation skill **+0.10 to +0.25** (pool 0.34 on validation
with the T-bill series now seeded), from +266 bps/yr of modelled gross excess less ~110 of
cost against a 100-name book's tracking error. Turnover **3 to 4x/yr**; the 2x-cost stress
should cost about 0.03 to 0.05 of skill, not the 0.22 the v2 lead lost. Train skill
positive in both sub-periods. By this repo's own anti-prediction rule a variant chosen on
a train screen is a bearish signal for validation, and B = 200 was chosen on one; that is
recorded here rather than left out.

FALSIFIERS.
  - Skill at or below zero with turnover near 3x says the v3 audit's verdict is about
    residual reversal itself and not about its 22x execution -- the stronger negative, and
    it would close the family.
  - Skill positive but the 2x-cost stress negative says the margin is thinner than the
    F6 column, i.e. the 35 bps/side used there understates what this book pays, which is
    the single most likely way the arithmetic is wrong.
  - A null percentile below 90% says a random 100-name book of the same types and regions
    held on the same schedule does as well, i.e. the band and not the score is doing the
    work -- in which case the next trial is the band on a different score, not this one.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "sa_resid_rev63_band",
    "family": "statistical-arbitrage",
    "track": "scout",
    "hypothesis": (
        "Reverting the 63-day return measured against the five leading principal "
        "components of the trailing 252-day standardised return matrix, holding the "
        "top 100 equal weight on monthly decisions but retaining a name already held "
        "while it stays inside the top 200, beats the equal-weight eligible pool's "
        "validation Sharpe by at least 0.10, because on the train split that slice "
        "earns +22.2 bps per 21 days over the pool (t +3.03) at the pool's own beta "
        "(0.974 vs 0.988) while the retention band cuts one-way turnover from 5.4x to "
        "3.2x a year -- about 110 bps/yr of modelled cost against 266 of gross excess, "
        "where the v2 lead's 22x construction paid 3-6%/yr and scored zero skill under "
        "v3; skill at or below zero says v3's verdict is on residual reversal itself "
        "rather than on its execution, and a null percentile below 90% says the band "
        "rather than the score did the work."
    ),
}

FORMATION = 63          # days of return reverted
WINDOW = 252            # days of return matrix the components come from
N_PC = 5
TOP_N = 100             # names held
BAND = 200              # a held name is kept while its score rank is within this
MIN_NAMES = 150
MIN_COVERAGE = 0.8


def _residual_reversal(block: np.ndarray, recent: np.ndarray) -> np.ndarray:
    """Cumulative `recent` return with its projection on the `N_PC` leading
    components of `block` removed, negated so a fallen residual scores high.
    The eigendecomposition is taken on the day-by-day Gram matrix, so its cost
    is set by `WINDOW` and not by the width of the panel."""
    mu, sigma = block.mean(axis=0), block.std(axis=0) + 1e-12
    standardized = (block - mu) / sigma
    _, vectors = np.linalg.eigh(standardized @ standardized.T)
    loadings = standardized.T @ vectors[:, -N_PC:]
    loadings /= np.linalg.norm(loadings, axis=0, keepdims=True) + 1e-12
    recent_z = (recent - mu) / sigma
    residual = recent_z - (recent_z @ loadings) @ loadings.T
    return -residual.sum(axis=0)


def generate_weights(prices: pd.DataFrame, eligible: pd.DataFrame = None) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)
    returns = prices.pct_change(fill_method=None)

    rows: dict = {}
    held: list = []          # carried forward; depends only on earlier decisions,
                             # which is what makes the band causal under truncation
    for dt in rebalance_dates:
        if dt not in returns.index:
            continue
        end = returns.index.get_loc(dt)
        if end < WINDOW:
            continue
        block = returns.iloc[end - WINDOW + 1 : end + 1]
        covered = block.notna().mean(axis=0).to_numpy() > MIN_COVERAGE
        ok = elig.loc[dt].to_numpy() & covered
        if ok.sum() < MIN_NAMES:
            continue
        ids = prices.columns[ok]
        # Mask first, then score: the mean, the standard deviation and the
        # component basis below are all estimated on the eligible set only,
        # never on the frame's column set (learnings.md, 2026-10-07).
        score = pd.Series(
            _residual_reversal(
                np.nan_to_num(block[ids].to_numpy()),
                np.nan_to_num(returns.iloc[end - FORMATION + 1 : end + 1][ids].to_numpy()),
            ),
            index=ids,
        ).dropna()
        if len(score) < MIN_NAMES:
            continue
        rank = score.rank(ascending=False)
        keep = [c for c in held if c in rank.index and rank[c] <= BAND]
        incoming = [c for c in score.nlargest(TOP_N).index if c not in keep]
        book = list(dict.fromkeys(keep + incoming))[:TOP_N]
        held = book
        w = pd.Series(0.0, index=prices.columns)
        w[book] = 1.0 / len(book)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
