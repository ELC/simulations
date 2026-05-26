"""Third-party adapter layer.

The only package in the codebase allowed to import :mod:`scipy` or
:mod:`statsmodels` directly. Every other module in :mod:`stlite_hello`
consumes the narrowly-typed wrappers re-exported here.
"""

from .scipy_stats import (
    BootstrapCIResult,
    DistributionName,
    KDESample,
    bootstrap_ci,
    fit_distribution,
    gaussian_kde_grid,
    pdf_values,
    rvs_distribution,
)
from .statsmodels import (
    KaplanMeierEstimate,
    kaplan_meier_mean_lifetime,
)

__all__ = [
    "BootstrapCIResult",
    "DistributionName",
    "KDESample",
    "KaplanMeierEstimate",
    "bootstrap_ci",
    "fit_distribution",
    "gaussian_kde_grid",
    "kaplan_meier_mean_lifetime",
    "pdf_values",
    "rvs_distribution",
]
