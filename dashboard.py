import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Log Monitoring Dashboard", layout="wide")

st.title("🚨 Log Monitoring & Anomaly Detection Dashboard")

# ---------------------------
# Helper Functions
# ---------------------------
def load_logs():
    if not os.path.exists("logs.txt"):
        return pd.DataFrame(columns=["log"])
    with open("logs.txt") as f:
        data = [line.strip() for line in f.readlines()]
    df = pd.DataFrame(data, columns=["log"])

    def classify(log):
        if "ERROR" in log:
            return "ERROR"
        elif "WARNING" in log:
            return "WARNING"
        else:
            return "INFO"

    df["level"] = df["log"].apply(classify)
    return df


def load_history():
    if not os.path.exists("history.txt"):
        return []
    with open("history.txt") as f:
        return [int(x.strip()) for x in f.readlines() if x.strip().isdigit()]


# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.header("⚙️ Controls")

auto_refresh = st.sidebar.checkbox("Auto Refresh (5 sec)", value=False)
filter_level = st.sidebar.multiselect(
    "Filter Log Level",
    ["INFO", "WARNING", "ERROR"],
    default=["INFO", "WARNING", "ERROR"]
)

search_term = st.sidebar.text_input("🔍 Search Logs")

# ---------------------------
# Load Data
# ---------------------------
df = load_logs()

# Apply filters
if filter_level:
    df = df[df["level"].isin(filter_level)]

if search_term:
    df = df[df["log"].str.contains(search_term, case=False)]

# ---------------------------
# Metrics
# ---------------------------
total_logs = len(df)
error_count = len(df[df["level"] == "ERROR"])
warning_count = len(df[df["level"] == "WARNING"])
info_count = len(df[df["level"] == "INFO"])

anomaly_rate = (error_count / total_logs * 100) if total_logs > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Logs", total_logs)
col2.metric("Errors", error_count)
col3.metric("Warnings", warning_count)
col4.metric("Anomaly Rate (%)", f"{anomaly_rate:.2f}")

# ---------------------------
# Charts
# ---------------------------
st.subheader("📊 Log Level Distribution")
dist_data = pd.DataFrame({
    "Level": ["INFO", "WARNING", "ERROR"],
    "Count": [info_count, warning_count, error_count]
})
st.bar_chart(dist_data.set_index("Level"))

# ---------------------------
# History Trend
# ---------------------------
st.subheader("📈 Anomaly Trend Over Time")

history = load_history()
if history:
    hist_df = pd.DataFrame(history, columns=["Anomalies"])
    st.line_chart(hist_df)
else:
    st.info("No history available yet")

# ---------------------------
# Logs Table (Pagination)
# ---------------------------
st.subheader("📄 Logs")

page_size = st.slider("Rows per page", 5, 50, 10)
total_pages = max(1, (len(df) + page_size - 1) // page_size)
page = st.number_input("Page", 1, total_pages, 1)

start = (page - 1) * page_size
end = start + page_size

st.dataframe(df.iloc[start:end], use_container_width=True)

# ---------------------------
# Download Report
# ---------------------------
if os.path.exists("report.txt"):
    with open("report.txt", "r") as f:
        st.download_button("⬇️ Download Report", f, file_name="report.txt")

# ---------------------------
# Auto Refresh
# ---------------------------
if auto_refresh:
    time.sleep(5)
    st.rerun()