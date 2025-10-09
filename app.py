import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "automotive_data.xlsx"
df = pd.read_excel(file_path)

st.title("🚗 Vehicle Fleet Performance Dashboard")
st.subheader("Data Overview")
st.dataframe(df)

# Summary stats
st.subheader("Summary Statistics")
st.dataframe(df.describe())

# Example plot: Mileage by Vehicle Type
st.subheader("Mileage by Vehicle Type")
fig, ax = plt.subplots()
sns.barplot(data=df, x="Vehicle_Type", y="Mileage (km)", ax=ax)
st.pyplot(fig)

# Example plot: Total Trips per Station
st.subheader("Trips per Start Station (Top 10)")
top_stations = df["Start_Station"].value_counts().head(10)
st.bar_chart(top_stations)
