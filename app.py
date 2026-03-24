import altair as alt
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

with st.sidebar:
    st.header("Inputs")

    currency = st.selectbox(
        "Currency",
        options=["USD ($)", "EUR (€)", "GBP (£)", "CHF (CHF)", "JPY (¥)"],
        index=0,
        help="Display currency for amounts (no FX conversion yet).",
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
        help="How much you start with today.",
    )

    monthly_contrib = st.number_input(
        f"Monthly contribution ({currency_symbol})",
        min_value=0.0,
        value=300.0,
        step=50.0,
        help="How much you add every month.",
    )

    rate_pct = st.slider(
        "Annual interest rate (%)",
        min_value=0.0,
        max_value=20.0,
        value=7.0,
        step=0.1,
        help="Expected average annual return.",
    )

    inflation_pct = st.slider(
        "Inflation rate (%)",
        min_value=0.0,
        max_value=15.0,
        value=2.5,
        step=0.1,
        help="Used to show inflation-adjusted (real) values.",
    )

    years = st.slider(
        "Years",
        min_value=0,
        max_value=50,
        value=10,
        step=1,
        help="How long you leave the money invested.",
    )

# ---------- Sim (from src/) ----------
df = simulate_monthly(
    principal=float(principal),
    monthly_contribution=float(monthly_contrib),
    annual_rate=float(rate_pct) / 100.0,
    years=int(years),
    annual_inflation_rate=float(inflation_pct) / 100.0,
)

# ---------- Chart controls ----------
st.subheader("Growth Over Time")

view = st.radio(
    "View",
    options=["Nominal", "Real (inflation-adjusted)"],
    horizontal=True,
)

# ---------- Summary computations ----------
final_value = float(df["balance"].iloc[-1])
total_contributions_only = float(df["contributions"].iloc[-1] - principal)
interest_earned_total = float(df["interest"].iloc[-1])

real_final_value = float(df["real_balance"].iloc[-1])
# In "real" terms, compare against inflation-adjusted contributions at the end
real_contributions_end = float(df["contributions"].iloc[-1] / df["inflation_index"].iloc[-1])
real_interest_earned = float(real_final_value - real_contributions_end)

def money(x: float) -> str:
    return f"{currency_symbol}{x:,.2f}"

# Choose what summary shows based on view
if view == "Nominal":
    shown_interest = interest_earned_total
    shown_final = final_value
    suffix = ""
else:
    shown_interest = real_interest_earned
    shown_final = real_final_value
    suffix = " (Real)"

# ---------- Summary tiles (2x2 cards) ----------
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
    card("Starting Amount", money(principal))
with r1[1]:
    card("Total Contributions", money(total_contributions_only))

r2 = st.columns(2)
with r2[0]:
    card(f"Interest Earned{suffix}", money(shown_interest))
with r2[1]:
    card(f"Final Value{suffix}", money(shown_final))

st.divider()

# ---------- Build chart data based on view ----------
if view == "Nominal":
    stack_df = df[["month", "contributions", "interest"]].copy()
    stack_df["interest"] = stack_df["interest"].clip(lower=0)

    value_vars = ["contributions", "interest"]
    label_map = {"contributions": "Contributions", "interest": "Interest"}
    order_map = {"Contributions": 0, "Interest": 1}
else:
    # Convert contributions and balance into "today's money" by dividing by inflation index
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
        y=alt.Y(
            "amount:Q",
            title="Amount",
            stack="zero",
            axis=alt.Axis(format="~s", tickCount=6),
        ),
        color=alt.Color(
            "component:N",
            title="",
            legend=alt.Legend(orient="bottom"),
        ),
        order=alt.Order("stack_order:Q", sort="ascending"),
        tooltip=[
            alt.Tooltip("month:Q", title="Month"),
            alt.Tooltip("component:N", title="Component"),
            alt.Tooltip("amount:Q", title="Amount", format=",.2f"),
        ],
    )
)

st.altair_chart(area.properties(height=380).interactive(), use_container_width=True)

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