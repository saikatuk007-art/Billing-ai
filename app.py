import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load billing data
billing = pd.read_csv('billing_data.csv')
complaints = pd.read_csv('complaints.csv')

# Clean Customer_ID fields
billing['Customer_ID'] = billing['Customer_ID'].astype(str).str.strip()
complaints['Customer_ID'] = complaints['Customer_ID'].astype(str).str.strip()

# Categorize complaints by topic
def categorize(text):
    text = str(text).lower()
    if "roaming" in text:
        return "Roaming Issue"
    elif "discount" in text:
        return "Discount Missing"
    elif "tax" in text:
        return "Tax Dispute"
    else:
        return "Other"

complaints['Category'] = complaints['Complaint_Text'].apply(categorize)

# Add timestamp if missing
if 'Timestamp' not in complaints.columns:
    complaints['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Title
st.title("📡 BillGuard AI Dashboard")

# Section 1: Billing Anomalies
st.header("🔍 Billing Anomalies")

if 'anomaly' not in billing.columns:
    st.warning("Anomaly column missing. Please run anomaly detection first.")
    anomalies = pd.DataFrame()
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

    # KPI Metrics
    st.metric("Total Anomalies", len(filtered_anomalies))

    # Bar chart
    st.subheader("📊 Anomalies by Plan Type")
    plan_counts = filtered_anomalies['Plan_Type'].value_counts()
    fig, ax = plt.subplots()
    ax.bar(plan_counts.index, plan_counts.values, color='tomato')
    ax.set_xlabel("Plan Type")
    ax.set_ylabel("Count")
    st.pyplot(fig)

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

    st.metric("Negative Complaints", len(filtered_complaints[filtered_complaints['Sentiment'] == 'NEGATIVE']))

