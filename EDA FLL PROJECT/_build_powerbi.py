"""Enhance Power BI star schema + self-contained full dashboard HTML."""
import json
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).parent
PBI = ROOT / "powerbi_data EDA DATA"
df = pd.read_csv(PBI / "traffic_clean.csv")
TARGET = "Slowness_percent"
INC = [
    "Immobilized_bus", "Broken_Truck", "Vehicle_excess", "Accident_victim",
    "Running_over", "Fire_vehicles", "Occurrence_involving_freight",
    "Incident_involving_dangerous_freight", "Lack_of_electricity", "Fire",
    "Point_of_flooding", "Manifestations", "Defect_in_the_network_of_trolleybuses",
    "Tree_on_the_road", "Semaphore_off", "Intermittent_Semaphore",
]
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

kpi = pd.DataFrame({
    "KPI": [
        "Avg Slowness %", "Median Slowness %", "Min Slowness %", "Max Slowness %",
        "Total Incident Events", "High Risk Slots", "Medium Risk Slots", "Low Risk Slots",
        "Outlier Slots", "Peak Hour Avg %", "Off Peak Avg %", "Observations",
    ],
    "Value": [
        round(df[TARGET].mean(), 2), round(df[TARGET].median(), 2),
        round(df[TARGET].min(), 2), round(df[TARGET].max(), 2),
        int(df["Total_Incidents"].sum()),
        int((df["Risk_Level"] == "High").sum()),
        int((df["Risk_Level"] == "Medium").sum()),
        int((df["Risk_Level"] == "Low").sum()),
        int(df["Is_Outlier"].sum()),
        round(df.loc[df["Is_Peak_Hour"] == 1, TARGET].mean(), 2),
        round(df.loc[df["Is_Peak_Hour"] == 0, TARGET].mean(), 2),
        len(df),
    ],
    "Page": ["Overview"] * 12,
})
weekday_sum = (
    df.groupby(["Weekday", "Weekday_Num"], as_index=False)
    .agg(
        Avg_Slowness=(TARGET, "mean"),
        Max_Slowness=(TARGET, "max"),
        Min_Slowness=(TARGET, "min"),
        Total_Incidents=("Total_Incidents", "sum"),
        High_Risk_Slots=("Risk_Level", lambda s: int((s == "High").sum())),
        Avg_Predicted=("Predicted_Slowness", "mean"),
    )
    .sort_values("Weekday_Num")
)
period_sum = (
    df.groupby(["Period", "Period_Order"], as_index=False)
    .agg(
        Avg_Slowness=(TARGET, "mean"),
        Total_Incidents=("Total_Incidents", "sum"),
        N=("Row_ID", "count"),
        High_Risk_Slots=("Risk_Level", lambda s: int((s == "High").sum())),
    )
    .sort_values("Period_Order")
)
hourly_sum = df.groupby(["Hour_code", "Time", "Period", "Period_Order", "Is_Peak_Hour"], as_index=False).agg(
    Avg_Slowness=(TARGET, "mean"),
    Std_Slowness=(TARGET, "std"),
    Avg_Incidents=("Total_Incidents", "mean"),
    Avg_Predicted=("Predicted_Slowness", "mean"),
)
peak_sum = df.groupby(["Weekday", "Weekday_Num", "Is_Peak_Hour"], as_index=False).agg(
    Avg_Slowness=(TARGET, "mean"), N=("Row_ID", "count")
)
risk_sum = df.groupby(["Risk_Level", "Weekday", "Weekday_Num"], as_index=False).agg(Slots=("Row_ID", "count"))

# Approximate RF importance ranking from |correlation| * uniqueness as a dashboard table
# Prefer a dedicated file if we can compute from residual variance — use abs corr with target as proxy
# plus Hour_code. Better: use sklearn if available.
try:
    from sklearn.ensemble import RandomForestRegressor
    X = df[["Hour_code"] + INC]
    y = df[TARGET]
    rf = RandomForestRegressor(n_estimators=300, random_state=42)
    rf.fit(X, y)
    fi_df = pd.DataFrame({"Feature": X.columns, "Importance": rf.feature_importances_})
    fi_df["Importance_Pct"] = (fi_df["Importance"] * 100).round(2)
    fi_df = fi_df.sort_values("Importance", ascending=False)
    fi_df["Rank"] = range(1, len(fi_df) + 1)
except Exception:
    corr = df[["Hour_code"] + INC].corrwith(df[TARGET]).abs().sort_values(ascending=False)
    fi_df = pd.DataFrame({"Feature": corr.index, "Importance": corr.values})
    fi_df["Importance_Pct"] = (fi_df["Importance"] / fi_df["Importance"].sum() * 100).round(2)
    fi_df["Rank"] = range(1, len(fi_df) + 1)

for name, tbl in [
    ("kpi_summary.csv", kpi),
    ("weekday_summary.csv", weekday_sum),
    ("period_summary.csv", period_sum),
    ("hourly_summary.csv", hourly_sum),
    ("peak_offpeak_summary.csv", peak_sum),
    ("risk_by_weekday.csv", risk_sum),
    ("feature_importance.csv", fi_df),
]:
    tbl.to_csv(PBI / name, index=False)
    print("wrote", name, len(tbl))

# Relationships file for Power BI documentation
rel = pd.DataFrame([
    ["traffic_clean", "Hour_code", "dim_time", "Hour_code", "Many-to-one", "Single"],
    ["traffic_clean", "Weekday", "dim_weekday", "Weekday", "Many-to-one", "Single"],
    ["incidents_long", "Row_ID", "traffic_clean", "Row_ID", "Many-to-one", "Single"],
    ["incidents_long", "Hour_code", "dim_time", "Hour_code", "Many-to-one", "Single"],
    ["hourly_summary", "Hour_code", "dim_time", "Hour_code", "Many-to-one", "Single"],
    ["weekday_summary", "Weekday", "dim_weekday", "Weekday", "One-to-one", "Both"],
])
rel.columns = ["FromTable", "FromColumn", "ToTable", "ToColumn", "Cardinality", "CrossFilter"]
rel.to_csv(PBI / "model_relationships.csv", index=False)

dax = r'''
-- ============================================================
-- São Paulo Traffic — Power BI DAX measures
-- Paste into a measure table named "Measures"
-- Fact table: traffic_clean
-- ============================================================

Avg Slowness =
AVERAGE ( traffic_clean[Slowness_percent] )

Median Slowness =
MEDIAN ( traffic_clean[Slowness_percent] )

Max Slowness =
MAX ( traffic_clean[Slowness_percent] )

Min Slowness =
MIN ( traffic_clean[Slowness_percent] )

Total Incident Events =
SUM ( traffic_clean[Total_Incidents] )

Observation Count =
COUNTROWS ( traffic_clean )

High Risk Slots =
CALCULATE ( COUNTROWS ( traffic_clean ), traffic_clean[Risk_Level] = "High" )

Medium Risk Slots =
CALCULATE ( COUNTROWS ( traffic_clean ), traffic_clean[Risk_Level] = "Medium" )

Low Risk Slots =
CALCULATE ( COUNTROWS ( traffic_clean ), traffic_clean[Risk_Level] = "Low" )

High Risk % =
DIVIDE ( [High Risk Slots], [Observation Count] )

Outlier Slots =
CALCULATE ( COUNTROWS ( traffic_clean ), traffic_clean[Is_Outlier] = 1 )

Peak Avg Slowness =
CALCULATE ( AVERAGE ( traffic_clean[Slowness_percent] ), traffic_clean[Is_Peak_Hour] = 1 )

OffPeak Avg Slowness =
CALCULATE ( AVERAGE ( traffic_clean[Slowness_percent] ), traffic_clean[Is_Peak_Hour] = 0 )

Peak Premium =
[Peak Avg Slowness] - [OffPeak Avg Slowness]

Peak Uplift % =
DIVIDE ( [Peak Premium], [OffPeak Avg Slowness] )

Slots With Any Incident =
CALCULATE ( COUNTROWS ( traffic_clean ), traffic_clean[Has_Incident] = 1 )

Incident Presence % =
DIVIDE ( [Slots With Any Incident], [Observation Count] )

Avg Predicted =
AVERAGE ( traffic_clean[Predicted_Slowness] )

Model MAE =
AVERAGEX ( traffic_clean, ABS ( traffic_clean[Residual] ) )

Model RMSE =
SQRT ( AVERAGEX ( traffic_clean, traffic_clean[Residual] ^ 2 ) )

Avg Residual =
AVERAGE ( traffic_clean[Residual] )

Evening Avg Slowness =
CALCULATE (
    AVERAGE ( traffic_clean[Slowness_percent] ),
    traffic_clean[Period] = "Evening peak (16:30-20:00)"
)

Midday Avg Slowness =
CALCULATE (
    AVERAGE ( traffic_clean[Slowness_percent] ),
    traffic_clean[Period] = "Midday (10:00-16:00)"
)

Evening vs Midday Gap =
[Evening Avg Slowness] - [Midday Avg Slowness]

-- Use on incidents_long
Incident Event Count =
SUM ( incidents_long[Incident_Count] )

Incident Slot Count =
CALCULATE ( COUNTROWS ( incidents_long ), incidents_long[Has_Incident] = 1 )
'''
(ROOT / "PowerBI_DAX_Measures.txt").write_text(dax.strip() + "\n", encoding="utf-8")

# Self-contained dashboard
records = df.replace({np.nan: None}).to_dict(orient="records")
coef = pd.read_csv(PBI / "model_coefficients.csv")
coef_rec = coef.replace({np.nan: None}).to_dict(orient="records")
impact = pd.read_csv(PBI / "incident_impact.csv")
imp_rec = impact.replace({np.nan: None}).to_dict(orient="records")
fi_rec = fi_df.replace({np.nan: None}).to_dict(orient="records")

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>São Paulo Traffic — Full Project Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{--bg:#eef2f6;--card:#fff;--ink:#13202c;--mute:#5d6b7a;--line:#d7dee6;--acc:#1f5f8b;--lo:#2f9e5b;--md:#e9a23b;--hi:#d64550}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 "IBM Plex Sans",system-ui,sans-serif}
header{background:#13202c;color:#fff;padding:22px 24px}
header h1{margin:0;font-size:22px} header p{margin:6px 0 0;opacity:.8}
nav{display:flex;gap:6px;flex-wrap:wrap;background:#1c2b3a;padding:8px 16px;position:sticky;top:0;z-index:5}
nav button{background:transparent;border:0;color:#c5d0da;padding:8px 14px;border-radius:6px;cursor:pointer;font:inherit}
nav button.on{background:var(--acc);color:#fff;font-weight:600}
main{max-width:1280px;margin:0 auto;padding:18px 20px 48px}
.bar{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
select{font:inherit;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:#fff}
.kpis{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin-bottom:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.kpi b{display:block;font-size:26px;font-weight:700} .kpi span{color:var(--mute);font-size:12px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.cv{position:relative;height:280px}
h2{font-size:18px;margin:4px 0 12px} h3{margin:0 0 8px;font-size:14px}
table{border-collapse:collapse;font-size:12px;width:100%}
th,td{padding:5px 7px;border:1px solid #eef2f6;text-align:center} th{background:#f7f9fb;color:var(--mute)}
td.l,th.l{text-align:left}
.note{color:var(--mute);font-size:13px;margin-top:8px}
.sec{display:none}.sec.on{display:block}
.sl{display:grid;grid-template-columns:minmax(140px,1.3fr) 1fr 40px;gap:8px;align-items:center;margin:8px 0}
.big{font-size:42px;font-weight:700}
.pill{display:inline-block;padding:3px 12px;border-radius:99px;color:#fff;font-weight:600}
.meter{height:14px;border-radius:7px;background:linear-gradient(90deg,var(--lo),var(--md),var(--hi));position:relative;margin:12px 0}
.meter i{position:absolute;top:-5px;width:4px;height:24px;background:var(--ink);border-radius:2px}
footer{max-width:1280px;margin:0 auto;padding:0 20px 40px;color:var(--mute);font-size:13px}
</style>
</head>
<body>
<header>
  <h1>São Paulo urban traffic dashboard</h1>
  <p>Full project view · 14–18 Dec 2009 · 135 half-hour slots · UCI dataset 483 · Parallel to Colab + Word report</p>
</header>
<nav id="tabs"></nav>
<main>
  <div class="bar">
    <label>Weekday <select id="dayF"></select></label>
    <label>Period <select id="perF"></select></label>
    <label>Peak only <select id="pkF"><option value="all">All slots</option><option value="1">Peak hours</option><option value="0">Off-peak</option></select></label>
  </div>
  <div id="s0" class="sec on"></div>
  <div id="s1" class="sec"></div>
  <div id="s2" class="sec"></div>
  <div id="s3" class="sec"></div>
  <div id="s4" class="sec"></div>
</main>
<footer>
  Pages match the Power BI build: Executive Overview, Time Intelligence, Incident Analysis, Predictive Insights, Data model.
  Filters apply to KPI cards and charts. Data is embedded from traffic_clean.csv — no upload required.
  Student: Hemavathy K · KCT · EDA 2026.
</footer>
<script>
const DATA = __DATA__;
const COEF = __COEF__;
const IMPACT = __IMPACT__;
const FI = __FI__;
const DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday"];
const TABS=["1. Executive Overview","2. Time Intelligence","3. Incident Analysis","4. Predictive Insights","5. Data model"];
const $ = id => document.getElementById(id);
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const avg = a => a.length ? a.reduce((x,y)=>x+y,0)/a.length : NaN;
const f1 = x => isNaN(x) ? "–" : Number(x).toFixed(1);
const f2 = x => isNaN(x) ? "–" : Number(x).toFixed(2);
let charts = {};
function mk(id,cfg){if(charts[id])charts[id].destroy();Chart.defaults.color=css("--mute");Chart.defaults.borderColor=css("--line");
  cfg.options=Object.assign({responsive:true,maintainAspectRatio:false},cfg.options);charts[id]=new Chart($(id),cfg)}

$("dayF").innerHTML='<option>All</option>'+DAYS.map(d=>`<option>${d}</option>`).join("");
const P=[...new Set(DATA.map(r=>r.Period))];
$("perF").innerHTML='<option>All</option>'+P.map(d=>`<option>${d}</option>`).join("");
$("tabs").innerHTML=TABS.map((t,i)=>`<button class="${i?"":"on"}" onclick="tab(${i})">${t}</button>`).join("");
["dayF","perF","pkF"].forEach(id=>$(id).onchange=render);
function tab(i){document.querySelectorAll("nav button").forEach((b,j)=>b.classList.toggle("on",i==j));
  document.querySelectorAll(".sec").forEach((s,j)=>s.classList.toggle("on",i==j))}
function filtered(){
  const d=$("dayF").value,p=$("perF").value,k=$("pkF").value;
  return DATA.filter(r=>(d=="All"||r.Weekday==d)&&(p=="All"||r.Period==p)&&(k=="all"||String(r.Is_Peak_Hour)==k));
}
function render(){
  const R=filtered(), S=R.map(r=>r.Slowness_percent);
  const times=[...new Map(DATA.map(r=>[r.Hour_code,r.Time])).entries()].sort((a,b)=>a[0]-b[0]).map(x=>x[1]);
  const pal=["#1f5f8b","#e9a23b","#2f9e5b","#d64550","#7a5cc2"];
  const hi=R.filter(r=>r.Risk_Level==="High").length;
  const totInc=R.reduce((a,r)=>a+(r.Total_Incidents||0),0);
  const pk=avg(R.filter(r=>r.Is_Peak_Hour==1).map(r=>r.Slowness_percent));
  const op=avg(R.filter(r=>r.Is_Peak_Hour==0).map(r=>r.Slowness_percent));

  $("s0").innerHTML=`<h2>Executive overview</h2>
  <div class="kpis">
    <div class="card kpi"><b>${f1(avg(S))}%</b><span>Average slowness</span></div>
    <div class="card kpi"><b>${f1(Math.max(...S))}%</b><span>Peak slowness</span></div>
    <div class="card kpi"><b>${totInc}</b><span>Total incident events</span></div>
    <div class="card kpi"><b>${hi}</b><span>High-risk slots</span></div>
    <div class="card kpi"><b>${f1(pk)}%</b><span>Peak-hour average</span></div>
    <div class="card kpi"><b>${f1(op)}%</b><span>Off-peak average</span></div>
  </div>
  <div class="grid">
    <div class="card"><h3>Slowness through the day by weekday</h3><div class="cv"><canvas id="c1"></canvas></div></div>
    <div class="card"><h3>Average slowness by period</h3><div class="cv"><canvas id="c2"></canvas></div></div>
    <div class="card"><h3>Risk-level mix</h3><div class="cv"><canvas id="c2b"></canvas></div></div>
    <div class="card"><h3>Weekday comparison</h3><div class="cv"><canvas id="c2c"></canvas></div></div>
  </div>
  <p class="note">Same KPIs as Power BI Page 1. Evening congestion dominates the average. Use the weekday filter to isolate Friday.</p>`;

  const ds=( $("dayF").value=="All"?DAYS:[$("dayF").value]).map((w,i)=>({
    label:w,borderColor:pal[DAYS.indexOf(w)],backgroundColor:pal[DAYS.indexOf(w)],tension:.3,pointRadius:2,
    data:times.map(t=>avg(R.filter(r=>r.Weekday==w&&r.Time==t).map(r=>r.Slowness_percent)))
  }));
  mk("c1",{type:"line",data:{labels:times,datasets:ds},options:{scales:{y:{title:{display:true,text:"Slowness %"}}}}});
  mk("c2",{type:"bar",data:{labels:P,datasets:[{data:P.map(x=>avg(S.length?R.filter(r=>r.Period==x).map(r=>r.Slowness_percent):[])),backgroundColor:["#e9a23b","#1f5f8b","#d64550"]}]},options:{plugins:{legend:{display:false}}}});
  const rl=["Low","Medium","High"];
  mk("c2b",{type:"doughnut",data:{labels:rl,datasets:[{data:rl.map(x=>R.filter(r=>r.Risk_Level==x).length),backgroundColor:["#2f9e5b","#e9a23b","#d64550"]}]}});
  mk("c2c",{type:"bar",data:{labels:DAYS,datasets:[{label:"Avg slowness",data:DAYS.map(w=>avg(R.filter(r=>r.Weekday==w).map(r=>r.Slowness_percent))),backgroundColor:"#1f5f8b"}]},options:{plugins:{legend:{display:false}}}});

  const all=DATA.map(r=>r.Slowness_percent),mn=Math.min(...all),mx=Math.max(...all);
  const rate=v=>v>=10.9?"High":v>7.9?"Medium":"Low";
  const col=v=>({Low:"#2f9e5b",Medium:"#e9a23b",High:"#d64550"})[rate(v)];
  const heat=v=>isNaN(v)?"":`color-mix(in srgb, ${col(v)} ${Math.round(25+60*(v-mn)/(mx-mn||1))}%, transparent)`;
  $("s1").innerHTML=`<h2>Time intelligence</h2>
  <div class="kpis">
    <div class="card kpi"><b>${f1(pk)}%</b><span>Peak-hour average</span></div>
    <div class="card kpi"><b>${f1(op)}%</b><span>Off-peak average</span></div>
    <div class="card kpi"><b>${isNaN(pk-op)?"–":f1(pk-op)}</b><span>Peak premium (pp)</span></div>
    <div class="card kpi"><b>${isNaN(pk/op)?"–":Math.round((pk/op-1)*100)+"%"}</b><span>Peak uplift</span></div>
  </div>
  <div class="card"><h3>Heatmap — weekday × time (average slowness %)</h3>
  <div style="overflow:auto"><table><tr><th class="l"></th>${times.map(t=>`<th>${t}</th>`).join("")}</tr>
  ${DAYS.map(w=>`<tr><th class="l">${w.slice(0,3)}</th>${times.map(t=>{const v=avg(DATA.filter(r=>r.Weekday==w&&r.Time==t).map(r=>r.Slowness_percent));return`<td style="background:${heat(v)}">${f1(v)}</td>`}).join("")}</tr>`).join("")}
  </table></div>
  <p class="note">Green = low risk (≤7.9%), amber = medium, red = high (≥10.9%). Darker red = slower. Friday evening is the worst band.</p></div>
  <div class="grid" style="margin-top:14px">
    <div class="card"><h3>Peak vs off-peak by weekday</h3><div class="cv"><canvas id="c5"></canvas></div></div>
    <div class="card"><h3>Rolling 90-min slowness (all days)</h3><div class="cv"><canvas id="c6"></canvas></div></div>
  </div>`;
  mk("c5",{type:"bar",data:{labels:DAYS,datasets:[
    {label:"Off-peak",data:DAYS.map(w=>avg(DATA.filter(r=>r.Weekday==w&&r.Is_Peak_Hour==0).map(r=>r.Slowness_percent))),backgroundColor:"#1f5f8b"},
    {label:"Peak",data:DAYS.map(w=>avg(DATA.filter(r=>r.Weekday==w&&r.Is_Peak_Hour==1).map(r=>r.Slowness_percent))),backgroundColor:"#d64550"}
  ]}});
  mk("c6",{type:"line",data:{labels:DATA.map(r=>r.Weekday.slice(0,3)+" "+r.Time),datasets:[{label:"Rolling3",data:DATA.map(r=>r.Slowness_Rolling3),borderColor:"#1f5f8b",pointRadius:0,tension:.2}]},options:{plugins:{legend:{display:false}}}});

  const top=[...R].sort((a,b)=>b.Slowness_percent-a.Slowness_percent).slice(0,10);
  $("s2").innerHTML=`<h2>Incident analysis</h2>
  <div class="grid">
    <div class="card"><h3>Extra slowness when incident is present (impact points)</h3><div class="cv" style="height:360px"><canvas id="c3"></canvas></div></div>
    <div class="card"><h3>Total events (frequency ≠ impact)</h3><div class="cv" style="height:360px"><canvas id="c4"></canvas></div></div>
  </div>
  <div class="card" style="margin-top:14px"><h3>Ten most congested slots in the current filter</h3>
  <table><tr><th class="l">Day</th><th>Time</th><th>Slowness %</th><th>Incidents</th><th>Risk</th><th>Outlier</th></tr>
  ${top.map(r=>`<tr><td class="l">${r.Weekday}</td><td>${r.Time}</td><td>${r.Slowness_percent}</td><td>${r.Total_Incidents}</td><td>${r.Risk_Level}</td><td>${r.Is_Outlier?"Yes":""}</td></tr>`).join("")}
  </table>
  <p class="note">Flooding has few events but the largest impact. Trolleybus defects are frequent but not the main congestion driver. Correlation is not causation.</p></div>`;
  const imp = IMPACT.slice().sort((a,b)=>b.Impact_Points-a.Impact_Points);
  mk("c3",{type:"bar",data:{labels:imp.map(x=>x.Incident),datasets:[{data:imp.map(x=>x.Impact_Points),backgroundColor:imp.map(x=>x.Impact_Points>=0?"#d64550":"#2f9e5b")}]},options:{indexAxis:"y",plugins:{legend:{display:false}}}});
  mk("c4",{type:"bar",data:{labels:imp.map(x=>x.Incident),datasets:[{data:imp.map(x=>x.Total_Events),backgroundColor:"#1f5f8b"}]},options:{indexAxis:"y",plugins:{legend:{display:false}}}});

  const mae = avg(R.map(r=>Math.abs(r.Residual||0)));
  const rmse = Math.sqrt(avg(R.map(r=>(r.Residual||0)**2)));
  $("s3").innerHTML=`<h2>Predictive insights</h2>
  <div class="kpis">
    <div class="card kpi"><b>${f2(mae)}</b><span>MAE (filtered)</span></div>
    <div class="card kpi"><b>${f2(rmse)}</b><span>RMSE (filtered)</span></div>
    <div class="card kpi"><b>${FI[0]?FI[0].Feature.replaceAll("_"," "):"–"}</b><span>Top RF feature</span></div>
  </div>
  <div class="grid">
    <div class="card"><h3>Linear coefficients (what-if model)</h3><div class="cv"><canvas id="c7"></canvas></div></div>
    <div class="card"><h3>Random Forest feature importance</h3><div class="cv"><canvas id="c8"></canvas></div></div>
    <div class="card"><h3>Actual vs predicted</h3><div class="cv"><canvas id="c9"></canvas></div></div>
    <div class="card" id="simCard"></div>
  </div>
  <p class="note">Random Forest is the accuracy model (Colab Chapter 13). The linear model is only for the sliders — same as model_coefficients.csv in Power BI Page 4.</p>`;
  const cf=COEF.filter(r=>r.Feature!=="Intercept");
  mk("c7",{type:"bar",data:{labels:cf.map(r=>r.Feature.replaceAll("_"," ")),datasets:[{data:cf.map(r=>r.Coefficient),backgroundColor:cf.map(r=>r.Coefficient>=0?"#d64550":"#2f9e5b")}]},options:{indexAxis:"y",plugins:{legend:{display:false}}}});
  mk("c8",{type:"bar",data:{labels:FI.map(r=>r.Feature.replaceAll("_"," ")),datasets:[{data:FI.map(r=>r.Importance_Pct),backgroundColor:"#1f5f8b"}]},options:{indexAxis:"y",plugins:{legend:{display:false}}}});
  mk("c9",{type:"scatter",data:{datasets:[{label:"Slots",data:R.map(r=>({x:r.Predicted_Slowness,y:r.Slowness_percent})),backgroundColor:"#1f5f8b"}]},options:{scales:{x:{title:{display:true,text:"Predicted"}},y:{title:{display:true,text:"Actual"}}}}});
  sim();

  $("s4").innerHTML=`<h2>Power BI data model (star schema)</h2>
  <div class="card">
    <p>Load every CSV in <code>powerbi_data EDA DATA</code> (or the Colab <code>powerbi_export.zip</code>).</p>
    <table>
      <tr><th class="l">Table</th><th>Role</th><th>Use on page</th></tr>
      <tr><td class="l">traffic_clean</td><td>Fact (135 rows)</td><td>All pages</td></tr>
      <tr><td class="l">dim_time / dim_weekday</td><td>Dimensions</td><td>Slicers, heatmap</td></tr>
      <tr><td class="l">incidents_long</td><td>Incident fact (melted)</td><td>Page 3 filters by type</td></tr>
      <tr><td class="l">incident_impact</td><td>Impact ranking</td><td>Page 3</td></tr>
      <tr><td class="l">kpi_summary, weekday/period/hourly summaries</td><td>Pre-aggregates</td><td>Faster cards if DirectQuery not used</td></tr>
      <tr><td class="l">model_coefficients, feature_importance</td><td>Model outputs</td><td>Page 4</td></tr>
      <tr><td class="l">thresholds</td><td>Risk cut-offs 7.9 / 10.9</td><td>Conditional formatting</td></tr>
    </table>
    <p class="note">Relationships: traffic_clean[Hour_code] → dim_time; traffic_clean[Weekday] → dim_weekday; incidents_long[Row_ID] → traffic_clean[Row_ID]. DAX is in PowerBI_DAX_Measures.txt and Word Chapter 14.</p>
  </div>`;
}

let SV={Hour_code:12};
function sim(){
  if(!COEF||!COEF.length){return}
  const cf=Object.fromEntries(COEF.map(r=>[r.Feature,r]));
  const feats=COEF.map(r=>r.Feature).filter(x=>!["Intercept","Hour_code","Hour_code_sq"].includes(x));
  const pred=()=>{let v=cf.Intercept.Coefficient+cf.Hour_code.Coefficient*SV.Hour_code+cf.Hour_code_sq.Coefficient*SV.Hour_code**2;
    feats.forEach(f=>v+=cf[f].Coefficient*(SV[f]||0));return Math.max(0,Math.min(100,v))};
  const time=m=>{const t=420+(m-1)*30;return String(Math.floor(t/60)).padStart(2,"0")+":"+String(t%60).padStart(2,"0")};
  $("simCard").innerHTML=`<h3>What-if congestion simulator</h3>
  <div class="sl"><span>Time slot</span><input type="range" min="1" max="27" value="${SV.Hour_code}" data-f="Hour_code"><b id="v_h">${time(SV.Hour_code)}</b></div>
  ${feats.map(f=>`<div class="sl"><span>${f.replaceAll("_"," ")}</span><input type="range" min="0" max="${Math.max((cf[f].Max_Value||0)+2,5)}" value="${SV[f]||0}" data-f="${f}"><b id="v_${f}">${SV[f]||0}</b></div>`).join("")}
  <div class="big" id="pv"></div><p><span class="pill" id="pr"></span></p>
  <div class="meter"><i id="pm"></i></div>`;
  const upd=()=>{const v=pred(),r=v>=10.9?"High":v>7.9?"Medium":"Low";
    $("pv").textContent=f1(v)+"%";$("pr").textContent=r+" risk";
    $("pr").style.background={Low:"#2f9e5b",Medium:"#e9a23b",High:"#d64550"}[r];
    $("pm").style.left=Math.min(100,v/30*100)+"%";};
  $("simCard").querySelectorAll("input").forEach(i=>i.oninput=()=>{SV[i.dataset.f]=+i.value;
    $(i.dataset.f=="Hour_code"?"v_h":"v_"+i.dataset.f).textContent=i.dataset.f=="Hour_code"?time(+i.value):i.value;upd()});
  upd();
}
render();
</script>
</body>
</html>
'''
html = (
    html.replace("__DATA__", json.dumps(records))
    .replace("__COEF__", json.dumps(coef_rec))
    .replace("__IMPACT__", json.dumps(imp_rec))
    .replace("__FI__", json.dumps(fi_rec))
)
out_html = ROOT / "Sao_Paulo_Traffic_FULL_DASHBOARD.html"
out_html.write_text(html, encoding="utf-8")
print("wrote", out_html, "bytes", out_html.stat().st_size)
