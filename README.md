# 🚗 Vehicle Fleet Performance Dashboard

An interactive Streamlit dashboard for analyzing and visualizing vehicle fleet performance using Python, Pandas, and Plotly.
Ideal for fleet managers, automotive analysts, or data enthusiasts seeking operational insights and cost efficiency from fleet data.

This project demonstrates modern data analytics, interactive visualization, and dynamic filtering — all in a responsive web interface.

──────────────────────────────────────────────
🛠️ FEATURES
──────────────────────────────────────────────

🎯 CORE FUNCTIONALITY
• Dynamic Filters – filter data by Brand, Vehicle Type, Driver, and Month
• KPI Cards – Total Vehicles, Total Mileage (km), Total Fuel Used (L), Total Trips

📊 INTERACTIVE VISUALIZATIONS
• Vehicles by Type – distribution of fleet composition
• Mileage by Brand – total mileage comparison
• Monthly Trends – mileage & fuel usage over time
• Mileage vs. Fuel Usage – scatter plot for efficiency analysis
• Fuel Efficiency per Driver – compare driving performance
• Maintenance Cost per Model – identify cost-intensive vehicles
• Trips per Route – analyze route activity
• Correlation Heatmap – explore metric relationships

💡 ANALYTICAL ENHANCEMENTS
• Automated Insights – top brand, most efficient vehicle, avg cost/km
• Cost Efficiency Metrics – operational cost per km (fuel + maintenance)

🧭 USER EXPERIENCE
• Tabbed Layout – Overview | Visualizations | Maintenance & Costs | Data Export
• Data Export – download filtered datasets (CSV)
• Caching Enabled – optimized with @st.cache_data
• Responsive Design – adapts to all screen sizes

──────────────────────────────────────────────
📊 TECHNOLOGIES USED
──────────────────────────────────────────────

• Python 3.13+
• Pandas
• Plotly Express
• Streamlit
• NumPy
• openpyxl, xlsxwriter

──────────────────────────────────────────────
🚀 HOW IT WORKS
──────────────────────────────────────────────

1️⃣ Prepare your dataset:
   The file should be named automotive_data.xlsx and placed in the same directory.

2️⃣ Run the dashboard:
   streamlit run automotive_dashboard.py

3️⃣ Explore:
   - Apply sidebar filters
   - View KPIs and charts
   - Analyze cost and efficiency metrics
   - Export filtered results

──────────────────────────────────────────────
⚙️ PROJECT STRUCTURE
──────────────────────────────────────────────

📁 vehicle-fleet-dashboard/
├── automotive_dashboard.py    → main Streamlit app
├── automotive_data.xlsx       → sample dataset
├── requirements.txt           → dependencies
└── README.md                  → documentation

──────────────────────────────────────────────
⚡ FUTURE IMPROVEMENTS
──────────────────────────────────────────────

• Predictive analytics for fleet performance
• AI-based efficiency recommendations
• Real-time IoT / telematics data integration
• PDF or Excel report exports
• Dark mode and customizable UI themes

──────────────────────────────────────────────
📸 SCREENSHOTS
──────────────────────────────────────────────
Coming soon — examples of KPIs, trends, and heatmaps.