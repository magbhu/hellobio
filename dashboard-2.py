import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(
    page_title="Personal Stocks Dashboard - OrchidLab",
    page_icon="📈",
    layout="wide"
)

# --- Load Data (CSV or JSON) ---
@st.cache_data # Cache the data loading for performance
def load_data(file_path, file_type):
    #df = pd.read_json('stocks.json')
    df = pd.read_csv('stocks.csv')
    # Calculate derived metrics
    df['market_value'] = df['quantity'] * df['ltp']
    df['gain_loss'] = (df['ltp'] - df['average_cost_price']) * df['quantity']
    df['percentage_gain_loss'] = (df['gain_loss'] / (df['average_cost_price'] * df['quantity'])) * 100
    return df


# --- Sidebar for File Upload ---
st.sidebar.header("Upload Stock Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

data_source_df = pd.DataFrame()
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    data_source_df = load_data(uploaded_file, file_extension)
    st.sidebar.success("File loaded successfully!")
else:
    st.sidebar.info("Upload a CSV or JSON file to get started.")
    # Optional: Load a default dataset if no file is uploaded for demonstration
    # You can comment out or remove this block if you always expect a file upload
    try:
        # Assuming you have 'stocks.csv' or 'stocks.json' in the same directory
        data_source_df = load_data('stocks.csv', 'csv') # Or 'stocks.json', 'json'
        st.sidebar.info("Loaded default 'stocks.csv' for demonstration.")
    except FileNotFoundError:
        st.sidebar.warning("No file uploaded and default data not found. Please upload a file.")


# --- Dashboard Layout ---
st.title("💰 Stocks Portfolio Dashboard - OrchidLab")
st.markdown("An interactive dashboard to visualize your stock holdings.")

if not data_source_df.empty:
    # --- Key Metrics ---
    total_market_value = data_source_df['market_value'].sum()
    total_gain_loss = data_source_df['gain_loss'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Market Value", f"₹ {total_market_value:,.2f}")
    with col2:
        st.metric("Total Gain/Loss", f"₹ {total_gain_loss:,.2f}", delta=f"{total_gain_loss:,.2f}")
    with col3:
        st.metric("Number of Stocks", len(data_source_df))

    st.markdown("---")

    # --- Interactive Table ---
    st.subheader("Stock Holdings Overview")
    st.dataframe(data_source_df.style.format({
        'average_cost_price': "₹ {:.2f}",
        'ltp': "₹ {:.2f}",
        'market_value': "₹ {:.2f}",
        'gain_loss': "₹ {:.2f}",
        'percentage_gain_loss': "{:.2f}%"
    }), use_container_width=True)

    st.markdown("---")

    # --- Visualizations ---
    st.subheader("Portfolio Distribution by Market Value")
    fig_pie = px.pie(
        data_source_df,
        values='market_value',
        names='stock_code',
        title='Portfolio Market Value Distribution',
        hole=0.3,
        hover_data=['quantity', 'average_cost_price', 'ltp', 'gain_loss']
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Gain/Loss per Stock")
    fig_bar = px.bar(
        data_source_df,
        x='stock_code',
        y='gain_loss',
        title='Gain/Loss per Stock',
        color='gain_loss',
        color_continuous_scale=px.colors.sequential.RdBu, # Red for loss, Blue for gain
        hover_data=['quantity', 'average_cost_price', 'ltp', 'market_value']
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Market Value vs. Average Cost Price")
    fig_scatter = px.scatter(
        data_source_df,
        x='average_cost_price',
        y='ltp',
        size='quantity',
        color='stock_code',
        hover_name='stock_code',
        title='LTP vs. Average Cost Price (Size by Quantity)',
        labels={'average_cost_price': 'Average Cost Price (₹)', 'ltp': 'Last Traded Price (₹)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.info("No data available to display the dashboard. Please upload a file from the sidebar.")

st.markdown("---")
st.caption("Data is for demonstration purposes only and may not reflect real-time market data.")