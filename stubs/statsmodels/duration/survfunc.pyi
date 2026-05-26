import numpy as np
from numpy.typing import NDArray

class SurvfuncRight:
    surv_prob: NDArray[np.float64]
    surv_times: NDArray[np.float64]

    def __init__(
        self,
        time: NDArray[np.float64],
        status: NDArray[np.int_],
        title: str | None = ...,
        freq_weights: NDArray[np.float64] | None = ...,
        exog: NDArray[np.float64] | None = ...,
    ) -> None: ...
