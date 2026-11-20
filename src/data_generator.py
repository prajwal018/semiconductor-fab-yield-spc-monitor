from __future__ import annotations
import numpy as np
import pandas as pd

PROCESS_MODULES = ["Lithography", "Etch", "Deposition", "CMP", "Implant"]

def generate_wafer_data(n_lots: int = 40, wafers_per_lot: int = 12, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic wafer-level process and electrical-test measurements."""
    rng = np.random.default_rng(seed)
    rows = []
    start = pd.Timestamp("2025-01-01 08:00:00")
    lot_shift = rng.normal(0, 0.7, n_lots)

    for lot_num in range(1, n_lots + 1):
        lot_id = f"LOT-{lot_num:04d}"
        module = PROCESS_MODULES[(lot_num - 1) % len(PROCESS_MODULES)]
        tool_id = f"TOOL-{(lot_num % 6) + 1:02d}"
        excursion = (lot_num % 13 == 0)
        for wafer_num in range(1, wafers_per_lot + 1):
            pressure = 50 + lot_shift[lot_num - 1] + rng.normal(0, 0.85)
            temperature = 350 + rng.normal(0, 2.8)
            cd_nm = 45 + 0.45 * (pressure - 50) + rng.normal(0, 1.1)
            defect_count = max(0, int(rng.poisson(8 + max(cd_nm - 45, 0) * 1.4)))
            if excursion:
                pressure += 4.2
                cd_nm += 2.8
                defect_count += int(rng.integers(8, 18))

            # Illustrative pass/fail outcome influenced by defects and process drift.
            fail_probability = np.clip(0.025 + defect_count * 0.003 + max(cd_nm - 46, 0) * 0.025, 0.01, 0.65)
            die_total = 1000
            failed_die = int(rng.binomial(die_total, fail_probability))
            yield_pct = 100 * (die_total - failed_die) / die_total
            leakage_ua = max(0.05, 0.45 + 0.035 * defect_count + rng.normal(0, 0.12))
            vth_v = 0.70 + 0.004 * (cd_nm - 45) + rng.normal(0, 0.012)

            rows.append({
                "lot_id": lot_id,
                "wafer_id": f"{lot_id}-W{wafer_num:02d}",
                "wafer_number": wafer_num,
                "process_module": module,
                "tool_id": tool_id,
                "measurement_time": start + pd.Timedelta(hours=(lot_num - 1) * 3 + wafer_num * 0.08),
                "chamber_pressure_kpa": round(float(pressure), 3),
                "process_temperature_c": round(float(temperature), 2),
                "critical_dimension_nm": round(float(cd_nm), 3),
                "defect_count": defect_count,
                "leakage_current_ua": round(float(leakage_ua), 4),
                "threshold_voltage_v": round(float(vth_v), 4),
                "die_total": die_total,
                "die_fail": failed_die,
                "yield_pct": round(float(yield_pct), 2),
                "simulated_excursion": bool(excursion),
            })
    return pd.DataFrame(rows)
