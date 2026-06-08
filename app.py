import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="COVID-19 Italy Dashboard", layout="wide")

st.title("🇮🇹 COVID-19 Italy Data Dashboard")
st.markdown("Interactive analysis of COVID-19 trends in Italy")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("covid_italy.csv")   # ✅ CHANGED HERE
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df

df = load_data()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")

min_date = df['date'].min()
max_date = df['date'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

if len(date_range) == 2:
    df = df[
        (df['date'] >= pd.to_datetime(date_range[0])) &
        (df['date'] <= pd.to_datetime(date_range[1]))
    ]

# ----------------------------
# KPIs
# ----------------------------
total_cases = df['total_cases'].max()
total_deaths = df['total_deaths'].max()
peak_cases = df['new_cases'].max()
peak_deaths = df['new_deaths'].max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cases", f"{total_cases:,.0f}")
col2.metric("Total Deaths", f"{total_deaths:,.0f}")
col3.metric("Peak Cases", f"{peak_cases:,.0f}")
col4.metric("Peak Deaths", f"{peak_deaths:,.0f}")

# ----------------------------
# DAILY CASES TREND
# ----------------------------
st.subheader("📈 Daily New Cases Trend")

fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df['date'], df['new_cases'])
ax.set_title("Daily COVID-19 Cases in Italy")
ax.set_xlabel("Date")
ax.set_ylabel("Cases")

st.pyplot(fig)

# ----------------------------
# DEATH TREND
# ----------------------------
st.subheader("💀 Daily Deaths Trend")

fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df['date'], df['new_deaths'], color='red')

st.pyplot(fig)

# ----------------------------
# CASES VS DEATHS
# ----------------------------
st.subheader("📊 Cases vs Deaths Comparison")

fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df['date'], df['new_cases'], label='Cases')
ax.plot(df['date'], df['new_deaths']*100, label='Deaths x100')
ax.legend()

st.pyplot(fig)

# ----------------------------
# CORRELATION HEATMAP
# ----------------------------
st.subheader("🔥 Correlation Heatmap")

corr = df[['new_cases','total_cases','new_deaths','total_deaths']].corr()

fig, ax = plt.subplots(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)

st.pyplot(fig)

# ----------------------------
# DATA TABLE
# ----------------------------
st.subheader("📄 Raw Data Preview")
st.dataframe(df.tail(50))