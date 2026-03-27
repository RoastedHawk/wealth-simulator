from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class GoalResult:
    reached: bool
    month: Optional[int]  # 1-based month index from simulation
    value_at_month: Optional[float]


def time_to_target(df: pd.DataFrame, target: float, column: str = "balance") -> GoalResult:
    """
    Return the first month where df[column] >= target.
    Expects df to contain 'month' and the given column.
    """
    if target <= 0:
        return GoalResult(reached=True, month=0, value_at_month=0.0)

    hits = df.loc[df[column] >= target, ["month", column]]
    if hits.empty:
        return GoalResult(reached=False, month=None, value_at_month=None)

    first = hits.iloc[0]
    return GoalResult(reached=True, month=int(first["month"]), value_at_month=float(first[column]))
