"""Full project report (.docx) parallel to the Colab notebook."""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).parent
doc = Document()

# Page setup
for s in doc.sections:
    s.top_margin = Cm(2.0)
    s.bottom_margin = Cm(2.0)
    s.left_margin = Cm(2.2)
    s.right_margin = Cm(2.2)

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
style.paragraph_format.space_after = Pt(8)
style.paragraph_format.line_spacing = 1.15

for i in range(1, 4):
    hs = doc.styles[f"Heading {i}"]
    hs.font.color.rgb = RGBColor(0x13, 0x20, 0x2C)
    hs.font.name = "Calibri"


def shade(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_run_font(run, size=11, bold=False, color=None):
    run.font.size = Pt(size)
    run.bold = bold
    run.font.name = "Calibri"
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_caption(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x5D, 0x6B, 0x7A)


def add_para(text, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(11)
    return p


def add_bullet(text):
    p = doc.add_paragraph(text, style="List Bullet")
    return p


def add_code(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.4)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    r.font.name = "Consolas"
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x4D)
    return p


def table(headers, rows, col_w=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = ""
        r = cell.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)
        shade(cell, "13202C")
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = t.rows[ri + 1].cells[ci]
            cell.text = ""
            r = cell.paragraphs[0].add_run(str(val))
            r.font.size = Pt(9)
            if ri % 2 == 1:
                shade(cell, "F4F7FA")
    doc.add_paragraph()
    return t


# ── Cover ────────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("KUMARAGURU COLLEGE OF TECHNOLOGY")
set_run_font(r, 14, True, (0x13, 0x20, 0x2C))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Department of Computer Science / EDA")
set_run_font(r, 12, False, (0x5D, 0x6B, 0x7A))

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("PROJECT REPORT")
set_run_font(r, 16, True)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Smart Urban Transportation Systems")
set_run_font(r, 22, True, (0x1F, 0x5F, 0x8B))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Exploratory Data Analysis of Urban Traffic in São Paulo, Brazil")
set_run_font(r, 13)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("(UCI Machine Learning Repository — Dataset ID 483)")
set_run_font(r, 11, False, (0x5D, 0x6B, 0x7A))

doc.add_paragraph()
table(
    ["Field", "Details"],
    [
        ["Student name", "Hemavathy K"],
        ["Institution", "Kumaraguru College of Technology (KCT)"],
        ["Subject", "Exploratory Data Analysis (EDA)"],
        ["Dataset", "Behavior of the Urban Traffic of the City of São Paulo, Brazil"],
        ["DOI / License", "10.24432/C5902F  ·  CC BY 4.0"],
        ["Date", "October 2026"],
        ["Colab notebook", "Smart_Urban_Transportation_EDA_COLAB.ipynb"],
        ["Power BI data", "powerbi_data EDA DATA\\  (star schema CSVs)"],
        ["Interactive dashboard", "Sao_Paulo_Traffic_FULL_DASHBOARD.html"],
        ["DAX measures", "PowerBI_DAX_Measures.txt"],
        ["Tool stack", "Python (Google Colab) · pandas · seaborn · scikit-learn · Power BI"],
    ],
)

add_para(
    "This Word document is the parallel written report for the Google Colab notebook. "
    "Every numbered chapter here matches the same numbered section in the notebook. "
    "When you run a Colab cell, read the same-number chapter here to understand WHY the step exists, "
    "WHAT library or method is used, and HOW it is applied to this dataset."
)

doc.add_heading("How to read this report together with Colab", level=1)
add_para(
    "Open Smart_Urban_Transportation_EDA_COLAB.ipynb in Google Colab (File → Upload notebook). "
    "Use Runtime → Run all. Then keep this document beside the notebook."
)
table(
    ["Colab section (run this)", "This Word chapter (read this)", "What you should see"],
    [
        ["1. Project Overview", "Chapter 1", "Problem, RQs, variable dictionary"],
        ["2. Setup & Data Loading", "Chapter 2", "Libraries import + dataset 135×18"],
        ["3. Initial Examination", "Chapter 3", "shape, dtypes, head/tail, info()"],
        ["4. Cleaning & features", "Chapter 4", "0 missing, 0 duplicates, new columns"],
        ["5. Descriptive Statistics", "Chapter 5", "mean ~10%, skew, incident totals"],
        ["6. Univariate Analysis", "Chapter 6", "histogram, boxplot, frequency bars"],
        ["7. Time-Based Analysis", "Chapter 7", "U-shape day curve, heatmap"],
        ["8. Incident Frequency", "Chapter 8", "frequency ranking + dual-axis chart"],
        ["9. Relationship Analysis", "Chapter 9", "scatter + Mann-Whitney table"],
        ["10. Correlation Analysis", "Chapter 10", "heatmap + Pearson vs Spearman"],
        ["11. Outlier Analysis", "Chapter 11", "IQR fences, flagged extremes"],
        ["12. Top / Bottom slots", "Chapter 12", "worst and smoothest 10 rows"],
        ["13. Predictive Baseline", "Chapter 13", "Ridge vs Random Forest CV"],
        ["14. Key Insights (code)", "Chapter 15", "answers to all 6 RQs"],
        ["15. Power BI Export", "Chapter 14", "CSV star schema + zip download"],
        ["16. Extra visualizations", "Ch. 6–13 extended", "Plotly + residual plots"],
        ["17. Power BI how-to", "Chapter 14", "4-page dashboard build"],
    ],
)

# ── TOC ──────────────────────────────────────────────────────────────────
doc.add_heading("Table of contents", level=1)
for line in [
    "Executive summary",
    "Chapter 1 — Introduction (Colab §1)",
    "Chapter 2 — Setup and environment (Colab §2)",
    "Chapter 3 — Initial dataset examination (Colab §3)",
    "Chapter 4 — Data cleaning and feature engineering (Colab §4)",
    "Chapter 5 — Descriptive statistics (Colab §5)",
    "Chapter 6 — Univariate analysis (Colab §6)",
    "Chapter 7 — Time-based analysis (Colab §7)",
    "Chapter 8 — Incident frequency analysis (Colab §8)",
    "Chapter 9 — Relationship analysis (Colab §9)",
    "Chapter 10 — Correlation analysis (Colab §10)",
    "Chapter 11 — Outlier analysis (Colab §11)",
    "Chapter 12 — Top and bottom observations (Colab §12)",
    "Chapter 13 — Predictive baseline (Colab §13)",
    "Chapter 14 — Power BI full dashboard (Colab §15–17)",
    "Chapter 15 — Key insights, recommendations, limitations (Colab §14)",
    "References",
    "Appendix A — Feature dictionary",
    "Appendix B — Power BI relationships and page map",
    "Appendix C — Linear model coefficients",
]:
    add_bullet(line)

# ── Exec ─────────────────────────────────────────────────────────────────
doc.add_heading("Executive summary", level=1)
add_para(
    "This project is a complete Exploratory Data Analysis (EDA) of the UCI dataset "
    "“Behavior of the Urban Traffic of the City of São Paulo in Brazil” (ID 483). "
    "The file records 135 observations: every 30 minutes from 07:00 to 20:00 across five weekdays "
    "(14–18 December 2009). Each row stores a time-slot code, 16 incident counts, and the target "
    "Slowness in traffic (%)."
)
add_para("Key findings (computed in Colab; visualized in Power BI):", bold=True)
add_bullet("Peak congestion is the evening rush (about 16:30–20:00), with average slowness around 13–16%. Morning rush is secondary (~9–11%). Midday is the easiest period (~8%).")
add_bullet("Point of flooding is the most impactful incident: about +10.4 percentage points of slowness when present (p ≈ 0.0001).")
add_bullet("Lack of electricity adds about +5.86 points; semaphore off adds about +4.39 points. Signal and power failures matter more than raw vehicle breakdowns.")
add_bullet("Broken trucks and immobilized buses are frequent but only moderately associated with slowness. Frequency is not the same as impact.")
add_bullet("The dataset has zero missing values and zero duplicate rows, so no imputation was required.")
add_bullet("A Random Forest using hour code + incident counts explains about 70% of slowness variance (5-fold CV). Time of day is the strongest feature.")
add_bullet("The Power BI (and HTML) dashboard has five views: Executive Overview, Time Intelligence, Incident Analysis, Predictive Insights, and Data model.")

add_para("Project deliverables:", bold=True)
add_bullet("Google Colab notebook — numbered sections 1–17 with code plus Why / What / How markdown above each cell.")
add_bullet("This Word report — the same numbers, written for evaluation as a full project report.")
add_bullet("Power BI star-schema CSVs (original tables plus KPI, weekday, period, hourly, peak, risk, feature-importance, relationships).")
add_bullet("PowerBI_DAX_Measures.txt — paste-ready measures for Desktop.")
add_bullet("Sao_Paulo_Traffic_FULL_DASHBOARD.html — browser dashboard with the same pages (data embedded).")

# ── Ch1 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 1 — Introduction (Colab section 1)", level=1)
doc.add_heading("1.1 Why this chapter exists", level=2)
add_para(
    "EDA without a problem statement becomes a pile of charts. This chapter states who the work is for, "
    "what questions we will answer, and what each column means. The matching Colab cell is markdown only — no code yet."
)
doc.add_heading("1.2 Background", level=2)
add_para(
    "São Paulo’s metropolitan region has more than 21 million people and is routinely among the world’s most congested cities. "
    "Commuters lose large amounts of time to delay. Knowing WHEN slowness peaks and WHICH incidents worsen it supports:"
)
add_bullet("Traffic authorities — crew timing for signals and incident response.")
add_bullet("Public transport operators — schedule buffers around peaks and floods.")
add_bullet("Emergency services — routing when flooding or signal failure is present.")
add_bullet("Urban planners — drainage and power-backup investment.")
add_bullet("Students of EDA — a small, clean, real-world table that still needs careful interpretation.")

doc.add_heading("1.3 Problem statement — six research questions", level=2)
add_para("RQ1. At what times of day is slowness highest, and does the pattern differ by weekday?")
add_para("RQ2. Which incident types occur most frequently?")
add_para("RQ3. Which incidents are most strongly associated with higher slowness?")
add_para("RQ4. Are present-vs-absent differences statistically significant?")
add_para("RQ5. Are there outliers, and what do the extreme slots look like?")
add_para("RQ6. Can time + incident counts explain a useful share of slowness variance?")

doc.add_heading("1.4 Dataset facts", level=2)
table(
    ["Property", "Value"],
    [
        ["Source", "UCI Machine Learning Repository"],
        ["ID / DOI", "483 / 10.24432/C5902F"],
        ["Donor", "Edilson Anselmo Correa da Silva"],
        ["Rows × columns", "135 × 18 (raw)"],
        ["Calendar", "Mon 14 Dec 2009 – Fri 18 Dec 2009"],
        ["Resolution", "30 minutes, 07:00–20:00 (27 slots/day × 5 days)"],
        ["File format", "CSV; semicolon delimiter; comma decimal (European)"],
        ["Geography", "São Paulo, Brazil (city-level aggregate, not geo-tagged)"],
    ],
)

doc.add_heading("1.5 Variable dictionary (what each column is)", level=2)
add_para(
    "Hour (Coded) is not a clock hour. Code 1 = 07:00, code 2 = 07:30, … code 27 = 20:00. "
    "The 27-slot cycle repeats each weekday. Incident columns are event COUNTS in that half-hour, not yes/no flags "
    "(except that many rarely exceed 1). The target is a percentage of slowness versus free flow."
)
table(
    ["#", "Original name", "Renamed in code", "Role"],
    [
        ["1", "Hour (Coded)", "Hour_code", "Time slot 1–27"],
        ["2", "Immobilized bus", "Immobilized_bus", "Incident count"],
        ["3", "Broken Truck", "Broken_Truck", "Incident count"],
        ["4", "Vehicle excess", "Vehicle_excess", "Incident count"],
        ["5", "Accident victim", "Accident_victim", "Incident count"],
        ["6", "Running over", "Running_over", "Incident count"],
        ["7", "Fire vehicles", "Fire_vehicles", "Incident count"],
        ["8", "Occurrence involving freight", "Occurrence_involving_freight", "Incident count"],
        ["9", "Incident involving dangerous freight", "Incident_involving_dangerous_freight", "Incident count"],
        ["10", "Lack of electricity", "Lack_of_electricity", "Incident count"],
        ["11", "Fire", "Fire", "Incident count"],
        ["12", "Point of flooding", "Point_of_flooding", "Incident count"],
        ["13", "Manifestations", "Manifestations", "Incident count"],
        ["14", "Defect in the network of trolleybuses", "Defect_in_the_network_of_trolleybuses", "Incident count"],
        ["15", "Tree on the road", "Tree_on_the_road", "Incident count"],
        ["16", "Semaphore off", "Semaphore_off", "Incident count (signals off)"],
        ["17", "Intermittent Semaphore", "Intermittent_Semaphore", "Incident count"],
        ["18", "Slowness in traffic (%)", "Slowness_percent", "TARGET"],
    ],
)

# ── Ch2 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 2 — Setup and environment (Colab section 2)", level=1)
doc.add_heading("2.1 Why", level=2)
add_para(
    "Nothing else runs until libraries are imported and the CSV is in a DataFrame. "
    "Colab VMs are empty each session, so the loader must download the file, not assume it is already on disk."
)
doc.add_heading("2.2 What is used — libraries", level=2)
table(
    ["Library", "Why it is used in THIS project"],
    [
        ["pandas", "read_csv, rename, groupby, pivot_table, melt, describe, export CSV"],
        ["numpy", "arrays, NaN handling, sqrt for RMSE, masks for heatmaps"],
        ["matplotlib.pyplot", "figure layout, line/bar/fill_between, dual axis (twinx)"],
        ["seaborn", "histplot, boxplot, heatmap, regplot with less boilerplate"],
        ["scipy.stats", "mannwhitneyu for present vs absent tests"],
        ["sklearn", "Ridge, RandomForestRegressor, KFold, cross_val_score, StandardScaler"],
        ["plotly.express", "Section 16 interactive hover charts in Colab"],
        ["urllib, zipfile, io", "download and unzip the UCI archive"],
    ],
)
doc.add_heading("2.3 How — configuration lines", level=2)
add_code(
    "warnings.filterwarnings('ignore')   # keep Colab output readable\n"
    "sns.set_theme(style='whitegrid')    # consistent chart background\n"
    "plt.rcParams['figure.dpi'] = 110     # sharp enough for screenshots\n"
    "pd.set_option('display.max_columns', 30)"
)
add_para(
    "The UCI file is not a normal comma CSV. Brazil/Europe often use ';' between fields and ',' inside numbers "
    "(so 4,1 means 4.1). That is why the reader is:"
)
add_code("pd.read_csv(path, sep=';', decimal=',')")
doc.add_heading("2.4 How — four-step loader", level=2)
add_para("Step 1: If a local CSV whose name contains “sao paulo” exists, read it (offline / re-run).")
add_para("Step 2: Download the official UCI zip and read the CSV inside.")
add_para("Step 3: pip install ucimlrepo and fetch_ucirepo(id=483).")
add_para("Step 4: Google Colab file upload widget.")
add_para(
    "This order is deliberate: local file is fastest; UCI zip does not need an extra package; "
    "ucimlrepo is a backup API; upload is last so the notebook still works in an exam lab with no network to UCI."
)

# ── Ch3 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 3 — Initial dataset examination (Colab section 3)", level=1)
doc.add_heading("3.1 Why we look at raw data first", level=2)
add_para(
    "Cleaning before looking is a common mistake. We need to confirm row count, types, and that head/tail look like a time series, "
    "not a shuffled table."
)
doc.add_heading("3.2 What / How", level=2)
table(
    ["Call", "Why"],
    [
        ["df.shape", "Must be 135 rows × 18 columns"],
        ["df.dtypes", "All numeric after decimal=',' ; no leftover object percents"],
        ["df.head()", "Monday morning, hour codes 1–5, slowness climbing"],
        ["df.tail()", "Friday evening, hour codes 23–27, high slowness"],
        ["df.info()", "non-null counts (should be 135 everywhere)"],
    ],
)
add_para(
    "The table is small. That is a feature and a warning: every row matters (do not drop casually), "
    "and correlations can look dramatic by chance. Later tests use non-parametric methods for that reason."
)

# ── Ch4 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 4 — Data cleaning and feature engineering (Colab section 4)", level=1)
doc.add_heading("4.1 Why", level=2)
add_para(
    "Even a “clean” UCI table must be certified: missing, duplicates, negative counts, hour codes outside 1–27. "
    "Feature engineering then turns Hour_code into clock time, weekday, period, peak flag, risk band, and lag features "
    "so later charts and Power BI slicers have human labels."
)
doc.add_heading("4.2 Validation — what we check", level=2)
add_code(
    "df.isnull().sum()          # missing per column\n"
    "df.duplicated().sum()      # exact duplicate rows\n"
    "Hour (Coded) min/max       # must be 1–27\n"
    "Slowness min/max           # should be inside 0–100\n"
    "incident columns < 0       # must be 0"
)
add_para("Result for this dataset: 0 missing, 0 duplicates, hour 1–27, slowness about 3.4% to 23.4%, no negative incident counts. No imputation, no row drops.")

doc.add_heading("4.3 Column renaming — why snake_case", level=2)
add_para(
    "Names such as “Slowness in traffic (%)” cannot be used as df.Slowness in traffic (%). "
    "Spaces also break Power BI DAX if you are not careful. The Colab dictionary maps every original name to a PEP-8 snake_case name. "
    "INCIDENTS is a Python list of the 16 count columns; TARGET is the string 'Slowness_percent'. Both are reused in every later cell so we never hard-code 16 names again."
)

doc.add_heading("4.4 Every engineered feature — what, why, how", level=2)
table(
    ["New column", "Why it exists", "How it is computed"],
    [
        ["Time", "Humans cannot read Hour_code 17", "07:00 + 30×(code−1) minutes; f-string zero pad"],
        ["Hour_of_day", "Integer hour for grouping", "7 + (code−1)//2"],
        ["Hour_decimal", "Continuous time axis", "7 + (code−1)*0.5"],
        ["Period", "Rush vs midday story", "codes ≤5 morning; ≥20 evening; else midday"],
        ["Period_Order", "Correct sort in Power BI", "Morning=1, Midday=2, Evening=3"],
        ["Date / DateTime", "Calendar and line charts", "14 Dec 2009 + 30 min × row index"],
        ["Weekday / Weekday_Num", "Day comparison", "row // 27 indexes Mon–Fri"],
        ["Day_index", "0–4 ordinal", "i // 27"],
        ["Total_incidents", "Burden of the slot", "sum of 16 incident columns, axis=1"],
        ["Incident_Types_Active", "Diversity of problems", "count of columns > 0"],
        ["Has_Incident", "Any vs none", "(Total_incidents > 0).astype(int)"],
        ["Is_Peak_Hour", "Rush flag for slicers", "1 if code ≤5 or ≥20"],
        ["Risk_Level", "Ops traffic-light", "pd.cut at 7.9 and 10.9 (tertiles/IQR-inspired)"],
        ["Risk_Order", "Numeric sort", "Low=1 Medium=2 High=3"],
        ["Slowness_Rolling3", "90-minute smooth", "rolling(3).mean()"],
        ["Slowness_Prev_Slot", "Lag-1", "shift(1)"],
        ["Slowness_Change", "Building vs easing", "current − previous"],
        ["Day_Avg_Slowness", "Day baseline", "mean slowness of that weekday"],
        ["Diff_From_Day_Avg", "Unusual for that day", "slot − day mean"],
        ["Slowness_Rank_In_Day", "Worst slot of the day", "groupby rank descending"],
        ["Slowness_ZScore", "Standardized extreme", "(x−mean)/std"],
        ["Row_ID", "Power BI key", "1…135"],
        ["Is_Outlier", "IQR flag (ch.11)", "outside Q1−1.5IQR / Q3+1.5IQR"],
        ["Predicted_Slowness", "RF fit (ch.13)", "best_model.predict"],
        ["Residual", "Model error", "actual − predicted"],
        ["Hour_code_sq", "U-shape for linear sim", "Hour_code ** 2"],
    ],
)
add_para(
    "Peak definition: morning codes 1–5 (07:00–09:00) and evening codes 20–27 (16:30–20:00). "
    "Risk cut-offs Low ≤ 7.9% and High ≥ 10.9% match thresholds.csv used by Power BI conditional colour."
)
add_para(
    "Lag and rolling features treat the 135 rows as one concatenated week. The first slot of Tuesday still uses Monday 20:00 as “previous”. "
    "That is acceptable for a dashboard trend line; it is not a within-day-only lag. The report states this so the method is honest."
)

# ── Ch5 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 5 — Descriptive statistics (Colab section 5)", level=1)
doc.add_heading("5.1 Why", level=2)
add_para("A few numbers (mean, median, IQR, skew) are the fingerprint of the target before we draw charts. They also tell us whether a later t-test would be naïve.")
doc.add_heading("5.2 What / How", level=2)
add_code("df[TARGET].describe()   # count, mean, std, min, 25%, 50%, 75%, max\ndf[TARGET].skew()       # >0 right tail\ndf[TARGET].kurt()       # excess kurtosis vs normal")
add_para("Typical values on this file:")
table(
    ["Statistic", "Approx. value", "Meaning"],
    [
        ["Count", "135", "All slots present"],
        ["Mean", "~10.0–10.5%", "Average delay across the working week"],
        ["Median", "~9.5–10%", "Slightly below the mean → right skew"],
        ["Std", "~4.3–4.5%", "Spread; evening peaks sit well above this"],
        ["Min / Max", "3.4% / 23.4%", "Quiet midday vs Friday-style crush"],
        ["Skewness", "positive (~0.8)", "A few very slow slots pull the mean"],
        ["Kurtosis", "near 0", "Not wildly heavy-tailed after IQR"],
    ],
)
add_para(
    "Incident describe() plus total_events and pct_slots_with_inc show that trolleybus defects appear often, "
    "while fire vehicles / dangerous freight are almost unique events. Rare events can still have huge mean-difference "
    "(fire vehicles) but unstable p-values — Chapter 9 treats n<3 as N/A."
)

# ── Ch6 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 6 — Univariate analysis (Colab section 6)", level=1)
doc.add_heading("6.1 Why", level=2)
add_para("Univariate = one variable. We must know the shape of slowness and the ranking of incident counts before we talk about relationships.")
doc.add_heading("6.2 What is drawn", level=2)
add_bullet("Histogram + KDE of Slowness_percent, with mean (red dashed) and median (orange dashed).")
add_bullet("Box plot of slowness (five-number summary + Tukey outliers).")
add_bullet("Horizontal bar of total events by incident type, sorted.")
doc.add_heading("6.3 How to read each chart", level=2)
add_para(
    "Histogram bins count how many slots fall in each slowness interval. KDE is a smooth density; with n=135 it is more readable than tiny bins. "
    "If mean > median, the right tail is pulling the average — expected for congestion."
)
add_para(
    "Box: box = Q1 to Q3 (IQR), inner line = median, whiskers = 1.5×IQR, dots = candidate outliers. "
    "Upper dots are the extreme evening slots studied in Chapter 11–12."
)
add_para(
    "Bar chart is sorted so the eye compares frequency, not alphabetical order. "
    "This answers RQ2 (frequency) only. RQ3 (impact) needs Chapter 9."
)

# ── Ch7 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 7 — Time-based analysis (Colab section 7)", level=1)
doc.add_heading("7.1 Why", level=2)
add_para("Traffic follows the working day. If we only reported a weekly average we would hide the evening crisis. This chapter answers RQ1.")
doc.add_heading("7.2 Chart 1 — hourly mean ± 1 sd", level=2)
add_para(
    "groupby Hour_code computes mean and std of slowness (std is across the five weekdays at that clock time). "
    "A line shows continuity of time; fill_between shows day-to-day variability. A wide band at 18:00 means some Fridays are much worse than some Mondays."
)
doc.add_heading("7.3 Chart 2 — three periods", level=2)
add_para("Morning / Midday / Evening bars. Evening is on the order of 60%+ worse than midday. Colour: orange morning, blue midday, red evening.")
doc.add_heading("7.4 Chart 3 — weekday × time heatmap", level=2)
add_para(
    "pivot_table(index=Weekday, columns=Time, values=Slowness, aggfunc=mean) builds a 5×27 grid. "
    "seaborn heatmap with cmap RdYlGn_r (reversed) uses green = free flow and red = jammed — the same traffic-light language as Risk_Level. "
    "Scan a column: if a time is red every day, it is structural peak demand. Scan a row: Friday is typically the darkest evening."
)
doc.add_heading("7.5 Chart 4 — peak vs off-peak by weekday", level=2)
add_para(
    "Is_Peak_Hour groups rush versus the rest. Peak is several percentage points higher every day. "
    "This is the operational argument for not doing signal maintenance at 18:00."
)

# ── Ch8 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 8 — Incident frequency (Colab section 8)", level=1)
doc.add_heading("8.1 Why", level=2)
add_para("We already ranked totals in Chapter 6. Here we ask whether incidents pile up at the same hours as slowness.")
doc.add_heading("8.2 Dual-axis chart — how and why twinx", level=2)
add_para(
    "Average incident count (0–few) and slowness (4–16%) cannot share one Y scale without crushing one series. "
    "ax.twinx() adds a second Y axis. Bars = mean Total_incidents by Time; line = mean slowness by Time."
)
add_para(
    "Finding: the evening slowness spike is stronger than the incident-count spike. Volume of cars (unmeasured) still matters. "
    "Incidents worsen an already loaded network; they are not the only story. That is why Hour_code dominates the Random Forest later."
)

# ── Ch9 ──────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 9 — Relationship analysis (Colab section 9)", level=1)
doc.add_heading("9.1 Why", level=2)
add_para("RQ3 and RQ4: association of each incident with slowness, visually and with a test that does not assume normality.")
doc.add_heading("9.2 Scatter + regplot", level=2)
add_para(
    "corrwith(target) ranks incidents; the top six get sns.regplot (scatter + OLS line + 95% CI). "
    "r in the title is Pearson. A steep red line and r > 0.3 is a candidate driver. Many zeros make a vertical stack at x=0 — that is real, not a bug."
)
doc.add_heading("9.3 Mann-Whitney U — why not a t-test", level=2)
add_para(
    "For each incident we split slots into count>0 vs count==0. Mann-Whitney U is rank-based (non-parametric). "
    "A t-test would assume roughly normal slowness in both groups; flooding has only about 6 “present” rows. "
    "If either group has n<3 we print N/A instead of a fake p-value."
)
add_para("H0: the two groups come from the same distribution. p<0.05 → reject H0. We still report the mean difference (effect size). A tiny n can fail significance even with a large difference (fire vehicles).")
table(
    ["Incident", "Approx. Δ slowness if present", "p-value (typical run)"],
    [
        ["Point of flooding", "+10.39 pp", "0.0001 ***"],
        ["Fire vehicles", "+6.80 pp", "N/A (n=1)"],
        ["Lack of electricity", "+5.86 pp", "0.0029 **"],
        ["Semaphore off", "+4.39 pp", "0.0096 **"],
        ["Immobilized bus", "+1.77 pp", "~0.05 *"],
        ["Trolleybus network defect", "slightly negative", "not significant"],
    ],
)
add_para(
    "Trolleybus defects are common including at midday, so the unconditional mean slowness when they are present can be lower. "
    "That is confounding by time of day — another reason the model includes Hour_code."
)

# ── Ch10 ─────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 10 — Correlation analysis (Colab section 10)", level=1)
doc.add_heading("10.1 Why two coefficients", level=2)
add_para("Pearson r measures linear association. Spearman ρ uses ranks (monotonic, more robust to outliers and to 0–1–2 count scales). If both agree, the relationship is roughly linear. If Spearman >> Pearson, the link is curved.")
doc.add_heading("10.2 How the heatmap is built", level=2)
add_code(
    "corr = df[['Hour_code']+INCIDENTS+[TARGET]].corr()\n"
    "mask = np.triu(np.ones_like(corr, dtype=bool))\n"
    "sns.heatmap(corr, mask=mask, cmap='coolwarm', center=0, annot=True, fmt='.2f')"
)
add_para("The upper triangle is masked because r(X,Y)=r(Y,X). coolwarm is centred at 0 so blue = negative and red = positive.")
add_para("Typical positive correlations with slowness: Lack of electricity (~0.44), Point of flooding (~0.42), Semaphore off (~0.35), Hour_code (evening codes are large numbers).")
add_para(
    "Warning (correlation ≠ causation): with only five days, anything that happens to occur in the evening will correlate with slowness. "
    "We treat numbers as exploratory associations."
)

# ── Ch11 ─────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 11 — Outlier analysis (Colab section 11)", level=1)
doc.add_heading("11.1 Why we flag but do not delete", level=2)
add_para("n=135. Dropping Friday 19:00 would hide the phenomenon we care about. Outliers here are real congestion, not sensor garbage.")
doc.add_heading("11.2 IQR method — how", level=2)
add_code(
    "Q1, Q3 = quantiles 0.25, 0.75\n"
    "IQR = Q3 - Q1\n"
    "lower = Q1 - 1.5*IQR   # here it goes negative → no low outliers\n"
    "upper = Q3 + 1.5*IQR   # about 20–21%\n"
    "Is_Outlier = slowness < lower OR slowness > upper"
)
add_para("Tukey’s 1.5×IQR rule is the same rule the box plot uses, so Chapter 6 and 11 agree. A few Friday evening points sit above the upper fence. They are kept and exported for Power BI.")
add_para("Incident boxplots show right-skewed counts (lots of zeros, rare spikes). Those spikes are also kept.")

# ── Ch12 ─────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 12 — Top and bottom observations (Colab section 12)", level=1)
add_para(
    "sort_values(TARGET, ascending=False).head(10) lists the worst half-hours. "
    "They concentrate on late afternoon/evening, often Friday, often with several incident types at once."
)
add_para(
    "The smoothest ten are typically early midday or early morning with few incidents. "
    "This qualitative check matches the heatmap: the model of “evening + flood/power/signal” is not an average-only illusion."
)

# ── Ch13 ─────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 13 — Predictive baseline (Colab section 13)", level=1)
doc.add_heading("13.1 Why a model inside EDA", level=2)
add_para("Prediction is not the course goal. The model is a check: if hour + incidents cannot explain slowness, our charts over-claimed. R² also becomes a KPI on the Power BI predictive page. Residuals become a column for “worse than expected” slots.")
doc.add_heading("13.2 Features", level=2)
add_code("FEATURES = ['Hour_code'] + INCIDENTS\nX, y = df[FEATURES], df[TARGET]")
add_para("We do not include Period or Is_Peak_Hour in the ML features because they are deterministic functions of Hour_code (leakage / redundancy).")
doc.add_heading("13.3 Ridge — what and why", level=2)
add_para(
    "Ridge = linear regression + L2 penalty α Σ β². On 135 rows and 17 features, unpenalized OLS overfits. "
    "StandardScaler is required because Hour_code (1–27) and binary-ish incidents live on different scales. Pipeline: StandardScaler → Ridge(alpha=1.0)."
)
doc.add_heading("13.4 Random Forest — what and why", level=2)
add_para(
    "300 trees, random_state=42 for reproducibility. Trees capture the U-shaped time effect without us typing Hour_code². "
    "They also capture interactions (flooding in the evening). Feature importance = mean decrease in MSE."
)
doc.add_heading("13.5 Cross-validation — how", level=2)
add_code("cv = KFold(n_splits=5, shuffle=True, random_state=42)\ncross_val_score(model, X, y, cv=cv, scoring='r2')")
add_para("A single 80/20 split would test on only ~27 rows. 5-fold uses every row once as test. Shuffle=True because rows are time-ordered; without shuffle a fold might be “all Friday”. (A purely temporal split would be stricter for forecasting; this project is explanatory EDA, not next-week forecast.)")
table(
    ["Model", "Typical CV R²", "Typical MAE", "Why it wins/loses"],
    [
        ["Ridge", "~0.55", "~3.0 pp", "Linear; cannot bend at evening"],
        ["Random Forest", "~0.70", "~2.2 pp", "Non-linear time + interactions"],
    ],
)
add_para("Hour_code is usually the top importance. Then electricity, flooding, semaphore. That matches Chapters 7 and 9.")
doc.add_heading("13.6 Linear export model (simulator)", level=2)
add_para(
    "Power BI and the HTML sliders need interpretable coefficients, not 300 trees. "
    "Section 15 fits LinearRegression on Hour_code, Hour_code², and a few high-impact incidents. "
    "In-sample R² is only for the toy simulator. The official accuracy claim remains the RF cross-validation."
)

# ── Ch14 Power BI ────────────────────────────────────────────────────────
doc.add_heading("Chapter 14 — Power BI full dashboard (Colab sections 15–17)", level=1)
doc.add_heading("14.1 Why Power BI (and the HTML twin)", level=2)
add_para(
    "Python is the analysis lab. Power BI is the product for a traffic manager who will not open Colab. "
    "An existing HTML dashboard was already in the project folder; this submission enhances it into a five-page full dashboard "
    "with embedded data, extra KPI tiles, heatmap, peak vs off-peak, impact vs frequency, actual-vs-predicted, what-if sliders, "
    "and a data-model page. The same pages are specified below for Power BI Desktop using the enhanced CSV folder."
)
add_para(
    "You cannot attach a binary .pbix from this environment in a fully compiled form without Power BI Desktop. "
    "The complete dashboard is delivered as: (1) star-schema CSVs ready to load, (2) DAX measure file, (3) page-by-page build instructions, "
    "(4) Sao_Paulo_Traffic_FULL_DASHBOARD.html which already runs those pages. Building the .pbix is then a load-and-layout task, not a data-prep task."
)

doc.add_heading("14.2 What was already done vs what was enhanced", level=2)
table(
    ["Already in the project", "Enhancement in this complete version"],
    [
        ["traffic_clean, incidents_long, incident_impact", "Still the core facts — unchanged grain (135 / 2160 / 16)"],
        ["dim_time, dim_weekday", "Still the star dimensions"],
        ["model_coefficients, thresholds", "Still drive the simulator and risk colours"],
        ["4-tab HTML that required CSV upload", "FULL HTML: 5 pages, data embedded, extra KPIs, RF importance, residuals, data model tab"],
        ["Basic DAX in the old markdown report", "PowerBI_DAX_Measures.txt with MAE, RMSE, peak premium, evening gap, presence %"],
        ["7 tables", "Added kpi_summary, weekday_summary, period_summary, hourly_summary, peak_offpeak_summary, risk_by_weekday, feature_importance, model_relationships"],
    ],
)

doc.add_heading("14.3 Star schema — why this design", level=2)
add_para(
    "A star schema puts measurements in a fact table and labels in small dimensions. Power BI relationships stay many-to-one, slicers stay fast, "
    "and Time / Weekday labels are not repeated as messy calculated columns. incidents_long exists because a clustered bar “by incident type” is painful in wide format (16 columns)."
)
table(
    ["Table", "Rows", "Grain / purpose"],
    [
        ["traffic_clean.csv", "135", "Fact: one 30-min city snapshot"],
        ["incidents_long.csv", "2160", "Fact: one row per slot × incident type"],
        ["incident_impact.csv", "16", "Precomputed present/absent impact"],
        ["dim_time.csv", "27", "Hour_code → clock, period, peak"],
        ["dim_weekday.csv", "5", "Weekday → number → date"],
        ["model_coefficients.csv", "8", "Linear what-if terms"],
        ["thresholds.csv", "2", "Low_Max=7.9, High_Min=10.9"],
        ["kpi_summary.csv", "12", "Headline numbers for cards if needed"],
        ["weekday_summary.csv", "5", "Day-level rollup"],
        ["period_summary.csv", "3", "Period rollup"],
        ["hourly_summary.csv", "27", "Clock-time rollup"],
        ["peak_offpeak_summary.csv", "10", "Weekday × peak flag"],
        ["risk_by_weekday.csv", "15", "Risk mix per day"],
        ["feature_importance.csv", "17", "RF importance %"],
        ["model_relationships.csv", "6", "Documentation of joins"],
    ],
)

doc.add_heading("14.4 How to load in Power BI Desktop", level=2)
add_para("1. Open Power BI Desktop → Get data → Text/CSV.")
add_para("2. Load every CSV in folder “powerbi_data EDA DATA”. (Or unzip powerbi_export.zip from Colab section 15 — same names.)")
add_para("3. In Model view, hide Text/CSV auto-generated tables if duplicates appear; keep one of each name.")
add_para("4. Create relationships (from → to, many-to-one, single cross-filter unless noted):")
table(
    ["From", "To", "Cardinality"],
    [
        ["traffic_clean[Hour_code]", "dim_time[Hour_code]", "Many-to-one"],
        ["traffic_clean[Weekday]", "dim_weekday[Weekday]", "Many-to-one"],
        ["incidents_long[Row_ID]", "traffic_clean[Row_ID]", "Many-to-one"],
        ["incidents_long[Hour_code]", "dim_time[Hour_code]", "Many-to-one (optional)"],
        ["hourly_summary[Hour_code]", "dim_time[Hour_code]", "Many-to-one"],
        ["weekday_summary[Weekday]", "dim_weekday[Weekday]", "One-to-one"],
    ],
)
add_para("5. Home → New table → name it Measures. Paste PowerBI_DAX_Measures.txt (also listed below).")
add_para("6. Report view → add 4 pages (+ optional 5th documentation page). Use slicers: dim_weekday[Weekday], dim_time[Period], dim_time[Is_Peak_Hour]. Set slicers to sync across pages (View → Sync slicers).")

doc.add_heading("14.5 DAX measures — what each one is for", level=2)
add_para("DAX is Power BI’s formula language. Measures recalculate with whatever the user has filtered. That is why we do not hard-code “average = 10.05” on a card.")
add_code(
    "Avg Slowness = AVERAGE(traffic_clean[Slowness_percent])\n"
    "Total Incident Events = SUM(traffic_clean[Total_Incidents])\n"
    "High Risk Slots = CALCULATE(COUNTROWS(traffic_clean), traffic_clean[Risk_Level]=\"High\")\n"
    "Peak Avg Slowness = CALCULATE(AVERAGE(traffic_clean[Slowness_percent]), traffic_clean[Is_Peak_Hour]=1)\n"
    "OffPeak Avg Slowness = CALCULATE(..., Is_Peak_Hour=0)\n"
    "Peak Premium = [Peak Avg Slowness] - [OffPeak Avg Slowness]\n"
    "Model RMSE = SQRT(AVERAGEX(traffic_clean, traffic_clean[Residual]^2))\n"
    "Incident Presence % = DIVIDE(CALCULATE(COUNTROWS(traffic_clean), Has_Incident=1), COUNTROWS(traffic_clean))"
)
add_para("CALCULATE changes the filter context (e.g. only peak hours). DIVIDE protects against divide-by-zero. AVERAGEX iterates rows for MAE/RMSE.")

doc.add_heading("14.6 Full dashboard — page layouts", level=2)
doc.add_heading("Page 1 — Executive Overview", level=3)
table(
    ["Visual", "Fields / measure", "Why"],
    [
        ["Card × 6", "Avg Slowness, Max Slowness, Total Incident Events, High Risk Slots, Peak Avg, OffPeak Avg", "30-second briefing"],
        ["Line", "dim_time[Time] vs Avg Slowness, legend Weekday", "U-shape of the day"],
        ["Clustered bar", "Period vs Avg Slowness", "Evening vs midday"],
        ["Donut", "Risk_Level count", "Share of high-risk slots"],
        ["Bar", "Weekday vs Avg Slowness", "Friday effect"],
        ["Slicers", "Weekday, Period, Peak flag", "Interactive what-if on filters only"],
    ],
)
doc.add_heading("Page 2 — Time Intelligence", level=3)
table(
    ["Visual", "Fields / measure", "Why"],
    [
        ["Cards", "Peak Avg, OffPeak Avg, Peak Premium, Peak Uplift %", "Quantify rush cost"],
        ["Matrix (heatmap)", "Rows Weekday, columns Time, values Avg Slowness, conditional colour red-yellow-green", "Same as seaborn heatmap"],
        ["Clustered bar", "Weekday × Is_Peak_Hour", "Peak gap every day"],
        ["Area / line", "DateTime or Row_ID vs Slowness_Rolling3", "90-minute smoothness"],
    ],
)
add_para("Conditional formatting: use thresholds Low_Max 7.9 and High_Min 10.9 (or the Risk_Level column directly).")
doc.add_heading("Page 3 — Incident Analysis", level=3)
table(
    ["Visual", "Fields", "Why"],
    [
        ["Horizontal bar", "incident_impact[Incident], Impact_Points", "RQ3 ranking"],
        ["Horizontal bar", "Incident, Total_Events", "RQ2 ranking — put beside impact so students see they differ"],
        ["Clustered bar", "Avg_Slowness_With vs Without", "Same story as Mann-Whitney means"],
        ["Table", "Top 10 from traffic_clean sorted by slowness", "Chapter 12 in interactive form"],
        ["Slicer", "incidents_long[Incident]", "Filter the long table if you add a time line of one type"],
    ],
)
doc.add_heading("Page 4 — Predictive Insights", level=3)
table(
    ["Visual", "Fields", "Why"],
    [
        ["Bar", "model_coefficients Feature vs Coefficient", "What-if linear effects"],
        ["Bar", "feature_importance Feature vs Importance_Pct", "RF ranking"],
        ["Scatter", "Predicted_Slowness (X) vs Slowness_percent (Y)", "Fit quality"],
        ["Column", "Row_ID vs Residual", "Under/over prediction"],
        ["Cards", "Model MAE, Model RMSE", "Error in slowness points"],
        ["What-if parameters (optional)", "Hour_code 1–27 + incident what-if", "Same idea as HTML sliders; or keep HTML for sliders"],
    ],
)
doc.add_heading("Page 5 — Data model (documentation page)", level=3)
add_para("A text box listing grain, relationships, and “correlation is not causation”. This is the page examiners can screenshot as evidence that the Power BI model was designed, not a single dumped table.")

doc.add_heading("14.7 Colour and UX rules used", level=2)
add_bullet("Traffic light: green Low, amber Medium, red High — same as Colab heatmap.")
add_bullet("KPIs on top, charts below, slicers left or top (standard dashboard F-pattern).")
add_bullet("Titles state the question (“Evening is worse than midday”), not just “Bar chart 1”.")
add_bullet("Sync slicers so a Friday filter on Page 1 still applies on Page 3.")

doc.add_heading("14.8 HTML dashboard — how it completes the Power BI story", level=2)
add_para(
    "Sao_Paulo_Traffic_FULL_DASHBOARD.html loads in any browser with no Power BI license. "
    "It embeds traffic_clean + coefficients + impact + feature importance as JSON, so there is no file picker. "
    "Tabs 1–5 match the Power BI pages. This is the guaranteed visual deliverable; Desktop is the professional BI deliverable using the same tables."
)

# ── Ch15 ─────────────────────────────────────────────────────────────────
doc.add_heading("Chapter 15 — Key insights and conclusion (Colab section 14)", level=1)
doc.add_heading("15.1 Answers to the research questions", level=2)
add_para("RQ1 — When is slowness highest?", bold=True)
add_para("Evening 16:30–20:00 (highest mean). Morning 07:00–09:30 is a smaller peak. Midday is lowest. Friday evening is the worst band on the heatmap.")
add_para("RQ2 — Most frequent incidents?", bold=True)
add_para("Trolleybus network defects dominate counts; immobilized buses and broken trucks follow; then semaphore off and lack of electricity. Fire / dangerous freight are almost unique.")
add_para("RQ3 — Most associated with slowness?", bold=True)
add_para("Flooding (+~10.4 pp), fire vehicles (rare), lack of electricity (+~5.9 pp), semaphore off (+~4.4 pp). High frequency ≠ high impact.")
add_para("RQ4 — Significant?", bold=True)
add_para("Flooding, electricity, and semaphore off typically p<0.01 on Mann-Whitney (n large enough). Rare types are inconclusive.")
add_para("RQ5 — Outliers?", bold=True)
add_para("A handful of slots exceed the IQR upper fence (~21%). They are genuine Friday-style extremes. Not removed.")
add_para("RQ6 — Can we explain slowness?", bold=True)
add_para("Random Forest CV R² ≈ 0.70 with hour + incidents. About 30% remains (weather, unmeasured volume, events). Enough to say the EDA variables are real drivers, not noise.")

doc.add_heading("15.2 Recommendations", level=2)
table(
    ["Finding", "Action"],
    [
        ["Evening ~60%+ worse than midday", "Staggered hours / congestion pricing discussion; do not plan works at 18:00"],
        ["Flooding +10 pp", "Drainage and flood-point mapping before rainy season"],
        ["Electricity +5.9 pp", "UPS / backup for traffic signals on busy corridors"],
        ["Semaphore off +4.4 pp", "24/7 signal repair SLA"],
        ["Trolleybus defects very frequent", "Maintenance programme (reliability), even if not the top slowness lever"],
        ["Friday worst", "Extra transit supply and incident patrols on Friday afternoon"],
    ],
)

doc.add_heading("15.3 Limitations", level=2)
add_bullet("Only five weekdays in December 2009 — no weekend, no season, no 2020s network.")
add_bullet("No geography — cannot draw a street heatmap.")
add_bullet("No weather column — flooding is partly rain in disguise.")
add_bullet("Associations, not causal experiments.")
add_bullet("RF in-sample predictions on the same 135 rows are optimistic for new days; we therefore quote cross-validation, not training R², as the headline.")

doc.add_heading("15.4 Future work", level=2)
add_bullet("A year of data; merge rainfall; GPS / camera locations; time-series models (lag features only within day); deploy a small API for next-slot prediction.")

# ── Refs ─────────────────────────────────────────────────────────────────
doc.add_heading("References", level=1)
add_para("Correa da Silva, E. A. (2017). Behavior of the Urban Traffic of the City of Sao Paulo in Brazil [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5902F")
add_para("Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley. (IQR / box plot rule used in Chapters 6 and 11.)")
add_para("McKinney, W. (2010). Data structures for statistical computing in Python. Proc. SciPy.")
add_para("Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering.")
add_para("Waskom, M. L. (2021). seaborn: statistical data visualization. JOSS.")
add_para("Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. JMLR.")
add_para("Virtanen et al. (2020). SciPy 1.0. Nature Methods.")
add_para("Microsoft. Power BI documentation. https://learn.microsoft.com/en-us/power-bi/")

# ── App A ────────────────────────────────────────────────────────────────
doc.add_heading("Appendix A — Feature dictionary (Colab §4 + exports)", level=1)
add_para("See Chapter 4 table. Power BI fact table also keeps original 16 incident columns in wide form so cards can SUM a single type without using incidents_long.")

doc.add_heading("Appendix B — Power BI page map vs Colab", level=1)
table(
    ["Power BI / HTML page", "Colab sections that produced the numbers"],
    [
        ["1 Executive Overview", "5, 6, 7"],
        ["2 Time Intelligence", "7"],
        ["3 Incident Analysis", "8, 9, 12"],
        ["4 Predictive Insights", "10, 13, 15, 16"],
        ["5 Data model", "4, 15, 17"],
    ],
)

doc.add_heading("Appendix C — Linear simulator coefficients", level=1)
add_para("Exported in model_coefficients.csv (typical values from the project data):")
table(
    ["Feature", "Coefficient", "How to read it"],
    [
        ["Intercept", "6.88", "Baseline when coded hour and listed incidents are 0"],
        ["Hour_code", "−0.052", "Linear time tilt"],
        ["Hour_code_sq", "+0.014", "Quadratic U-shape (evening rise)"],
        ["Lack_of_electricity", "+1.37", "Added slowness % per extra outage count"],
        ["Point_of_flooding", "+1.02", "Per extra flood point"],
        ["Semaphore_off", "+0.83", "Per extra dead signal"],
        ["Fire_vehicles", "+2.44", "Large per event; extremely rare"],
        ["Defect trolleybuses", "−0.49", "Same sign as Chapter 9 (confounded by time)"],
    ],
)

doc.add_heading("Appendix D — How to submit / run the full project", level=1)
add_para("1. Upload Smart_Urban_Transportation_EDA_COLAB.ipynb to Google Colab → Runtime → Run all. Screenshot key figures for the appendix of a printed report if required.")
add_para("2. Download powerbi_export.zip from the Colab download cell (or use the folder already in this zip: powerbi_data EDA DATA).")
add_para("3. Open Sao_Paulo_Traffic_FULL_DASHBOARD.html to demonstrate the five-page dashboard immediately.")
add_para("4. In Power BI Desktop, load the CSVs, create relationships, paste DAX, build the four analytical pages as in Chapter 14, save as SãoPaulo_Traffic_EDA.pbix.")
add_para("5. Bind this Word file as the official report. Section numbers already match the notebook.")

p = doc.add_paragraph()
r = p.add_run("End of report — Hemavathy K · Kumaraguru College of Technology · EDA · October 2026")
r.italic = True
r.font.size = Pt(10)

out = ROOT / "Smart_Urban_Transportation_FULL_PROJECT_REPORT.docx"
doc.save(out)
print("Wrote", out, "bytes", out.stat().st_size)
