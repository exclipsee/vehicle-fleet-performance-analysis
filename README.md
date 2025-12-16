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
| **Visualization** | Plotly Express |
| **Web Framework** | Streamlit |
| **File Handling** | openpyxl, xlsxwriter |

---

## ✅ Tests

This repository includes a small test suite for the modeling utilities.

- Run tests locally (from project root):

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

- The tests cover basic feature engineering and the model pipeline in `model_utils.py`.

## 🔮 Predictive Model (short)

The Streamlit app includes a simple predictive tab that demonstrates feature engineering and a regularized linear model (ElasticNet). Use the dashboard to experiment with features and targets without modifying code.

---
