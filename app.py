import altair as alt
import pandas as pd
import streamlit as st

from wealth_simulator.sim import simulate_monthly

st.set_page_config(page_title="Wealth Simulator", layout="wide")

# ---------- Styling (cards) ----------
st.markdown(
    """
<style>
.card {
  border: 1px solid rgba(120,120,120,0.25);
  border-radius: 14px;
  padding: 14px 16px;
  background: rgba(255,255,255,0.55);
}
@media (prefers-color-scheme: dark) {
  .card { background: rgba(30,30,30,0.35); }
}
.card-title {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 6px;
}
.card-value {
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1.2;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Wealth Simulator")
st.caption("Explore how your money could grow over time with contributions + compounding.")

# ---------- Sidebar inputs ----------
with st.sidebar:
    st.header("Inputs")

    mode = st.radio("Mode", ["Single", "Compare scenarios"], horizontal=True)

    st.subheader("Scenario Presets")
    PRESETS = {
        "Conservative": {"annual_rate_pct": 4.0, "inflation_pct": 2.5},
        "Moderate": {"annual_rate_pct": 7.0, "inflation_pct": 2.5},
        "Aggressive": {"annual_rate_pct": 10.0, "inflation_pct": 2.5},
    }

    currency = st.selectbox(
        "Currency",
        ["USD ($)", "EUR (€)", "GBP (£)", "CHF (CHF)", "JPY (¥)"],
        index=0,
    )
    currency_symbol = {
        "USD ($)": "$",
        "EUR (€)": "€",
        "GBP (£)": "£",
        "CHF (CHF)": "CHF ",
        "JPY (¥)": "¥",
    }[currency]

    principal = st.number_input(
        f"Starting amount ({currency_symbol})",
        min_value=0.0,
        value=10_000.0,
        step=500.0,
    )
    monthly_contrib = st.number_input(
        f"Monthly contribution ({currency_symbol})",
        min_value=0.0,
        value=300.0,
        step=50.0,
    )
    years = st.slider("Years", 0, 50, 10, 1)

    if mode == "Single":
        rate_pct = st.slider("Annual interest rate (%)", 0.0, 20.0, 7.0, 0.1)
        inflation_pct = st.slider("Inflation rate (%)", 0.0, 15.0, 2.5, 0.1)
        selected = []
    else:
        selected = st.multiselect(
            "Select scenarios to compare",
            options=list(PRESETS.keys()),
            default=["Conservative", "Moderate", "Aggressive"],
        )
        # fallback values for the single-run summary/table below
        rate_pct = PRESETS["Moderate"]["annual_rate_pct"]
        inflation_pct = PRESETS["Moderate"]["inflation_pct"]

def money(x: float) -> str:
    return f"{currency_symbol}{x:,.2f}"

# ---------- One “primary” sim (used for summary + table) ----------
df = simulate_monthly(
    principal=float(principal),
    monthly_contribution=float(monthly_contrib),
    annual_rate=float(rate_pct) / 100.0,
    years=int(years),
    annual_inflation_rate=float(inflation_pct) / 100.0,
)

st.subheader("Growth Over Time")
view = st.radio("View", ["Nominal", "Real (inflation-adjusted)"], horizontal=True)

# ---------- Summary computations (based on selected view) ----------
final_value = float(df["balance"].iloc[-1])
total_contributions_only = float(df["contributions"].iloc[-1] - principal)
interest_earned_total = float(df["interest"].iloc[-1])

real_final_value = float(df["real_balance"].iloc[-1])
real_contributions_end = float(df["contributions"].iloc[-1] / df["inflation_index"].iloc[-1])
real_interest_earned = float(real_final_value - real_contributions_end)

if view == "Nominal":
    shown_interest = interest_earned_total
    shown_final = final_value
    suffix = ""
else:
    shown_interest = real_interest_earned
    shown_final = real_final_value
    suffix = " (Real)"

st.subheader("Summary")
st.caption("Breakdown of what you put in vs what your investments earned.")

def card(title: str, value: str) -> None:
    st.markdown(
        f"""
<div class="card">
  <div class="card-title">{title}</div>
  <div class="card-value">{value}</div>
</div>
""",
        unsafe_allow_html=True,
    )

r1 = st.columns(2)
with r1[0]:
    card("Starting Amount", money(float(principal)))
with r1[1]:
    card("Total Contributions", money(total_contributions_only))

r2 = st.columns(2)
with r2[0]:
    card(f"Interest Earned{suffix}", money(shown_interest))
with r2[1]:
    card(f"Final Value{suffix}", money(shown_final))

st.divider()

# ---------- Chart ----------
if mode == "Compare scenarios" and selected:
    frames = []
    for name in selected:
        preset = PRESETS[name]
        scenario_df = simulate_monthly(
            principal=float(principal),
            monthly_contribution=float(monthly_contrib),
            annual_rate=float(preset["annual_rate_pct"]) / 100.0,
            years=int(years),
            annual_inflation_rate=float(preset["inflation_pct"]) / 100.0,
        ).copy()
        scenario_df["Scenario"] = name
        frames.append(scenario_df)

    compare_df = pd.concat(frames, ignore_index=True)

    # Scenario endpoint tiles (outside any loop!)
    endpoints = compare_df.sort_values("month").groupby("Scenario", as_index=False).tail(1)
    metric_col = "balance" if view == "Nominal" else "real_balance"
    st.caption("Scenario outcomes at the end of the horizon")
    cols = st.columns(len(selected))
    for col, name in zip(cols, selected):
        value = float(endpoints.loc[endpoints["Scenario"] == name, metric_col].iloc[0])
        col.metric(name, money(value))

    y_col = "balance" if view == "Nominal" else "real_balance"
    y_title = "Balance" if view == "Nominal" else "Real Balance"

    line = (
        alt.Chart(compare_df)
        .mark_line()
        .encode(
            x=alt.X("month:Q", title="Month"),
            y=alt.Y(f"{y_col}:Q", title=y_title, axis=alt.Axis(format="~s", tickCount=6)),
            color=alt.Color("Scenario:N", title="Scenario"),
            tooltip=[
                alt.Tooltip("Scenario:N"),
                alt.Tooltip("month:Q", title="Month"),
                alt.Tooltip(f"{y_col}:Q", title=y_title, format=",.2f"),
            ],
        )
        .properties(height=380)
        .interactive()
    )
    st.altair_chart(line, use_container_width=True)

else:
    # Single-mode stacked chart (matches view)
    if view == "Nominal":
        stack_df = df[["month", "contributions", "interest"]].copy()
        stack_df["interest"] = stack_df["interest"].clip(lower=0)
        value_vars = ["contributions", "interest"]
        label_map = {"contributions": "Contributions", "interest": "Interest"}
        order_map = {"Contributions": 0, "Interest": 1}
    else:
        real_df = df[["month", "contributions", "inflation_index", "real_balance"]].copy()
        real_df["real_contributions"] = real_df["contributions"] / real_df["inflation_index"]
        real_df["real_interest"] = (real_df["real_balance"] - real_df["real_contributions"]).clip(lower=0)

        stack_df = real_df[["month", "real_contributions", "real_interest"]].copy()
        value_vars = ["real_contributions", "real_interest"]
        label_map = {"real_contributions": "Contributions (Real)", "real_interest": "Interest (Real)"}
        order_map = {"Contributions (Real)": 0, "Interest (Real)": 1}

    long_df = stack_df.melt(
        id_vars="month",
        value_vars=value_vars,
        var_name="component",
        value_name="amount",
    )
    long_df["component"] = long_df["component"].map(label_map)
    long_df["stack_order"] = long_df["component"].map(order_map)

    area = (
        alt.Chart(long_df)
        .mark_area()
        .encode(
            x=alt.X("month:Q", title="Month"),
            y=alt.Y("amount:Q", title="Amount", stack="zero", axis=alt.Axis(format="~s", tickCount=6)),
            color=alt.Color("component:N", title="", legend=alt.Legend(orient="bottom")),
            order=alt.Order("stack_order:Q", sort="ascending"),
            tooltip=[
                alt.Tooltip("month:Q", title="Month"),
                alt.Tooltip("component:N", title="Component"),
                alt.Tooltip("amount:Q", title="Amount", format=",.2f"),
            ],
        )
    )
    st.altair_chart(area.properties(height=380).interactive(), use_container_width=True)

# ---------- Table (single-run) ----------
with st.expander("See Table"):
    display_df = (
        df.rename(
            columns={
                "month": "Month",
                "contributions": "Contributions",
                "interest": "Interest",
                "balance": "Balance",
                "real_balance": "Real Balance",
            }
        )
        .loc[:, ["Month", "Contributions", "Interest", "Balance", "Real Balance"]]
        .copy()
    )

    for col in ["Contributions", "Interest", "Balance", "Real Balance"]:
        display_df[col] = display_df[col].round(2)

    st.dataframe(display_df, use_container_width=True, hide_index=True)