from __future__ import annotations
import numpy as np
import pandas as pd

def add_control_limits(df: pd.DataFrame, column: str, sigma: float = 3.0) -> pd.DataFrame:
    """Add mean and 3-sigma limits using the supplied series (illustrative baseline)."""
    out = df.copy()
    values = pd.to_numeric(out[column], errors="coerce")
    center = values.mean()
    std = values.std(ddof=1)
    out["center_line"] = center
    out["ucl"] = center + sigma * std
    out["lcl"] = center - sigma * std
    out.attrs.update({"cl": center, "ucl": center + sigma * std, "lcl": center - sigma * std})
    return out

def detect_western_electric(df: pd.DataFrame, column: str) -> list[str]:
    """Flag points using four basic Western Electric-style rules.

    Limits and zones are estimated from the entire provided series for this demo.
    For operational SPC, estimate limits from a stable historical baseline.
    """
    x = pd.to_numeric(df[column], errors="coerce").to_numpy(dtype=float)
    mean = np.nanmean(x)
    std = np.nanstd(x, ddof=1)
    if not np.isfinite(std) or std == 0:
        return ["No signal"] * len(x)

    z = (x - mean) / std
    labels = ["No signal"] * len(x)
    for i in range(len(z)):
        if abs(z[i]) > 3:
            labels[i] = "Rule 1: beyond 3σ"
        elif i >= 2 and (np.sum(z[i-2:i+1] > 2) >= 2 or np.sum(z[i-2:i+1] < -2) >= 2):
            labels[i] = "Rule 2: 2 of 3 beyond 2σ"
        elif i >= 4 and (np.sum(z[i-4:i+1] > 1) >= 4 or np.sum(z[i-4:i+1] < -1) >= 4):
            labels[i] = "Rule 3: 4 of 5 beyond 1σ"
        elif i >= 7 and (np.all(z[i-7:i+1] > 0) or np.all(z[i-7:i+1] < 0)):
            labels[i] = "Rule 4: 8 consecutive on one side"
    return labels
