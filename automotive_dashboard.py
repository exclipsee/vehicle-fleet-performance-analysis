# automotive_dashboard.py
import pandas as pd
import streamlit as st
import plotly.express as px

# ===========================
# Page Configuration
# ===========================
st.set_page_config(
    page_title="Vehicle Fleet Performance Dashboard",
    page_icon="🚗",
    layout="wide"
)

# ===========================
# Load Dataset
# ===========================
@st.cache_data
def load_data(path):
    return pd.read_excel(path)

file_path = "automotive_data.xlsx"  # Adjust path if needed
df = load_data(file_path)

# ===========================
# Sidebar Filters
# ===========================
st.sidebar.header("🔍 Filters")
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
].copy()

# ===========================
# Derived Metrics
# ===========================
filtered_df["Efficiency (km/L)"] = filtered_df["Mileage (km)"] / filtered_df["Fuel Used (L)"]
filtered_df["Total Cost (€)"] = filtered_df["Fuel Used (L)"] * 1.8 + filtered_df["Maintenance Cost (€)"]  # assumed fuel price
filtered_df["Cost per km (€)"] = filtered_df["Total Cost (€)"] / filtered_df["Mileage (km)"]

# ===========================
# Dashboard Title
# ===========================
st.title("🚗 Vehicle Fleet Performance Dashboard")
st.markdown("Interactive dashboard for analyzing and optimizing your vehicle fleet’s performance.")

# ===========================
# Tabs Layout
# ===========================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Visualizations", "⚙️ Maintenance & Costs", "⬇️ Data Export"])

# ===========================
# TAB 1 - Overview (KPIs + Insights)
# ===========================
with tab1:
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Vehicles", filtered_df["Vehicle ID"].nunique())
    col2.metric("Total Mileage (km)", int(filtered_df["Mileage (km)"].sum()))
    col3.metric("Total Fuel Used (L)", int(filtered_df["Fuel Used (L)"].sum()))
    col4.metric("Total Trips", int(filtered_df["Total Trips"].sum()))

    st.markdown("---")
    st.subheader("📊 Automated Insights")

    top_brand = filtered_df.groupby("Brand")["Mileage (km)"].sum().idxmax()
    most_efficient_vehicle = (
        filtered_df.assign(Efficiency=lambda x: x["Mileage (km)"] / x["Fuel Used (L)"])
        .sort_values("Efficiency", ascending=False)
        .iloc[0]
    )

    st.markdown(f"- **Top Brand by Total Mileage:** {top_brand}")
    st.markdown(f"- **Most Fuel-Efficient Vehicle:** {most_efficient_vehicle['Model']} "
                f"({most_efficient_vehicle['Efficiency (km/L)']:.2f} km/L)")
    st.markdown(f"- **Average Cost per km:** €{filtered_df['Cost per km (€)'].mean():.2f}")

# ===========================
# TAB 2 - Visualizations
# ===========================
with tab2:
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

    # Monthly trends
    monthly_df = (
        filtered_df.groupby("Month")[["Mileage (km)", "Fuel Used (L)"]].sum().reset_index()
        .sort_values("Month")
    )
    fig_trend = px.line(
        monthly_df,
        x="Month",
        y=["Mileage (km)", "Fuel Used (L)"],
        title="Monthly Mileage and Fuel Usage Trends",
        markers=True
    )
    st.plotly_chart(fig_trend, use_container_width=True)

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

    # Fuel efficiency per driver
    fig_efficiency = px.bar(
        filtered_df.groupby("Driver_Name")["Efficiency (km/L)"].mean().reset_index(),
        x="Driver_Name",
        y="Efficiency (km/L)",
        title="Average Fuel Efficiency per Driver",
        color="Driver_Name",
        text_auto=".2f"
    )
    st.plotly_chart(fig_efficiency, use_container_width=True)

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

    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    corr_matrix = filtered_df[["Mileage (km)", "Fuel Used (L)", "Maintenance Cost (€)", "Total Trips", "Efficiency (km/L)"]].corr()
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlation between Metrics"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ===========================
# TAB 3 - Maintenance & Cost Analysis
# ===========================
with tab3:
    st.subheader("Maintenance & Cost Analysis")

    # Maintenance cost by model
    fig_maint = px.bar(
        filtered_df.groupby("Model")["Maintenance Cost (€)"].sum().reset_index(),
        x="Model",
        y="Maintenance Cost (€)",
        title="Maintenance Cost per Model",
        color="Model",
        text_auto=".2f"
    )
    st.plotly_chart(fig_maint, use_container_width=True)

    # Cost per km by brand
    fig_cost_eff = px.bar(
        filtered_df.groupby("Brand")["Cost per km (€)"].mean().reset_index(),
        x="Brand",
        y="Cost per km (€)",
        title="Average Operating Cost per km by Brand",
        color="Brand",
        text_auto=".2f"
    )
    st.plotly_chart(fig_cost_eff, use_container_width=True)

# ===========================
# TAB 4 - Data Export
# ===========================
with tab4:
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df.reset_index(drop=True))
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_vehicle_data.csv",
        mime="text/csv"
    )
