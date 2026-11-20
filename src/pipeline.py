from __future__ import annotations
from pathlib import Path
import pandas as pd
from .data_generator import generate_wafer_data

DATA_PATH = Path("data/wafer_measurements.csv")

def load_or_generate_data(n_lots: int = 40, wafers_per_lot: int = 12, refresh: bool = False) -> pd.DataFrame:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if refresh or not DATA_PATH.exists():
        df = generate_wafer_data(n_lots=n_lots, wafers_per_lot=wafers_per_lot)
        df.to_csv(DATA_PATH, index=False)
    else:
        df = pd.read_csv(DATA_PATH, parse_dates=["measurement_time"])
    return df

def summarize_yield(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("lot_id", as_index=False).agg(
        wafers=("wafer_id", "count"),
        mean_yield_pct=("yield_pct", "mean"),
        mean_defects=("defect_count", "mean"),
        mean_cd_nm=("critical_dimension_nm", "mean"),
    )

def lot_disposition(df: pd.DataFrame, yield_hold_threshold: float = 93.0,
                    defect_hold_threshold: float = 22.0) -> pd.DataFrame:
    """Transparent illustrative triage rule; not a production release rule."""
    lots = summarize_yield(df)
    lots["disposition"] = "NORMAL"
    lots.loc[
        (lots["mean_yield_pct"] < yield_hold_threshold) |
        (lots["mean_defects"] > defect_hold_threshold), "disposition"
    ] = "HOLD"
    lots.loc[
        (lots["mean_yield_pct"].between(yield_hold_threshold, 95.0)) |
        (lots["mean_defects"].between(15, defect_hold_threshold)), "disposition"
    ] = "INVESTIGATE"
    lots["reason"] = lots.apply(
        lambda r: "; ".join(
            reason for condition, reason in [
                (r["mean_yield_pct"] < yield_hold_threshold, "Mean yield below demo threshold"),
                (r["mean_defects"] > defect_hold_threshold, "Mean defect count above demo threshold"),
                (r["mean_yield_pct"] <= 95.0, "Yield near/below demo target"),
                (r["mean_defects"] >= 15, "Elevated defect count"),
            ] if condition
        ) or "No demo rule triggered", axis=1
    )
    return lots.sort_values(["disposition", "mean_yield_pct"], ascending=[True, True])
