# Semiconductor Fab Yield & SPC Monitoring

An end-to-end Python portfolio project for semiconductor manufacturing analytics. It generates reproducible synthetic wafer/lot data, stores a CSV snapshot, computes yield summaries, applies illustrative SPC run rules, and provides a Streamlit dashboard with lot-level disposition support.

> **Important:** This project uses synthetic educational data and illustrative thresholds. It is not validated for production manufacturing, real lot release, hold, or scrap decisions. Do not represent the generated data as GlobalFoundries or any other fab's production data.

## Why this project is relevant

The project demonstrates skills relevant to yield engineering and production sustaining:
- Wafer/lot yield monitoring and defect trend analysis
- Process parameter monitoring and basic SPC
- Lot-level risk triage and investigation prioritization
- Python, Pandas, NumPy, SQL-ready data modelling, and Streamlit visualization
- Reproducible data generation and automated tests

## Features

1. Synthetic wafer-level data for multiple lots, tools, and process modules.
2. Process variables: chamber pressure, temperature, critical dimension (CD).
3. Electrical-test-style variables: leakage current and threshold voltage.
4. Yield and defect metrics at wafer and lot levels.
5. SPC dashboard with center line, control limits, and four Western Electric-style signal rules.
6. Transparent NORMAL / INVESTIGATE / HOLD demo triage.
7. CSV export and unit tests.

## Project structure

```text
semiconductor-fab-yield-spc-monitor/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── data_generator.py
│   ├── pipeline.py
│   └── spc.py
└── tests/
    └── test_project.py
```

## Setup on Windows

Open PowerShell in the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

## Run the dashboard

```powershell
streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`.

## Run tests

```powershell
pytest -q
```

## Data dictionary

| Field | Meaning |
|---|---|
| lot_id | Synthetic production lot identifier |
| wafer_id | Unique synthetic wafer identifier |
| process_module | Illustrative process module |
| tool_id | Synthetic tool identifier |
| chamber_pressure_kpa | Simulated chamber pressure |
| process_temperature_c | Simulated process temperature |
| critical_dimension_nm | Simulated critical dimension |
| defect_count | Simulated defect count |
| leakage_current_ua | Simulated leakage current |
| threshold_voltage_v | Simulated threshold voltage |
| die_total / die_fail | Total and failed die counts |
| yield_pct | 100 × (total die − failed die) / total die |
| simulated_excursion | Flag identifying injected synthetic excursions |

## Method notes and limitations

- The current demo estimates SPC mean and standard deviation from the displayed data. In a production-quality SPC system, limits should be estimated from a verified stable baseline, and chart selection should reflect the sampling plan (for example, I-MR or X-bar/R).
- The Western Electric-style rules are educational signals, not a substitute for a fab's control plan.
- The disposition thresholds are configurable demonstration values, not engineering specifications.
- Correlation is not causation. A suspected parameter should be confirmed through engineering review, process knowledge, and controlled experiments.
- The synthetic relationship between process parameters, defects, and yield is intentionally simplified.

## Suggested extensions

- Add an SQL database layer (SQLite/PostgreSQL) and lot/wafer/process tables.
- Add electrical parametric limits and failure-bin Pareto analysis.
- Add wafer-map spatial defect visualization.
- Add Cp/Cpk using validated specification limits.
- Add FMEA scoring (severity, occurrence, detection, RPN).
- Add explainable ML for yield-risk ranking, with leakage-safe train/test splitting by lot.
- Add an investigation report with evidence, suspected causes, containment, and follow-up actions.

## Resume description (use only after running and understanding the project)

**Semiconductor Fab Yield & SPC Monitoring Dashboard** | Python, Pandas, NumPy, Streamlit, Plotly, SPC

- Developed a Python dashboard to analyze wafer- and lot-level yield, defect trends, and process measurements using reproducible synthetic semiconductor manufacturing data.
- Implemented illustrative 3-sigma control limits and Western Electric-style run rules to flag potential process excursions and prioritize lot investigations.
- Built transparent lot-level triage logic and interactive visualizations for yield monitoring, process trends, and defect analysis.

Replace or qualify these bullets based on the features you personally implement and validate.
