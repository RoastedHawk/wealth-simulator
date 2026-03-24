from __future__ import annotations

import pandas as pd


def project_wealth(principal: float, annual_rate: float, years: int) -> float:
    """Compound annually. annual_rate like 0.07 for 7%."""
    if principal < 0:
        raise ValueError("principal must be >= 0")
    if years < 0:
        raise ValueError("years must be >= 0")
    return principal * (1 + annual_rate) ** years


def simulate_monthly(
    *,
    principal: float,
    monthly_contribution: float,
    annual_rate: float,
    years: int,
    annual_inflation_rate: float = 0.0,
) -> pd.DataFrame:
    """
    Simulate monthly compounding with fixed monthly contributions.

    annual_rate and annual_inflation_rate are expressed like 0.07 for 7%.
    Returns a DataFrame with:
      month, balance, contributions, interest, inflation_index, real_balance
    """
    if principal < 0:
        raise ValueError("principal must be >= 0")
    if monthly_contribution < 0:
        raise ValueError("monthly_contribution must be >= 0")
    if years < 0:
        raise ValueError("years must be >= 0")

    months = years * 12
    monthly_rate = annual_rate / 12.0
    monthly_inflation = annual_inflation_rate / 12.0

    balance = float(principal)
    contrib_only = 0.0
    inflation_index = 1.0

    rows: list[dict[str, float]] = []

    for m in range(months + 1):
        contributions = principal + contrib_only
        interest = balance - contributions
        if interest < 0 and interest > -1e-9:
            interest = 0.0

        real_balance = balance / inflation_index

        rows.append(
            {
                "month": float(m),
                "balance": balance,
                "contributions": contributions,
                "interest": interest,
                "inflation_index": inflation_index,
                "real_balance": real_balance,
            }
        )

        # advance one month
        balance = balance * (1 + monthly_rate) + monthly_contribution
        contrib_only += monthly_contribution
        inflation_index *= (1 + monthly_inflation)

    df = pd.DataFrame(rows)
    df["month"] = df["month"].astype(int)
    return df
