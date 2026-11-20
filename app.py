import streamlit as st
import pandas as pd
import plotly.express as px
from src.pipeline import load_or_generate_data, summarize_yield, lot_disposition
from src.spc import add_control_limits, detect_western_electric

st.set_page_config(page_title="Fab Yield & SPC Monitor", page_icon="🏭", layout="wide")
st.title("Semiconductor Fab Yield & SPC Monitoring")
st.caption("Educational portfolio project using reproducible simulated wafer-fabrication data — not production fab data.")

with st.sidebar:
    st.header("Configuration")
    n_lots = st.slider("Number of lots", 10, 150, 40, 5)
    wafers_per_lot = st.slider("Wafers per lot", 5, 25, 12)
    refresh = st.button("Generate new dataset")
    st.markdown("---")
    st.caption("All measurements and limits are illustrative. Replace them with validated process specifications for real use.")

df = load_or_generate_data(n_lots=n_lots, wafers_per_lot=wafers_per_lot, refresh=refresh)
summary = summarize_yield(df)
disposition = lot_disposition(df)

total_wafers = len(df)
overall_yield = df["yield_pct"].mean()
avg_defects = df["defect_count"].mean()
hold_lots = (disposition["disposition"] == "HOLD").sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Wafers measured", f"{total_wafers:,}")
c2.metric("Mean wafer yield", f"{overall_yield:.1f}%")
c3.metric("Mean defects / wafer", f"{avg_defects:.1f}")
c4.metric("Lots flagged HOLD", int(hold_lots))

st.subheader("Yield by production lot")
lot_yield = df.groupby("lot_id", as_index=False).agg(yield_pct=("yield_pct", "mean"))
fig = px.line(lot_yield, x="lot_id", y="yield_pct", markers=True,
              title="Mean wafer yield by lot", labels={"lot_id":"Lot", "yield_pct":"Yield (%)"})
fig.add_hline(y=95, line_dash="dash", annotation_text="Illustrative target: 95%")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Yield distribution")
    st.plotly_chart(px.histogram(df, x="yield_pct", nbins=25, title="Wafer yield distribution"), use_container_width=True)
with right:
    st.subheader("Defect count by process module")
    mod = df.groupby("process_module", as_index=False)["defect_count"].mean()
    st.plotly_chart(px.bar(mod, x="process_module", y="defect_count", title="Average defects per wafer"), use_container_width=True)

st.subheader("SPC: chamber pressure trend")
spc = add_control_limits(df.sort_values("measurement_time"), "chamber_pressure_kpa")
signals = detect_western_electric(spc, "chamber_pressure_kpa")
spc["spc_signal"] = signals
fig = px.line(spc, x="measurement_time", y="chamber_pressure_kpa", color="spc_signal",
              title="Chamber pressure with 3-sigma control limits",
              color_discrete_map={"No signal":"#2563eb", "Rule 1: beyond 3σ":"#dc2626",
                                  "Rule 2: 2 of 3 beyond 2σ":"#f59e0b",
                                  "Rule 3: 4 of 5 beyond 1σ":"#7c3aed",
                                  "Rule 4: 8 consecutive on one side":"#059669"})
fig.add_hline(y=spc.attrs["ucl"], line_dash="dash", annotation_text="UCL")
fig.add_hline(y=spc.attrs["cl"], line_dash="dot", annotation_text="CL")
fig.add_hline(y=spc.attrs["lcl"], line_dash="dash", annotation_text="LCL")
st.plotly_chart(fig, use_container_width=True)
st.caption("The demo applies Western Electric-style run rules to individual measurements. A real process requires rational subgrouping and validated control-chart selection.")

st.subheader("Lot disposition support")
st.dataframe(disposition, use_container_width=True, hide_index=True)
st.warning("Disposition is a decision-support demonstration only. It must not be used to release, hold, or scrap real manufacturing material.")

st.subheader("Wafer-level data")
st.dataframe(df.head(100), use_container_width=True)
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download wafer dataset (CSV)", csv, "wafer_measurements.csv", "text/csv")
