from wealth_simulator.sim import simulate_monthly


def test_simulate_monthly_row_count():
    df = simulate_monthly(principal=1000.0, monthly_contribution=100.0, annual_rate=0.06, years=2)
    # 24 months plus month 0
    assert len(df) == 25


def test_simulate_monthly_zero_rate_is_linear():
    df = simulate_monthly(principal=1000.0, monthly_contribution=100.0, annual_rate=0.0, years=1)
    assert df["balance"].iloc[-1] == 1000.0 + 100.0 * 12


def test_contributions_never_decrease():
    df = simulate_monthly(principal=500.0, monthly_contribution=50.0, annual_rate=0.05, years=3)
    assert (df["contributions"].diff().fillna(0) >= 0).all()
