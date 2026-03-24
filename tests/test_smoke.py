from wealth_simulator.sim import simulate_monthly


def test_simulate_monthly_row_count():
    df = simulate_monthly(
        principal=1000.0,
        monthly_contribution=100.0,
        annual_rate=0.06,
        years=2,
    )
    # 24 months plus month 0
    assert len(df) == 25


def test_simulate_monthly_zero_rate_is_linear():
    # With 0% return, balance should be principal + monthly_contribution * months
    df = simulate_monthly(
        principal=1000.0,
        monthly_contribution=100.0,
        annual_rate=0.0,
        years=1,
    )
    assert df["balance"].iloc[-1] == 1000.0 + 100.0 * 12


def test_contributions_never_decrease():
    df = simulate_monthly(
        principal=500.0,
        monthly_contribution=50.0,
        annual_rate=0.05,
        years=3,
    )
    assert (df["contributions"].diff().fillna(0) >= 0).all()


def test_real_balance_drops_with_inflation_when_nominal_flat():
    df = simulate_monthly(
        principal=10_000.0,
        monthly_contribution=0.0,
        annual_rate=0.0,
        years=1,
        annual_inflation_rate=0.12,
    )
    # Nominal stays at 10,000; real should be lower at the end.
    assert df["balance"].iloc[-1] == 10_000.0
    assert df["real_balance"].iloc[-1] < 10_000.0
    assert df["inflation_index"].iloc[-1] > 1.0
