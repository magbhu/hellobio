import streamlit as st
import pandas as pd
import altair as alt

st.title("📈 Magesh Stocks Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])

    # Filter only selected stocks
    selected_stocks = ["KARVYS", "STABAN", "BANMAH", "BANBAR"]
    df = df[df["Ticker"].isin(selected_stocks)]

    # Optional user selection
    tickers = st.multiselect("Select Tickers", options=selected_stocks, default=selected_stocks)

    filtered = df[df["Ticker"].isin(tickers)]

    # Plot weekly trends
    chart = alt.Chart(filtered).mark_line(point=True).encode(
        x="Date:T",
        y="Close:Q",
        color="Ticker:N",
        tooltip=["Date", "Ticker", "Close"]
    ).properties(
        width=800,
        height=400,
        title="Weekly Close Prices"
    ).interactive()

    st.altair_chart(chart)

    # Show data if needed
    with st.expander("📂 Show Raw Data"):
        st.dataframe(filtered)
