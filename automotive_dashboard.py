# automotive_dashboard.py
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Modeling imports
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score

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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Visualizations", "⚙️ Maintenance & Costs", "⬇️ Data Export", "🔮 Predictive Model"])

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

# ===========================
# TAB 5 - Predictive Model
# ===========================
with tab5:
    st.subheader("Predictive Model — Estimate Efficiency or Cost")

    # Basic feature engineering (create more factors)
    df_model = filtered_df.copy()
    # avoid divide-by-zero
    df_model["Total Trips"] = df_model["Total Trips"].replace(0, np.nan)
    df_model["Avg Trip Distance (km)"] = df_model["Mileage (km)"] / df_model["Total Trips"]
    df_model["Fuel per Trip (L)"] = df_model["Fuel Used (L)"] / df_model["Total Trips"]
    df_model["Maintenance per km (€)"] = df_model["Maintenance Cost (€)"] / df_model["Mileage (km)"]
    df_model["Month_Num"] = pd.to_datetime(df_model["Month"], errors="coerce").dt.month
    # cyclic encoding for month
    df_model["Month_sin"] = np.sin(2 * np.pi * (df_model["Month_Num"].fillna(0) / 12))
    df_model["Month_cos"] = np.cos(2 * np.pi * (df_model["Month_Num"].fillna(0) / 12))

    # Fill simple missing values
    df_model["Avg Trip Distance (km)"].fillna(df_model["Avg Trip Distance (km)"].median(), inplace=True)
    df_model["Fuel per Trip (L)"].fillna(df_model["Fuel per Trip (L)"].median(), inplace=True)
    df_model["Maintenance per km (€)"].fillna(0, inplace=True)

    target_option = st.selectbox("Select target", ["Efficiency (km/L)", "Cost per km (€)"])

    st.markdown("Choose features to include in the model (keep it simple to avoid overfitting):")
    candidate_features = [
        "Mileage (km)", "Fuel Used (L)", "Total Trips",
        "Avg Trip Distance (km)", "Fuel per Trip (L)", "Maintenance per km (€)",
        "Month_sin", "Month_cos", "Brand", "Vehicle_Type", "Driver_Name", "Model"
    ]

    chosen = st.multiselect("Features", options=candidate_features, default=[
        "Avg Trip Distance (km)", "Fuel per Trip (L)", "Maintenance per km (€)", "Brand", "Vehicle_Type"
    ])

    if len(chosen) == 0:
        st.warning("Select at least one feature to train the model.")
    else:
        # Prepare data
        model_df = df_model[[target_option] + chosen].dropna()

        if model_df.shape[0] < 10:
            st.warning("Not enough rows to train a reliable model. Try widening filters.")
        else:
            X = model_df[chosen]
            y = model_df[target_option]

            # identify numeric and categorical
            numeric_feats = X.select_dtypes(include=[np.number]).columns.tolist()
            categorical_feats = [c for c in chosen if c not in numeric_feats]

            # Build preprocessing
            numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])
            categorical_transformer = Pipeline(steps=[
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse=False))
            ])

            preprocessor = ColumnTransformer(transformers=[
                ("num", numeric_transformer, numeric_feats),
                ("cat", categorical_transformer, categorical_feats)
            ], remainder="drop")

            # ElasticNetCV to balance bias/variance (avoids overfitting vs underfitting)
            model = Pipeline(steps=[
                ("preproc", preprocessor),
                ("clf", ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9], cv=5, n_alphas=50, random_state=42))
            ])

            # Train/Test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)

            st.markdown("**Model Performance (test set)**")
            st.write(f"RMSE: {rmse:.4f}")
            st.write(f"R^2: {r2:.4f}")

            # Plot actual vs predicted
            try:
                fig_pred = px.scatter(x=y_test, y=y_pred, labels={"x": "Actual", "y": "Predicted"}, title="Actual vs Predicted")
                fig_pred.add_shape(type="line", x0=y_test.min(), x1=y_test.max(), y0=y_test.min(), y1=y_test.max(), line=dict(color="red", dash="dash"))
                st.plotly_chart(fig_pred, use_container_width=True)
            except Exception:
                st.write("Could not render prediction plot.")

            # Show important coefficients (for linear model)
            try:
                # get feature names after preprocessing
                preproc = model.named_steps["preproc"]
                # numeric names
                feature_names = []
                if numeric_feats:
                    feature_names.extend(numeric_feats)
                if categorical_feats:
                    # OneHotEncoder categories
                    ohe = preproc.named_transformers_["cat"].named_steps["onehot"]
                    cat_names = ohe.get_feature_names_out(categorical_feats).tolist()
                    feature_names.extend(cat_names)

                coefs = model.named_steps["clf"].coef_
                coef_df = pd.DataFrame({"feature": feature_names, "coef": coefs})
                coef_df["abs_coef"] = coef_df["coef"].abs()
                coef_df = coef_df.sort_values("abs_coef", ascending=False).head(20)
                st.markdown("**Top feature coefficients**")
                st.dataframe(coef_df.reset_index(drop=True))
            except Exception:
                st.write("Could not extract feature coefficients for display.")

            st.markdown("---")
            st.markdown("Tips: Selecting a moderate number of informative features and using the built-in ElasticNet regularization helps prevent both overfitting and underfitting. Try different feature combinations.")
