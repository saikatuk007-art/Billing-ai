import streamlit as st
import pandas as pd

# Load billing data
billing = pd.read_csv('billing_data.csv')

# Load complaint data
complaints = pd.read_csv('complaints.csv')

# Clean Customer_ID fields to ensure proper merging
billing['Customer_ID'] = billing['Customer_ID'].astype(str).str.strip()
complaints['Customer_ID'] = complaints['Customer_ID'].astype(str).str.strip()

# Display title
st.title("📡 BillGuard AI Dashboard")

# Section 1: Billing Anomalies
st.header("🔍 Billing Anomalies")

if 'anomaly' not in billing.columns:
    st.warning("Anomaly column missing. Please run anomaly detection first.")
    anomalies = pd.DataFrame()  # Empty placeholder
    filtered_anomalies = anomalies
else:
    anomalies = billing[billing['anomaly'] == -1]

    # Plan type filter
    plan_options = anomalies['Plan_Type'].unique().tolist()
    selected_plan = st.selectbox("Filter anomalies by Plan Type:", options=["All"] + plan_options)

    if selected_plan != "All":
        filtered_anomalies = anomalies[anomalies['Plan_Type'] == selected_plan]
    else:
        filtered_anomalies = anomalies

    st.dataframe(filtered_anomalies)

# Section 2: Complaint Sentiment
st.header("💬 Complaint Sentiment Analysis")

if 'Sentiment' not in complaints.columns:
    st.warning("Sentiment column missing. Please run NLP analysis first.")
    filtered_complaints = complaints
else:
    # Sentiment filter
    sentiment_options = complaints['Sentiment'].unique().tolist()
    selected_sentiment = st.selectbox("Filter complaints by Sentiment:", options=["All"] + sentiment_options)

    if selected_sentiment != "All":
        filtered_complaints = complaints[complaints['Sentiment'] == selected_sentiment]
    else:
        filtered_complaints = complaints

    st.dataframe(filtered_complaints[['Complaint_ID', 'Customer_ID', 'Complaint_Text', 'Sentiment']])

# Section 3: Cross-reference
st.header("🔗 Cross-Reference: Anomalies & Complaints")

if not filtered_anomalies.empty:
    merged = pd.merge(filtered_anomalies, filtered_complaints, on='Customer_ID', how='left')

    expected_columns = ['Customer_ID', 'Plan_Type', 'Final_Bill', 'Complaint_Text', 'Sentiment']
    available_columns = [col for col in expected_columns if col in merged.columns]

    st.subheader("🔗 Filtered Cross-Reference")
    st.dataframe(merged[available_columns])
else:
    st.info("No anomalies detected or anomaly detection not yet run.")
