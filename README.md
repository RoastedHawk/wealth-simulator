 Wealth Simulator

Interactive wealth growth simulator built with **Python** + **Streamlit**.  
Adjust starting amount, monthly contributions, expected annual return, time horizon, and currency to see a clear breakdown of **Contributions vs. Interest** over time.

![Wealth Simulator screenshot](assets/app.png)

## Features
- Currency selector (display formatting)
- Monthly contribution + compounding simulation
- Summary cards: Starting Amount, Total Contributions, Interest Earned, Final Value
- Stacked area chart (Contributions + Interest)
- Inflation-adjusted (real) view with Nominal vs Real toggle
- Detailed results table
- Tested simulation core with `pytest`
- Linting with `ruff`

## Tech Stack
- Python (venv)
- Streamlit (UI)
- Pandas (data)
- Altair (charting)
- Pytest (tests)
- Ruff (lint)

## Getting Started

### 1) Clone
[bash]

git clone <YOUR_REPO_URL>
cd wealth-simulator

### 2) Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

### 3) Install dependencies
python -m pip install -e ".[dev]"
Run the App
streamlit run app.py
Run Tests
python -m pytest
Lint
ruff check .
Project Structure
wealth-simulator/
  app.py                      # Streamlit UI
  pyproject.toml              # dependencies + tool config
  src/wealth_simulator/       # simulation package
    __init__.py
    sim.py                    # core simulation logic
  tests/                      # pytest tests
    test_smoke.py
Roadmap

Add compounding frequency toggle (monthly/annual)

Add inflation-adjusted view (real vs nominal)

Add export: download CSV

Add scenarios/presets (Conservative / Moderate / Aggressive)

Resume Bullet Ideas

Built an interactive wealth simulator in Streamlit with parameterized inputs, performance visualization, and results breakdown.

Implemented a reusable simulation engine with monthly compounding and contributions, covered by automated unit tests (pytest).

Established a production-style Python project layout using pyproject.toml, editable installs, and Ruff linting.

## License
MIT
