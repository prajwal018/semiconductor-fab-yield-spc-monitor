from src.data_generator import generate_wafer_data
from src.pipeline import summarize_yield, lot_disposition
from src.spc import add_control_limits, detect_western_electric

def test_generated_data_shape_and_ranges():
    df = generate_wafer_data(n_lots=3, wafers_per_lot=4, seed=7)
    assert len(df) == 12
    assert df["yield_pct"].between(0, 100).all()
    assert df["wafer_id"].is_unique

def test_lot_summary_and_disposition():
    df = generate_wafer_data(n_lots=4, wafers_per_lot=5)
    assert len(summarize_yield(df)) == 4
    assert set(lot_disposition(df)["disposition"]).issubset({"NORMAL", "HOLD", "INVESTIGATE"})

def test_spc_outputs():
    df = generate_wafer_data(n_lots=5, wafers_per_lot=5)
    out = add_control_limits(df, "chamber_pressure_kpa")
    assert {"ucl", "lcl", "center_line"}.issubset(out.columns)
    assert len(detect_western_electric(out, "chamber_pressure_kpa")) == len(df)
