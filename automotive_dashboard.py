# automotive_dashboard.py
import pandas as pd
import streamlit as st
import plotly.express as px

# ===========================
# Load dataset
# ===========================
file_path = "automotive_data.xlsx"  # make sure this is your expanded Excel file
df = pd.read_excel(file_path)

# ===========================
# Sidebar Filters
# ===========================
st.sidebar.header("Filters")
selected_brand = st.sidebar.multiselect("Select Brand", options=df["Brand"].unique(), default=df["Brand"].unique())
selected_type = st.sidebar.multiselect("Select Vehicle Type", options=df["Vehicle_Type"].unique(), default=df["Vehicle_Type"].unique())
selected_driver = st.sidebar.multiselect("Select Driver", options=df["Driver_Name"].unique(), default=df["Driver_Name"].unique())
selected_month = st.sidebar.multiselect("Select Month", options=df["Month"].unique(), default=df["Month"].unique())

# Filter dataframe
filtered_df = df[
    (df["Brand"].isin(selected_brand)) &
    (df["Vehicle_Type"].isin(selected_type)) &
    (df["Driver_Name"].isin(selected_driver)) &
    (df["Month"].isin(selected_month))
]

# ===========================
# Dashboard Title
# ===========================
st.title("🚗 Vehicle Fleet Performance Dashboard")
st.markdown("Interactive dashboard for fleet analysis: filter by brand, type, driver, and month.")

# ===========================
# KPI Cards
# ===========================
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Vehicles", filtered_df["Vehicle ID"].nunique())
col2.metric("Total Mileage (km)", filtered_df["Mileage (km)"].sum())
col3.metric("Total Fuel Used (L)", filtered_df["Fuel Used (L)"].sum())
col4.metric("Total Trips", filtered_df["Total Trips"].sum())

# ===========================
# Tables
# ===========================
st.subheader("Fleet Data")
st.dataframe(filtered_df.reset_index(drop=True))

# ===========================
# Charts
# ===========================
st.subheader("Visualizations")

# Vehicle count by type
fig_type = px.histogram(
    filtered_df, 
    x="Vehicle_Type", 
    title="Vehicles by Type",
    color="Vehicle_Type",
    text_auto=True
)
fig_type.update_layout(bargap=0.2)
st.plotly_chart(fig_type, use_container_width=True)

# Mileage by Brand
fig_mileage = px.bar(
    filtered_df.groupby("Brand")["Mileage (km)"].sum().reset_index(),
    x="Brand",
    y="Mileage (km)",
    title="Total Mileage by Brand",
    text="Mileage (km)",
    color="Brand"
)
st.plotly_chart(fig_mileage, use_container_width=True)

# Fuel usage vs Mileage scatter
fig_scatter = px.scatter(
    filtered_df,
    x="Mileage (km)",
    y="Fuel Used (L)",
    color="Vehicle_Type",
    size="Total Trips",
    hover_data=["Brand", "Model", "Driver_Name"],
    title="Mileage vs Fuel Usage"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Maintenance cost by Vehicle
fig_maint = px.bar(
    filtered_df.groupby("Model")["Maintenance Cost (€)"].sum().reset_index(),
    x="Model",
    y="Maintenance Cost (€)",
    title="Maintenance Cost per Model",
    color="Model",
    text="Maintenance Cost (€)"
)
st.plotly_chart(fig_maint, use_container_width=True)

# Trips per route
st.subheader("Trips per Route")
route_df = filtered_df.groupby(["Start_Station", "End_Station"])["Total Trips"].sum().reset_index()
fig_route = px.bar(
    route_df,
    x="Start_Station",
    y="Total Trips",
    color="End_Station",
    title="Total Trips per Route",
    text="Total Trips"
)
st.plotly_chart(fig_route, use_container_width=True)

# ===========================
# Correlation heatmap
# ===========================
st.subheader("Correlation Heatmap")
corr_matrix = filtered_df[["Mileage (km)", "Fuel Used (L)", "Maintenance Cost (€)", "Total Trips"]].corr()
fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Correlation between Metrics"
)
st.plotly_chart(fig_corr, use_container_width=True)
