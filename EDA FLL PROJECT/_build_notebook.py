# Build the Colab notebook: copy COMPLETE + extra parallel sections
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).parent
src = json.loads((ROOT / "Smart_Urban_Transportation_EDA_COMPLETE.ipynb").read_text(encoding="utf-8"))

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [line + "\n" for line in text.strip("\n").split("\n")]}

def code(text):
    lines = text.strip("\n").split("\n")
    src_lines = [l + "\n" for l in lines]
    if src_lines:
        src_lines[-1] = src_lines[-1].rstrip("\n")
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src_lines}

# Enrich title cell with parallel-document note
src["cells"][0]["source"] = [
    "# 🚦 Smart Urban Transportation Systems\n",
    "## Complete Exploratory Data Analysis — São Paulo Urban Traffic (UCI 483)\n",
    "\n",
    "---\n",
    "\n",
    "**Student:** Hemavathy K  \n",
    "**Institution:** Kumaraguru College of Technology (KCT)  \n",
    "**Subject:** Exploratory Data Analysis (EDA)  \n",
    "**Dataset:** UCI ML Repository ID 483 — Behavior of the Urban Traffic of the City of São Paulo, Brazil  \n",
    "**DOI:** 10.24432/C5902F  |  **License:** CC BY 4.0  \n",
    "**Tools:** Google Colab · pandas · seaborn · scikit-learn · Power BI\n",
    "\n",
    "---\n",
    "\n",
    "## How this notebook maps to the Word report\n",
    "Every numbered section below has a **matching chapter with the same number** in  \n",
    "`Smart_Urban_Transportation_FULL_PROJECT_REPORT.docx`.\n",
    "\n",
    "| Run this Colab section | Read this Word chapter |\n",
    "|---|---|\n",
    "| 1 Project Overview | Chapter 1 |\n",
    "| 2 Setup & Data Loading | Chapter 2 |\n",
    "| 3 Initial Examination | Chapter 3 |\n",
    "| 4 Cleaning & Feature Engineering | Chapter 4 |\n",
    "| 5 Descriptive Statistics | Chapter 5 |\n",
    "| 6 Univariate Analysis | Chapter 6 |\n",
    "| 7 Time-Based Analysis | Chapter 7 |\n",
    "| 8 Incident Frequency | Chapter 8 |\n",
    "| 9 Relationship Analysis | Chapter 9 |\n",
    "| 10 Correlation Analysis | Chapter 10 |\n",
    "| 11 Outlier Analysis | Chapter 11 |\n",
    "| 12 Top / Bottom Observations | Chapter 12 |\n",
    "| 13 Predictive Baseline | Chapter 13 |\n",
    "| 14 Key Insights | Chapter 15 |\n",
    "| 15 Power BI Export | Chapter 14 |\n",
    "| 16 Extra Visualizations | Chapter 6–10 (extended charts) |\n",
    "\n",
    "**How to run:** File → Upload notebook in Google Colab → Runtime → Run all.\n",
    "The dataset downloads automatically from UCI. If that fails, upload the CSV from the UCI page.\n",
]

extra = []

extra.append(md("""
## 15. Power BI Export — Star Schema Tables

### Why?
Power BI is the stakeholder-facing dashboard. Python charts are excellent for analysis, but traffic managers need **filters, KPIs and drill-down** without re-running code. We export a **star schema**: one fact table plus dimensions and summary tables.

### What is used?
- `traffic_clean.csv` — 135-row fact table (every engineered feature + predictions)
- `dim_time.csv` / `dim_weekday.csv` — time and weekday dimensions
- `incidents_long.csv` — melted incidents (one row per slot × incident type)
- `incident_impact.csv` — present-vs-absent impact ranking
- `model_coefficients.csv` — linear what-if model for the simulator
- `thresholds.csv` — Low / High risk cut-offs
- Extra summaries: weekday, period, hourly, peak vs off-peak, KPIs, feature importance

### How?
`df.to_csv(...)` writes UTF-8 CSVs. In Colab, the last cell also zips the folder so you can **download one file** and load it into Power BI Desktop.
"""))

extra.append(code(r"""
# ─── 15. Linear coefficients (interpretable what-if model) ───────────────────
from pathlib import Path
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

df['Hour_code_sq'] = df['Hour_code'] ** 2
lin_feats = ['Hour_code', 'Hour_code_sq', 'Lack_of_electricity',
             'Point_of_flooding', 'Semaphore_off',
             'Defect_in_the_network_of_trolleybuses', 'Fire_vehicles']
lin = LinearRegression().fit(df[lin_feats], df[TARGET])
coef_df = pd.DataFrame({
    'Feature': ['Intercept'] + lin_feats,
    'Coefficient': [lin.intercept_] + list(lin.coef_),
    'Max_Value': [np.nan] + [df[c].max() for c in lin_feats]
})
print('Linear model R² (in-sample, for simulator only):',
      round(r2_score(df[TARGET], lin.predict(df[lin_feats])), 3))
display(coef_df.round(5))

# Feature importance table for Power BI
fi_df = pd.DataFrame({
    'Feature': FEATURES,
    'Importance': best_model.feature_importances_
}).sort_values('Importance', ascending=False)
fi_df['Importance_Pct'] = (fi_df['Importance'] * 100).round(2)
fi_df['Rank'] = range(1, len(fi_df) + 1)

# Incident impact (reuse pa_df from section 9)
impact = pa_df.copy()
impact = impact.rename(columns={
    'Incident': 'Incident', 'n_with': 'Obs_With', 'n_without': 'Obs_Without',
    'mean_with': 'Avg_Slowness_With', 'mean_without': 'Avg_Slowness_Without',
    'diff_+/-': 'Impact_Points', 'p_value': 'P_Value'
})
impact['Incident_Col'] = INCIDENTS
impact['Total_Events'] = [int(df[c].sum()) for c in INCIDENTS]
impact['Pct_Obs_With'] = (impact['Obs_With'] / len(df) * 100).round(1)
impact['Correlation'] = [round(df[c].corr(df[TARGET]), 3) for c in INCIDENTS]
impact['Impact_Rank'] = impact['Impact_Points'].rank(ascending=False, method='min').astype(int)

# Long incidents
inc_long = df.melt(
    id_vars=['Row_ID', 'Weekday', 'Weekday_Num', 'Time', 'Hour_code', 'Period', TARGET],
    value_vars=INCIDENTS, var_name='Incident_Col', value_name='Incident_Count'
)
inc_long['Incident'] = inc_long['Incident_Col'].str.replace('_', ' ')
inc_long['Has_Incident'] = (inc_long['Incident_Count'] > 0).astype(int)

# Dimensions
dim_time = df[['Hour_code', 'Time', 'Hour_decimal', 'Period', 'Period_Order', 'Is_Peak_Hour']].drop_duplicates().sort_values('Hour_code')
dim_weekday = df[['Weekday', 'Weekday_Num', 'Date']].drop_duplicates().sort_values('Weekday_Num')
thresholds = pd.DataFrame({'Name': ['Low_Max', 'High_Min'], 'Value': [7.9, 10.9]})

# Extra dashboard tables
kpi = pd.DataFrame({
    'KPI': ['Avg Slowness %', 'Median Slowness %', 'Peak Slowness %', 'Total Incident Events',
            'High Risk Slots', 'Outlier Slots', 'RF CV R2', 'Observations'],
    'Value': [round(df[TARGET].mean(), 2), round(df[TARGET].median(), 2), round(df[TARGET].max(), 2),
              int(df['Total_incidents'].sum()), int((df['Risk_Level']=='High').sum()),
              int(df['Is_Outlier'].sum()), results['Random Forest']['R2'], len(df)]
})
weekday_sum = df.groupby(['Weekday', 'Weekday_Num'], as_index=False).agg(
    Avg_Slowness=(TARGET, 'mean'), Max_Slowness=(TARGET, 'max'),
    Total_Incidents=('Total_incidents', 'sum'), High_Risk_Slots=('Risk_Level', lambda s: (s=='High').sum())
).sort_values('Weekday_Num')
period_sum = df.groupby(['Period', 'Period_Order'], as_index=False).agg(
    Avg_Slowness=(TARGET, 'mean'), Total_Incidents=('Total_incidents', 'sum'), N=('Row_ID', 'count')
).sort_values('Period_Order')
hourly_sum = df.groupby(['Hour_code', 'Time', 'Period'], as_index=False).agg(
    Avg_Slowness=(TARGET, 'mean'), Std_Slowness=(TARGET, 'std'),
    Avg_Incidents=('Total_incidents', 'mean')
)
peak_sum = df.groupby(['Weekday', 'Weekday_Num', 'Is_Peak_Hour'], as_index=False).agg(
    Avg_Slowness=(TARGET, 'mean'), N=('Row_ID', 'count')
)
risk_sum = df.groupby(['Risk_Level', 'Weekday'], as_index=False).agg(Slots=('Row_ID', 'count'))

out_dir = Path('powerbi_export')
out_dir.mkdir(exist_ok=True)

export_df = df.copy()
if 'Total_incidents' in export_df.columns and 'Total_Incidents' not in export_df.columns:
    export_df = export_df.rename(columns={'Total_incidents': 'Total_Incidents'})
fact_cols = [c for c in export_df.columns if c != 'Hour_code_sq']
export_df[fact_cols].to_csv(out_dir / 'traffic_clean.csv', index=False)
inc_long.to_csv(out_dir / 'incidents_long.csv', index=False)
impact.to_csv(out_dir / 'incident_impact.csv', index=False)
dim_time.to_csv(out_dir / 'dim_time.csv', index=False)
dim_weekday.to_csv(out_dir / 'dim_weekday.csv', index=False)
coef_df.to_csv(out_dir / 'model_coefficients.csv', index=False)
thresholds.to_csv(out_dir / 'thresholds.csv', index=False)
kpi.to_csv(out_dir / 'kpi_summary.csv', index=False)
weekday_sum.to_csv(out_dir / 'weekday_summary.csv', index=False)
period_sum.to_csv(out_dir / 'period_summary.csv', index=False)
hourly_sum.to_csv(out_dir / 'hourly_summary.csv', index=False)
peak_sum.to_csv(out_dir / 'peak_offpeak_summary.csv', index=False)
risk_sum.to_csv(out_dir / 'risk_by_weekday.csv', index=False)
fi_df.to_csv(out_dir / 'feature_importance.csv', index=False)

print('Exported', len(list(out_dir.glob('*.csv'))), 'CSV files to', out_dir.resolve())
for p in sorted(out_dir.glob('*.csv')):
    print(' ', p.name, p.stat().st_size, 'bytes')
"""))

extra.append(code(r"""
# ─── Zip + download (Colab) ──────────────────────────────────────────────────
import shutil
shutil.make_archive('powerbi_export', 'zip', 'powerbi_export')
print('Created powerbi_export.zip')
try:
    from google.colab import files
    files.download('powerbi_export.zip')
except Exception:
    print('Not in Colab — zip is in the working folder. Upload the CSVs into Power BI Desktop.')
"""))

extra.append(md("""
## 16. Extra Visualizations (interactive + model diagnostics)

### Why?
Section 6–13 used seaborn (publication-style static charts). This section adds:
1. **Actual vs Predicted scatter** — shows how well the Random Forest fits
2. **Residuals over time** — where the model is systematically wrong
3. **Plotly interactive line chart** — hover to inspect each weekday
4. **Risk-level donut / countplot** — dashboard-style KPI companion

### What is used?
`matplotlib` for diagnostics; `plotly.express` for interactive hover charts (works in Colab).

### How?
If plotly is missing, `pip install plotly` runs automatically. Residual = Actual − Predicted. Points far above the 45° line are under-predicted congestion events.
"""))

extra.append(code(r"""
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Actual vs predicted
axes[0].scatter(df['Predicted_Slowness'], df[TARGET], alpha=0.7, c=df['Hour_code'], cmap='coolwarm')
mn, mx = df[TARGET].min(), df[TARGET].max()
axes[0].plot([mn, mx], [mn, mx], 'k--', lw=1, label='Perfect prediction')
axes[0].set_xlabel('Predicted slowness %')
axes[0].set_ylabel('Actual slowness %')
axes[0].set_title('Actual vs Predicted (color = hour code)', fontweight='bold')
axes[0].legend()

# Residuals over time slots
axes[1].bar(df['Row_ID'], df['Residual'], color=np.where(df['Residual']>=0, '#d64550', '#2f9e5b'))
axes[1].axhline(0, color='black', lw=0.8)
axes[1].set_xlabel('Observation (1–135, Mon→Fri)')
axes[1].set_ylabel('Residual (actual − predicted)')
axes[1].set_title('Residuals across the week', fontweight='bold')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(7, 4))
order_r = ['Low', 'Medium', 'High']
counts = df['Risk_Level'].value_counts().reindex(order_r)
ax.bar(order_r, counts.values, color=['#2f9e5b', '#e9a23b', '#d64550'])
ax.set_title('Risk-level slot counts', fontweight='bold')
ax.set_ylabel('Number of 30-min slots')
for i, v in enumerate(counts.values):
    ax.text(i, v + 0.5, str(int(v)), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
"""))

extra.append(code(r"""
# Interactive Plotly chart (hover each day)
try:
    import plotly.express as px
except ImportError:
    import os
    os.system('pip -q install plotly')
    import plotly.express as px

fig = px.line(
    df, x='Time', y=TARGET, color='Weekday', markers=True,
    category_orders={'Weekday': weekdays, 'Time': list(hour_to_time.values())},
    title='Interactive: slowness by time of day (hover a point)',
    labels={TARGET: 'Slowness %'}
)
fig.update_layout(legend_title_text='Weekday', hovermode='x unified')
fig.show()

fig2 = px.scatter(
    df, x='Total_incidents', y=TARGET, color='Period', size='Incident_Types_Active',
    hover_data=['Weekday', 'Time'],
    title='Slowness vs total incidents (bubble size = distinct incident types)'
)
fig2.show()
"""))

extra.append(md("""
## 17. How to build the Power BI dashboard (after this notebook)

### Why Power BI in this project?
Colab proves the science. Power BI is the **operational dashboard**: filters by weekday / period / peak hour, KPI cards, heatmap, incident ranking, and a coefficient-based what-if view.

### Files to load (from `powerbi_export.zip`)
Import **all CSV files**. Then in Model view create:

| From | To | Cardinality |
|---|---|---|
| traffic_clean[Hour_code] | dim_time[Hour_code] | Many-to-one |
| traffic_clean[Weekday] | dim_weekday[Weekday] | Many-to-one |
| incidents_long[Row_ID] | traffic_clean[Row_ID] | Many-to-one |

### Four report pages (full dashboard)
1. **Executive Overview** — KPI cards, slowness trend, risk donut, weekday bars  
2. **Time Intelligence** — hourly line, weekday×hour matrix, peak vs off-peak  
3. **Incident Analysis** — frequency vs impact (do not confuse the two)  
4. **Predictive Insights** — coefficients, actual vs predicted, residuals, feature importance  

Paste the DAX from the Word report **Chapter 14** (or `PowerBI_DAX_Measures.txt`) into Power BI.

You can also open `Sao_Paulo_Traffic_FULL_DASHBOARD.html` in a browser for an immediate interactive view of the same pages.
"""))

src["cells"].extend(extra)
src["metadata"]["colab"] = {
    "name": "Smart_Urban_Transportation_EDA_COLAB.ipynb",
    "provenance": [],
    "toc_visible": True,
}
out = ROOT / "Smart_Urban_Transportation_EDA_COLAB.ipynb"
out.write_text(json.dumps(src, indent=2, ensure_ascii=False), encoding="utf-8")
print("Wrote", out, "cells=", len(src["cells"]))
