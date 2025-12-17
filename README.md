# 🚗 Vehicle Fleet Performance Dashboard

An **interactive Streamlit dashboard** for analyzing and visualizing **vehicle fleet performance** using **Python**, **Pandas**, and **Plotly**.  
Built for **fleet managers**, **automotive analysts**, and **data enthusiasts** who want actionable insights into fleet operations, efficiency, and costs.  

This project demonstrates end-to-end **data analytics**, **interactive visualization**, and **dynamic filtering** - all in a modern, web-based dashboard.

---

## 🧭 Overview

The **Vehicle Fleet Performance Dashboard** allows you to:

- Monitor key operational metrics in real time  
- Identify top-performing vehicles, brands, and drivers  
- Analyze fuel efficiency, maintenance costs, and trip routes  
- Export filtered data for deeper analysis or reporting  

---

## 🛠️ Features

### 🎯 **Core Functionality**
- 🔍 Dynamic sidebar filters for:
  - `Brand`
  - `Vehicle Type`
  - `Driver`
  - `Month`
- 🧾 Real-time **KPI cards**:
  - **Total Vehicles**
  - **Total Mileage (km)**
  - **Total Fuel Used (L)**
  - **Total Trips**

---

### 📊 **Interactive Visualizations**

| Visualization | Description |
|----------------|-------------|
| 🚙 **Vehicles by Type** | Distribution of fleet composition |
| 🏁 **Mileage by Brand** | Compare mileage across brands |
| 📅 **Monthly Trends** | Track mileage and fuel usage over time |
| ⛽ **Mileage vs Fuel Usage** | Analyze fuel efficiency relationships |
| 👨‍✈️ **Fuel Efficiency per Driver** | Identify top-performing drivers |
| 🔧 **Maintenance Cost per Model** | Find cost-intensive vehicle models |
| 🚉 **Trips per Route** | Visualize route-level activity |
| 🧩 **Correlation Heatmap** | Explore relationships between core metrics |

---

### 💡 **Analytical Enhancements**
- 📈 **Automated Insights**  
  Get instant insights like:
  - Top brand by total mileage  
  - Most fuel-efficient vehicle  
  - Average cost per km  

- 💰 **Cost Efficiency Metrics**  
  Calculates **total operational cost per km** (fuel + maintenance).

---

### 🧭 **User Experience**
- 🗂️ **Tabbed Layout**:
  - `Overview`
  - `Visualizations`
  - `Maintenance & Costs`
  - `Data Export`
- ⚡ **Instant Data Export** as CSV  
- 🚀 **Caching with `@st.cache_data`** for performance  
- 📱 **Responsive Layout** for desktop and mobile  

---

## ⚙️ Technologies Used

| Category | Technology |
|-----------|-------------|
| **Language** | Python 3.13+ |
| **Data Handling** | Pandas, NumPy |
# 🚗 Vehicle Fleet Performance Dashboard

[![CI](https://github.com/exclipsee/vehicle-fleet-performance-analysis/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/exclipsee/vehicle-fleet-performance-analysis/actions/workflows/ci.yml)

An interactive Streamlit dashboard for analyzing and visualizing vehicle fleet performance using Python, Pandas, and Plotly.

This project helps fleet managers and analysts monitor efficiency, costs, and usage across a vehicle fleet using interactive visualizations and lightweight predictive tools.

---

## Quick Start

1. Clone the repository:

```powershell
git clone https://github.com/exclipsee/vehicle-fleet-performance-analysis.git
cd vehicle-fleet-performance-analysis
```

2. Create a virtual environment and install pinned dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

3. Run the Streamlit app:

```powershell
streamlit run automotive_dashboard.py
```

---

## Features (high level)

- Interactive filters: Brand, Vehicle Type, Driver, Month
- KPI cards: total vehicles, mileage, fuel used, trips
- Visualizations: mileage by brand, monthly trends, efficiency scatter, maintenance costs
- Predictive tab: simple feature engineering + ElasticNet model for estimating efficiency or cost

---

## Tests

Run the test suite (unit tests cover the small modeling utilities):

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

---

## Contributing

Feel free to open issues or PRs. Small ways to help:

- Add dataset examples in `data/` for reproducibility
- Improve tests or add CI matrix entries
- Add a Dockerfile for a reproducible container

---

## Notes

- Dependencies are pinned in `requirements.txt` for reproducible installs.
- CI runs tests on push/PR to `main` using GitHub Actions.
