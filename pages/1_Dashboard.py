import streamlit as st
import pandas as pd
from utils.styles import apply_custom_styles

apply_custom_styles()

st.title("📊 Dashboard")

# Mock data for demonstration
data = {
    "Topic": ["BigQuery", "Dataflow", "Spanner", "Pub/Sub"],
    "Mastery": [80, 45, 60, 30]
}
df = pd.DataFrame(data)

col1, col2, col3 = st.columns(3)
col1.metric("Current Streak", "3 Days", "+1")
col2.metric("Total Questions", "42", "+5")
col3.metric("Avg Score", "78%", "+2%")

st.divider()

st.subheader("Topic Mastery")
st.bar_chart(df.set_index("Topic"))

st.caption("Keep practicing to improve your mastery scores!")
