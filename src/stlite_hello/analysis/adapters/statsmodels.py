"""Narrow, typed wrappers around the ``statsmodels`` surface we use.

The only place in the codebase that may import :mod:`statsmodels`.
"""

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field
from statsmodels.duration.survfunc import SurvfuncRight

_MEDIAN_SURVIVAL_THRESHOLD = 0.5


class KaplanMeierEstimate(BaseModel):
    """Kaplan-Meier survival summary used by the mean-tenure metric."""

    model_config = ConfigDict(frozen=True)

    mean_lifetime: float = Field(ge=0.0)
    median_lifetime: float = Field(ge=0.0)
    observed_events: int = Field(ge=0)
    censored_events: int = Field(ge=0)


def kaplan_meier_mean_lifetime(
    *,
    durations: NDArray[np.float64],
    event_observed: NDArray[np.int_],
) -> KaplanMeierEstimate:
    """Right-censored mean of ``durations`` via Kaplan-Meier integration.

    Returns
    -------
    KaplanMeierEstimate
        ``mean_lifetime`` is the restricted mean survival time -- the area
        under the empirical survival function on the observed support.
        When no event is observed the estimate falls back to the longest
        censored duration.
    """
    if durations.shape != event_observed.shape:
        msg = "durations and event_observed must have the same shape"
        raise ValueError(msg)
    if durations.size == 0:
        return KaplanMeierEstimate(
            mean_lifetime=0.0,
            median_lifetime=0.0,
            observed_events=0,
            censored_events=0,
        )

    observed = int(np.sum(event_observed != 0))
    censored = int(event_observed.size - observed)

    if observed == 0:
        fallback = float(durations.max())
        return KaplanMeierEstimate(
            mean_lifetime=fallback,
            median_lifetime=fallback,
            observed_events=0,
            censored_events=censored,
        )

    sf = SurvfuncRight(durations.astype(np.float64), event_observed.astype(np.int_))
    times = np.asarray(sf.surv_times, dtype=np.float64)
    surv = np.asarray(sf.surv_prob, dtype=np.float64)

    extended_times = np.concatenate(([0.0], times))
    extended_surv = np.concatenate(([1.0], surv))
    differences = np.diff(extended_times)
    mean_lifetime = float(np.sum(extended_surv[:-1] * differences))

    below_half = np.where(surv <= _MEDIAN_SURVIVAL_THRESHOLD)[0]
    median_lifetime = float(times[int(below_half[0])]) if below_half.size > 0 else float(times[-1])

    return KaplanMeierEstimate(
        mean_lifetime=mean_lifetime,
        median_lifetime=median_lifetime,
        observed_events=observed,
        censored_events=censored,
    )
