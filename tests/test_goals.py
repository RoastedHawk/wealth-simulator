import pandas as pd

from wealth_simulator.goals import time_to_target


def test_time_to_target_reaches():
    df = pd.DataFrame({"month": [1, 2, 3], "balance": [90, 100, 110]})
    res = time_to_target(df, target=100, column="balance")
    assert res.reached is True
    assert res.month == 2
    assert res.value_at_month == 100.0


def test_time_to_target_not_reached():
    df = pd.DataFrame({"month": [1, 2, 3], "balance": [10, 20, 30]})
    res = time_to_target(df, target=100, column="balance")
    assert res.reached is False
    assert res.month is None
    assert res.value_at_month is None
