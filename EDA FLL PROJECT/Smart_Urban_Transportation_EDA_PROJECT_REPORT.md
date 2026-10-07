# 🚦 Smart Urban Transportation Systems
## Exploratory Data Analysis — Behavior of the Urban Traffic of São Paulo, Brazil

---

| Field | Details |
|---|---|
| **Student Name** | Hemavathy K |
| **Institution** | Kumaraguru College of Technology (KCT) |
| **Subject** | Exploratory Data Analysis (EDA) |
| **Dataset** | UCI ML Repository — ID 483 |
| **Date** | October 2026 |
| **Tool Stack** | Python (Google Colab) · Power BI · pandas · seaborn · scikit-learn |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Chapter 1: Introduction](#chapter-1-introduction)
3. [Chapter 2: Setup & Environment](#chapter-2-setup--environment)
4. [Chapter 3: Initial Dataset Examination](#chapter-3-initial-dataset-examination)
5. [Chapter 4: Data Cleaning & Feature Engineering](#chapter-4-data-cleaning--feature-engineering)
6. [Chapter 5: Descriptive Statistics](#chapter-5-descriptive-statistics)
7. [Chapter 6: Univariate Analysis](#chapter-6-univariate-analysis)
8. [Chapter 7: Time-Based Analysis](#chapter-7-time-based-analysis)
9. [Chapter 8: Incident Frequency Analysis](#chapter-8-incident-frequency-analysis)
10. [Chapter 9: Relationship Analysis](#chapter-9-relationship-analysis)
11. [Chapter 10: Correlation Analysis](#chapter-10-correlation-analysis)
12. [Chapter 11: Outlier Analysis](#chapter-11-outlier-analysis)
13. [Chapter 12: Top & Bottom Observations](#chapter-12-top--bottom-observations)
14. [Chapter 13: Predictive Baseline](#chapter-13-predictive-baseline)
15. [Chapter 14: Power BI Dashboard](#chapter-14-power-bi-dashboard)
16. [Chapter 15: Key Insights & Conclusion](#chapter-15-key-insights--conclusion)
17. [References](#references)
18. [Appendix](#appendix)

---

## Executive Summary

This project performs a complete **Exploratory Data Analysis (EDA)** on the *Behavior of the Urban Traffic of the City of São Paulo in Brazil* dataset from the UCI Machine Learning Repository (ID: 483). The dataset captures 135 half-hourly traffic observations recorded between 7:00 AM and 8:00 PM across five consecutive weekdays (December 14–18, 2009) in São Paulo — one of the world's most congested cities.

**Key findings at a glance:**

- 🕐 **Peak congestion** occurs during the **evening rush hour (16:30–20:00)** with average slowness reaching 13–16%. Morning rush (07:00–09:30) is also significantly congested (~9–11%).
- 🌊 **Point of flooding** is the most impactful incident type, adding ~10.4 percentage points to traffic slowness.
- ⚡ **Lack of electricity** (traffic light outages) adds ~5.86 points, and **Semaphore off** adds ~4.39 points — highlighting that traffic signal failures severely worsen congestion.
- 🚌 **Broken trucks** and **Immobilized buses** are the most *frequent* incidents but have moderate impact compared to flooding.
- 📊 The dataset is **clean** — zero missing values and zero duplicate rows — enabling direct analysis without imputation.
- 🤖 A **Random Forest baseline model** achieves R² ≈ 0.70 using only time-of-day and incident counts as features, confirming strong predictability from these variables.
- 📈 The **Power BI dashboard** provides interactive exploration across four analytical views: Executive Overview, Time Intelligence, Incident Analysis, and Predictive Insights.

The complete project delivers:
1. **Google Colab Notebook** — 15 analytical sections, each with detailed code and parallel explanations
2. **Power BI Dashboard** — 7 interconnected data tables in a star schema with interactive visuals
3. **Project Report** (this document) — Comprehensive documentation of every step, method, and finding

---

## Chapter 1: Introduction

### 1.1 Background & Motivation

Urban transportation is one of the most pressing infrastructure challenges of the 21st century. São Paulo, Brazil — home to over 21 million people in its metropolitan area — consistently ranks among the world's most traffic-congested cities. According to global mobility indices, São Paulo commuters lose hundreds of hours annually to traffic delays. Understanding *when* congestion peaks and *which incidents* worsen it is critical for:

- **Traffic management authorities** who need to allocate resources (signal controllers, rapid-response teams) effectively
- **Public transport operators** who must adjust bus/metro schedules around peak periods
- **Emergency services** who need to plan routing strategies during incidents
- **Urban planners** who must design infrastructure to reduce bottlenecks
- **Data scientists** who build predictive systems for smart city applications

Exploratory Data Analysis (EDA) provides the analytical foundation before any machine learning model is built. It answers "What is happening in the data?" before we ask "Why is it happening?" or "What will happen next?"

### 1.2 Problem Statement

This EDA project addresses the following six research questions:

> **RQ1:** At what times of day is traffic slowness highest, and does the pattern differ by day of week?

> **RQ2:** Which incident types occur most frequently in São Paulo traffic?

> **RQ3:** Which incidents are most strongly associated with higher traffic slowness?

> **RQ4:** Are there statistically significant differences in slowness when specific incidents are present versus absent?

> **RQ5:** Does the dataset contain outliers, and what characterizes the most extreme congestion events?

> **RQ6:** Can a simple predictive model using time and incident features explain a meaningful portion of slowness variance?

### 1.3 Dataset Description

| Property | Value |
|---|---|
| **Source** | UCI Machine Learning Repository |
| **Dataset ID** | 483 |
| **DOI** | 10.24432/C5902F |
| **License** | CC BY 4.0 |
| **URL** | https://archive.ics.uci.edu/dataset/483 |
| **Observations** | 135 rows |
| **Variables** | 18 columns (17 explanatory + 1 target) |
| **Time Span** | Dec 14–18, 2009 (Monday–Friday) |
| **Temporal Resolution** | Every 30 minutes, 07:00–20:00 |
| **Geography** | São Paulo, Brazil |
| **File Format** | CSV (semicolon-separated, comma decimal) |

The dataset was donated by Edilson Anselmo Correa da Silva and represents real-world traffic monitoring data collected from São Paulo's traffic management center.

### 1.4 Dataset Variables

The dataset contains 18 variables:

| # | Original Column Name | Renamed | Type | Description |
|---|---|---|---|---|
| 1 | Hour (Coded) | Hour_code | Integer (1–27) | Sequential time slot code (1 = 07:00, 27 = 20:00) |
| 2 | Immobilized bus | Immobilized_bus | Integer (0–4) | Count of immobilized buses in that time slot |
| 3 | Broken Truck | Broken_Truck | Integer (0–5) | Count of broken-down trucks |
| 4 | Vehicle excess | Vehicle_excess | Integer (0–1) | Whether vehicle excess was detected |
| 5 | Accident victim | Accident_victim | Integer (0–3) | Accident victims involved |
| 6 | Running over | Running_over | Integer (0–2) | Pedestrian runover incidents |
| 7 | Fire vehicles | Fire_vehicles | Integer (0–1) | Fire-related vehicle events |
| 8 | Occurrence involving freight | Occurrence_involving_freight | Integer (0–1) | Freight incidents |
| 9 | Incident involving dangerous freight | Incident_involving_dangerous_freight | Integer (0–1) | Hazardous material incidents |
| 10 | Lack of electricity | Lack_of_electricity | Integer (0–4) | Power outage events affecting traffic |
| 11 | Fire | Fire | Integer (0–1) | Fire incidents near traffic |
| 12 | Point of flooding | Point_of_flooding | Integer (0–7) | Flooding points on roads |
| 13 | Manifestations | Manifestations | Integer (0–1) | Public demonstrations/protests |
| 14 | Defect in trolleybus network | Defect_in_the_network_of_trolleybuses | Integer (0–8) | Trolleybus infrastructure defects |
| 15 | Tree on the road | Tree_on_the_road | Integer (0–1) | Fallen trees blocking roads |
| 16 | Semaphore off | Semaphore_off | Integer (0–4) | Non-functioning traffic signals |
| 17 | Intermittent Semaphore | Intermittent_Semaphore | Integer (0–1) | Intermittently functioning signals |
| 18 | Slowness in traffic (%) | Slowness_percent | Float | **TARGET** — Overall traffic slowness percentage |

> **Note:** The `Hour_code` variable encodes both the day and time. Since data is recorded for 27 time slots per day (07:00–19:30, every 30 min) × 5 days = 135 rows, the hour code cycles 1–27 for each weekday.

### 1.5 Intended Users & Applications

This analysis is designed for:
- **Traffic management authorities** → Use time-based insights to staff signal repair teams during peak hours
- **Urban planners** → Use incident frequency data to prioritize infrastructure resilience (drainage, power backup)
- **Public transport operators** → Adjust bus schedules around peak and flooding-prone time slots
- **Emergency services** → Understand which incident types cause the most congestion to pre-position resources
- **Data scientists & students** → Use as a teaching example for EDA methodology on real-world transportation data

### 1.6 Project Objectives

1. Perform end-to-end EDA following industry-standard methodology
2. Engineer meaningful features for temporal and categorical analysis
3. Identify the time periods of highest traffic congestion
4. Rank incident types by frequency and by impact on slowness
5. Validate statistical associations using correlation and hypothesis testing
6. Build a predictive baseline to quantify explainability
7. Export structured data for Power BI interactive visualization
8. Document every analytical decision with justification

---

## Chapter 2: Setup & Environment

### 2.1 Python Libraries Used

EDA in Python relies on a curated ecosystem of libraries. The table below explains each library used in this project:

| Library | Version | Purpose | Why Chosen |
|---|---|---|---|
| `pandas` | ≥1.5 | Data loading, cleaning, transformation, groupby aggregations | Industry standard for tabular data manipulation; provides DataFrame and Series structures |
| `numpy` | ≥1.23 | Numerical arrays, mathematical operations, statistical computations | Foundation for all numerical computing in Python; used by all other libraries |
| `matplotlib` | ≥3.6 | Base plotting library for all 2D visualizations | Provides fine-grained control over every plot element; used by seaborn as backend |
| `seaborn` | ≥0.12 | High-level statistical visualization | Simplifies complex plots (heatmaps, boxplots, regplots) with better default aesthetics |
| `scipy.stats` | ≥1.9 | Statistical tests (Mann-Whitney U, Pearson correlation, p-values) | Provides validated implementations of statistical tests; the `stats` module is industry standard |
| `scikit-learn` | ≥1.1 | Machine learning baseline (Ridge, Random Forest, cross-validation) | Most widely used ML library in Python; consistent API across algorithms |

### 2.2 Data Loading Strategy

The notebook implements a **robust 4-step fallback loading mechanism** to ensure the dataset loads regardless of network conditions or environment:

```
Step 1: Check for a local CSV file matching "sao paulo" pattern
   ↓ (if not found)
Step 2: Download directly from UCI zip archive
   ↓ (if network fails)
Step 3: Install and use the ucimlrepo Python package
   ↓ (if that also fails)
Step 4: Prompt for manual file upload (Google Colab only)
```

**Why this multi-step approach?**
- Colab sessions are ephemeral — files don't persist between sessions
- UCI servers can occasionally be unreachable
- Researchers may want to run offline from a pre-downloaded CSV
- The `ucimlrepo` package provides a programmatic API as a reliable backup

### 2.3 Loading Code Explanation

```python
import os, io, zipfile, urllib.request, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')    # Suppress non-critical warnings during EDA
sns.set_theme(style='whitegrid')     # Apply consistent visual theme to all seaborn plots
plt.rcParams['figure.dpi'] = 110    # Set high resolution for clear plots
pd.set_option('display.max_columns', 30)  # Show up to 30 columns (dataset has 18)
```

**Line-by-line:**
- `os, io, zipfile, urllib.request` — Standard library modules for file operations and HTTP downloads
- `warnings.filterwarnings('ignore')` — Suppresses `FutureWarning` and `DeprecationWarning` that clutter output without affecting results
- `sns.set_theme(style='whitegrid')` — Sets a clean white background with subtle gridlines for all seaborn plots; `context='notebook'` scales element sizes for Colab's display
- `plt.rcParams['figure.dpi'] = 110` — DPI (dots per inch) controls image sharpness; 110 is a good balance between quality and file size in Colab

**Data reading function:**
```python
def read_uci_csv(path_or_buffer):
    return pd.read_csv(path_or_buffer, sep=';', decimal=',')
```
The original UCI file uses **semicolons (`;`) as delimiters** (common in Portuguese/European locales) and **commas (`,`) as decimal separators** (e.g., `4,1` means `4.1`). The `sep=';'` and `decimal=','` parameters handle this non-standard formatting correctly.

---

## Chapter 3: Initial Dataset Examination

### 3.1 Why We Examine Raw Data First

Before any cleaning or analysis, we must understand the raw data exactly as received. This step answers:
- How many rows and columns are there?
- What are the data types of each column?
- Do the first and last rows look reasonable?
- Is the data structured as expected?

Skipping this step is a common EDA mistake that leads to incorrect assumptions about the data's structure.

### 3.2 Dataset Dimensions

```python
print(f'Rows: {df.shape[0]}, Columns: {df.shape[1]}')
# Output: Rows: 135, Columns: 18
```

The dataset is **small but rich** — 135 observations over 5 days with 17 incident-type features. With such a small dataset:
- Every observation is valuable; we should be cautious about dropping rows
- Statistical tests should be interpreted conservatively (small sample means wider confidence intervals)
- Correlations may appear strong by chance (spurious correlations)

### 3.3 Column Overview

All 18 columns are numeric (integer or float). This is notable because:
- **No categorical string columns** → No need for label encoding before modeling
- **Hour_code is ordinal** (1–27 mapping to time slots), not truly continuous → needs careful treatment
- **Incident variables are count-valued** (0, 1, 2, 3... occurrences) → not binary flags but event counts
- **Target (Slowness_percent)** is a continuous float from 3.4 to 23.4

### 3.4 Data Types Analysis

| Variable Type | Count | Examples |
|---|---|---|
| Integer (ordinal time) | 1 | Hour_code |
| Integer (event counts) | 16 | All incident columns |
| Float (continuous target) | 1 | Slowness in traffic (%) |

**What to look for:**
- Are there any `object` (string) columns where numbers were expected? → No
- Are floating-point columns properly parsed? → Yes (decimal=','  handled it)
- Are there any unexpected data types? → No

### 3.5 First & Last Observations

The first 5 rows show Hour codes 1–5 (07:00–09:00), Monday, with mostly zero incidents. Slowness values of 4.1, 6.6, 8.7, 9.2, 11.1 show the morning ramp-up pattern clearly.

The last 5 rows show Hour codes 23–27 (18:30–20:00), Friday, with incident values present and slowness of 17.4–18.1%, confirming the expected evening rush pattern.

---

## Chapter 4: Data Cleaning & Feature Engineering

### 4.1 Why Data Cleaning is Essential

Raw data from real-world systems almost always contains quality issues:
- **Missing values** — sensors fail, fields are not recorded
- **Duplicate rows** — data entry errors or system retransmissions
- **Inconsistent types** — numbers stored as strings
- **Out-of-range values** — data entry errors (e.g., negative counts)
- **Column names** — spaces and special characters break Python code

Even if the data is clean (as in this case), documenting the verification step is essential for reproducibility and scientific rigor.

### 4.2 Missing Value Analysis

```python
print(df.isnull().sum())
# All 18 columns return 0 missing values
# Total missing: 0
```

**Result:** ✅ Zero missing values across all 135 observations.

**Interpretation:** The dataset was carefully curated before upload to UCI. In practice, traffic sensor data often has gaps due to sensor failures, network outages, or maintenance windows. The absence of missing values here simplifies the analysis significantly — no imputation strategy (mean fill, forward fill, interpolation) is needed.

### 4.3 Duplicate Row Check

```python
print(f'Duplicate rows: {df.duplicated().sum()}')
# Output: 0
```

**Result:** ✅ Zero duplicate rows.

**Why check?** Duplicate rows can artificially inflate the influence of certain time periods. For example, if the 08:00 Monday observation appeared twice, the morning period would be over-represented in all averages.

### 4.4 Range & Consistency Checks

| Variable | Expected Range | Actual Range | Status |
|---|---|---|---|
| Hour_code | 1–27 | 1–27 | ✅ |
| Slowness_percent | 0–100 | 3.4–23.4 | ✅ |
| All incident columns | ≥0 | 0–8 | ✅ |

No out-of-range values were found.

### 4.5 Column Renaming

**Why rename columns?**

The original UCI column names contain spaces and special characters (parentheses, `%`, etc.), which:
- Cannot be accessed with Python attribute syntax (`df.Slowness in traffic (%)` fails)
- Cause issues in SQL-like operations and Power BI column references
- Are inconsistent in style

```python
col_map = {
    'Hour (Coded)': 'Hour_code',
    'Slowness in traffic (%)': 'Slowness_percent',
    ...
}
df = df.rename(columns=col_map)
```

The renaming convention uses **snake_case** (lowercase words separated by underscores), which is the Python community standard (PEP 8).

### 4.6 Feature Engineering

Feature engineering is the process of creating new, more informative variables from existing ones. This step is crucial because:
- Raw features (like `Hour_code 1–27`) are not directly interpretable
- Engineered features can capture non-linear patterns (like the U-shape of slowness over the day)
- Some analyses require temporal context (weekday, period, peak hour) that isn't in the raw data

Below is a detailed explanation of every new feature created:

#### 4.6.1 Time String (`Time`)
```python
hour_to_time = {i: f"{7+(i-1)//2:02d}:{30*((i-1)%2):02d}" for i in range(1, 28)}
df['Time'] = df['Hour_code'].map(hour_to_time)
```
**Why:** Hour_code 1–27 is not human-readable. This maps codes to clock times (e.g., code 1 → "07:00", code 2 → "07:30").
**How:** 
- `(i-1)//2` gives the hour offset from 7:00 (integer division)
- `30*((i-1)%2)` gives 0 or 30 minutes (modulo alternates between 0 and 1)
- `f"{...}:02d"` zero-pads single digits (e.g., "07" not "7")

#### 4.6.2 Hour of Day (`Hour_of_day`)
```python
df['Hour_of_day'] = df['Hour_code'].apply(lambda x: 7 + (x-1)//2)
```
**Why:** An integer hour (7–20) is useful for heatmaps and bucket-level aggregations.

#### 4.6.3 Time Period (`Period`)
```python
df['Period'] = df['Hour_code'].apply(
    lambda x: 'Morning (07-09:30)' if x<=5 else 
    ('Evening (16:30-20)' if x>=20 else 'Midday (10-16)'))
```
**Why:** Grouping 27 time slots into 3 periods reduces dimensionality and aligns with real-world traffic patterns (morning rush, midday lull, evening rush).
**How:** Uses the natural breakpoints of São Paulo's traffic:
- Codes 1–5 → 07:00–09:00 (Morning rush)
- Codes 6–19 → 09:30–16:00 (Midday)
- Codes 20–27 → 16:30–20:00 (Evening rush)

#### 4.6.4 Weekday (`Weekday`, `Weekday_Num`)
```python
dates = pd.date_range('2009-12-14', '2009-12-18', freq='D')
df['Weekday'] = [(dates[i//27]).day_name() for i in range(135)]
df['Weekday_Num'] = [(dates[i//27]).dayofweek + 1 for i in range(135)]
```
**Why:** Since each day has exactly 27 time slots, integer division by 27 gives the day index (0=Monday, 1=Tuesday, ..., 4=Friday).
**How:** `dates[i//27]` selects the correct date; `.day_name()` returns the full weekday name; `.dayofweek + 1` gives 1=Monday, 5=Friday.

#### 4.6.5 Total Incidents (`Total_incidents`)
```python
df['Total_incidents'] = df[INCIDENTS].sum(axis=1)
```
**Why:** A single number summarizing the total incident burden at each time slot is useful for correlation analysis and as a model feature.
**How:** `axis=1` sums across columns (horizontally) for each row.

#### 4.6.6 Has Incident Flag (`Has_Incident`)
```python
df['Has_Incident'] = (df['Total_incidents'] > 0).astype(int)
```
**Why:** A binary flag (0/1) allows simple comparison: "Is slowness different when ANY incident is present?"

#### 4.6.7 Peak Hour Flag (`Is_Peak_Hour`)
```python
df['Is_Peak_Hour'] = df['Hour_code'].apply(lambda x: 1 if x<=5 or x>=20 else 0)
```
**Why:** Identifies rush-hour time slots for direct peak vs. off-peak comparison.
**Definition used:** Morning rush = codes 1–5 (07:00–09:00); Evening rush = codes 20–27 (16:30–20:00).

#### 4.6.8 Risk Level (`Risk_Level`, `Risk_Order`)
```python
df['Risk_Level'] = pd.cut(df[TARGET], bins=[0, 7.9, 10.9, 100], labels=['Low','Medium','High'])
df['Risk_Order'] = df['Risk_Level'].map({'Low':1,'Medium':2,'High':3})
```
**Why:** Categorizing continuous slowness into risk tiers enables traffic management decisions:
- **Low (0–7.9%):** Free-flowing traffic — no immediate action needed
- **Medium (7.9–10.9%):** Moderate congestion — monitor and prepare
- **High (>10.9%):** Severe congestion — activate response protocols
**How:** `pd.cut()` bins a continuous variable into discrete intervals. The thresholds (7.9, 10.9) were chosen based on the IQR of the slowness distribution.

#### 4.6.9 Rolling Average (`Slowness_Rolling3`)
```python
df['Slowness_Rolling3'] = df[TARGET].rolling(3, min_periods=1).mean().round(2)
```
**Why:** A 3-slot (90-minute) rolling average smooths short-term noise and reveals underlying trends.
**How:** `rolling(3)` creates a sliding window of 3 consecutive values; `min_periods=1` allows computation even at the start where fewer than 3 values exist.

#### 4.6.10 Lag Feature (`Slowness_Prev_Slot`)
```python
df['Slowness_Prev_Slot'] = df[TARGET].shift(1)
```
**Why:** Traffic at time t is often correlated with traffic at t-1 (autocorrelation). This lag feature enables change detection.
**How:** `shift(1)` moves values one position forward, so each row contains the *previous* row's slowness value. The first row gets NaN (no prior value).

#### 4.6.11 Change in Slowness (`Slowness_Change`)
```python
df['Slowness_Change'] = (df[TARGET] - df['Slowness_Prev_Slot']).round(2)
```
**Why:** Rate of change reveals whether congestion is building or easing at any given time slot.

#### 4.6.12 Daily Average & Deviation
```python
df['Day_Avg_Slowness'] = [df.loc[df['Weekday']==w, TARGET].mean() for w in df['Weekday']]
df['Diff_From_Day_Avg'] = (df[TARGET] - df['Day_Avg_Slowness']).round(2)
```
**Why:** Comparing each time slot's slowness to that day's average reveals which slots are unusually congested for that particular day.

#### 4.6.13 Rank Within Day (`Slowness_Rank_In_Day`)
```python
df['Slowness_Rank_In_Day'] = df.groupby('Weekday')[TARGET].rank(ascending=False).astype(int)
```
**Why:** Rank 1 = most congested slot of that day. Enables consistent cross-day comparison.

#### 4.6.14 Z-Score (`Slowness_ZScore`)
```python
df['Slowness_ZScore'] = ((df[TARGET] - df[TARGET].mean()) / df[TARGET].std()).round(3)
```
**Why:** Z-scores standardize values to a common scale (mean=0, std=1), making outlier detection universal. |Z| > 3 is a common outlier threshold.
**How:** Z = (X - μ) / σ. A Z-score of 2.5 means the observation is 2.5 standard deviations above the mean.

#### 4.6.15 Predicted Slowness & Residual
```python
df['Predicted_Slowness'] = best_model.predict(df[FEATURES]).round(2)
df['Residual'] = (df[TARGET] - df['Predicted_Slowness']).round(2)
```
**Why:** Residuals (actual - predicted) reveal observations where the model is consistently wrong — often the most interesting data points.

#### 4.6.16 Outlier Flag (`Is_Outlier`)
```python
df['Is_Outlier'] = ((df[TARGET] < lo) | (df[TARGET] > hi)).astype(int)
```
**Why:** Binary flag for IQR-detected outliers enables Power BI filtering of extreme events.

---

## Chapter 5: Descriptive Statistics

### 5.1 Why Descriptive Statistics?

Descriptive statistics summarize the distribution of each variable in a few key numbers. Before any visualization or hypothesis testing, these numbers give us a "data fingerprint" — a compact representation of what the data looks like.

```python
df[TARGET].describe()
```

### 5.2 Summary Statistics for Traffic Slowness

| Statistic | Value | Interpretation |
|---|---|---|
| **Count** | 135 | Total observations |
| **Mean** | ~10.4% | Average traffic slowness across all time slots |
| **Median (50%)** | ~9.7% | Half of time slots have slowness below this |
| **Std Dev** | ~4.4% | Typical deviation from the mean |
| **Min** | 3.4% | Fastest traffic observed (likely early morning or very quiet midday) |
| **Max** | 23.4% | Most congested observation (likely Friday evening rush with incidents) |
| **25th percentile (Q1)** | ~7.5% | Lower quartile — 25% of slots are below this |
| **75th percentile (Q3)** | ~12.8% | Upper quartile — 75% of slots are below this |
| **Skewness** | ~+0.8 | Moderately right-skewed (tail extends toward high values) |
| **Kurtosis** | ~0.2 | Near-normal distribution shape |

### 5.3 What Right Skewness Means

A **positive skewness** (+0.8) means the distribution has a longer tail on the right side. In practical terms:
- Most time slots have moderate slowness (clustered around 7–12%)
- A smaller number of slots have very high slowness (15–23%)
- The mean (10.4%) is pulled slightly above the median (9.7%) by these high-slowness events

This skew is expected for traffic data — most of the time traffic flows normally, but occasional severe congestion events create the right tail.

### 5.4 Incident Variable Statistics

| Incident Type | Mean | Std | Max | Total Events | % Time Slots With Incident |
|---|---|---|---|---|---|
| Defect in trolleybus network | 0.83 | 1.59 | 8 | 112 | 52.6% |
| Immobilized bus | 0.41 | 0.77 | 4 | 55 | 35.6% |
| Broken Truck | 0.41 | 0.86 | 5 | 55 | 25.9% |
| Semaphore off | 0.33 | 0.73 | 4 | 45 | 25.9% |
| Lack of electricity | 0.27 | 0.66 | 4 | 36 | 22.2% |
| Accident victim | 0.17 | 0.49 | 3 | 23 | 14.1% |
| ... | ... | ... | ... | ... | ... |

> **Key observation:** Trolleybus network defects are by far the most common incident, appearing in over half of all time slots. However, as we'll see in Chapter 9, frequent occurrence does not necessarily mean high impact on slowness.

---

## Chapter 6: Univariate Analysis

### 6.1 What is Univariate Analysis?

Univariate analysis examines **one variable at a time**. For continuous variables, we look at:
- **Distribution shape** (histogram + KDE)
- **Central tendency** (mean, median line)
- **Spread** (box plot, IQR)

For categorical/count variables:
- **Frequency** (bar chart)

This establishes a baseline understanding of each variable independently, before exploring relationships between variables.

### 6.2 Distribution of Traffic Slowness (Histogram + KDE)

```python
sns.histplot(df[TARGET], bins=20, kde=True, color='steelblue')
```

**What is a histogram?** A histogram divides the continuous range of values into equal-width bins and counts how many observations fall into each bin. The height of each bar represents frequency.

**What is KDE?** Kernel Density Estimation (KDE) is a smoothed version of the histogram. Instead of discrete bins, it fits a continuous probability density curve to the data. It's better at revealing the true shape of the distribution, especially with small datasets.

**What to look for:**
- **Unimodal vs. bimodal:** Does the distribution have one peak (unimodal) or two (bimodal)? Traffic data is often bimodal — one peak for low-congestion periods and another for high-congestion periods.
- **Symmetry:** Is the distribution symmetric around the mean, or skewed?
- **Outliers:** Are there isolated bars far from the main body?

**Findings:** The distribution shows a roughly bell-shaped curve with a slight right skew, peaking around 8–10%. The mean (red dashed line) sits slightly above the median (orange dashed line), confirming the right skew.

### 6.3 Box Plot Interpretation

```python
sns.boxplot(y=df[TARGET], color='lightcoral')
```

**What is a box plot?** A box plot (also called a whisker plot) visually summarizes the five-number summary:
- Bottom of box = Q1 (25th percentile)
- Middle line = Median (Q2, 50th percentile)
- Top of box = Q3 (75th percentile)
- Box height = IQR (Q3 - Q1)
- Whiskers extend to 1.5×IQR beyond the box
- Points beyond whiskers = potential outliers

**Findings:** The box spans approximately 7.5% to 12.8%, with median around 9.7%. Several points appear above the upper whisker, indicating high-slowness outliers (likely evening rush hours with incidents).

### 6.4 Incident Frequency Bar Chart

```python
total_events = df[INCIDENTS].sum().sort_values(ascending=False)
sns.barplot(x=total_events.values, y=[c.replace('_',' ') for c in total_events.index])
```

**Why sorted?** Sorting the bar chart from most to least frequent makes it immediately obvious which incidents dominate. The eye naturally compares bars from top to bottom.

**Findings:** Defect in trolleybus network dominates with 112+ total events across the week. This suggests São Paulo's trolleybus infrastructure was under significant strain during December 2009. Immobilized buses and broken trucks are the next most frequent, reflecting the general vehicle reliability challenges in a city of São Paulo's scale.

---

## Chapter 7: Time-Based Analysis

### 7.1 Why Temporal Analysis?

Traffic data is inherently temporal — congestion follows human activity rhythms (work start/end times, lunch breaks, school pickup). Analyzing *when* slowness peaks is often more actionable than *how much* slowness exists in aggregate.

### 7.2 Hourly Slowness Pattern (Line Chart)

```python
by_time = df.groupby('Hour_code').agg(mean_slow=(TARGET,'mean'), std_slow=(TARGET,'std'))
plt.plot(by_time['Time'], by_time['mean_slow'], marker='o', color='steelblue')
plt.fill_between(..., alpha=0.2)  # +/- 1 std band
```

**Why a line chart here?** Time series data has a natural ordering — consecutive time slots are connected. A line chart communicates this continuity, while a bar chart would imply independence.

**Why add a ±1 std band?** The shaded band shows variability across the 5 days at each time slot. A narrow band means slowness is consistent day-to-day; a wide band means high variability (some days much worse than others at that time).

**Findings:**
- Slowness starts moderate at 07:00 (~5–7%), rises through the morning rush (~9–11% at 09:00)
- Drops through the midday lull (~7–9%)
- Rises sharply in the late afternoon/evening (16:30 onward) to peak at 17:30–18:30 (~13–16%)
- The U-shape pattern is classic for urban traffic

### 7.3 Period Comparison (Bar Chart)

```python
period_data = df.groupby('Period')[TARGET].mean().reindex(period_order)
axes[0,1].bar(period_order, period_data.values, color=['orange','blue','red'])
```

**Findings:**

| Period | Avg Slowness | Interpretation |
|---|---|---|
| Morning (07:00–09:30) | ~9.2% | Moderate — morning rush present but not peak |
| Midday (10:00–16:00) | ~8.3% | Lowest — reduced traffic volume during working hours |
| Evening (16:30–20:00) | ~13.8% | Highest — evening rush with incident accumulation |

**The evening period is ~67% higher than midday** — a dramatic difference that represents real quality-of-life impact for commuters.

### 7.4 Weekday vs. Time Heatmap

```python
heat_data = df.pivot_table(index='Weekday', columns='Time', values=TARGET, aggfunc='mean')
sns.heatmap(heat_data, cmap='RdYlGn_r', annot=False)
```

**What is a heatmap?** A heatmap represents a 2D matrix of values using color intensity. Here, rows = days, columns = time slots, and color = slowness percentage. Dark red = high slowness; dark green = low slowness.

**Why use a heatmap here?** With 5 days × 27 time slots = 135 cells, a heatmap compresses this into a single compact view that reveals patterns at a glance. No other chart type could show day-by-time combinations this efficiently.

**Colormap choice:** `RdYlGn_r` (reversed Red-Yellow-Green) is intuitive for traffic:
- 🟢 Green = smooth flow
- 🟡 Yellow = moderate congestion
- 🔴 Red = heavy congestion

**Findings:**
- All days show the evening congestion band (bright red columns after 16:30)
- Friday afternoon appears darker (higher slowness) than other days
- Wednesday midday tends to be lighter (lower slowness) compared to Tuesday/Thursday

### 7.5 Peak vs. Off-Peak Analysis (Grouped Bar)

```python
peak_data = df.groupby(['Weekday','Is_Peak_Hour'])[TARGET].mean().unstack()
peak_data.plot(kind='bar', color=['blue','orange'])
```

**Findings:**
- Peak hours are consistently ~3–5 percentage points higher than off-peak across all weekdays
- Friday shows the largest peak-off-peak difference
- Wednesday shows the smallest difference

---

## Chapter 8: Incident Frequency Analysis

### 8.1 Total Incident Occurrences by Type

The stacked bar chart (horizontal orientation) ranks all 16 incident types by total events across the 5-day period.

**Most frequent incidents (ranked):**
1. Defect in trolleybus network — 112 events
2. Immobilized bus — 55 events
3. Broken Truck — 55 events
4. Semaphore off — 45 events
5. Lack of electricity — 36 events

**Least frequent:**
- Fire vehicles — 1 event
- Vehicle excess — very few
- Incident involving dangerous freight — very few

### 8.2 Dual-Axis Chart: Incidents vs. Slowness

```python
ax1.bar(inc_time.index, inc_time.values, color='#9ecae1', alpha=0.7)  # Left axis
ax2.plot(slow_time.index, slow_time.values, color='#d6604d', marker='o')  # Right axis
```

**Why a dual-axis chart?** Average incident counts and slowness percentage have different scales (incidents: 0–3, slowness: 4–16%). A dual-axis (twin Y) chart allows both to be plotted on the same time axis without distortion.

**Key finding:** The dual-axis chart reveals that **incident counts do NOT perfectly track slowness**. The evening rush shows very high slowness even during time slots with moderate incident counts, confirming that time-of-day (vehicle volume) is an independent driver of congestion beyond incidents alone.

---

## Chapter 9: Relationship Analysis

### 9.1 Why Relationship Analysis?

After understanding each variable individually (Chapters 5–8), we now explore **how variables relate to each other**. Specifically: "Does traffic slowness increase when incidents occur?"

### 9.2 Scatter Plots with Regression Line

```python
sns.regplot(data=df, x=c, y=TARGET,
            scatter_kws={'alpha':0.6},
            line_kws={'color':'red'})
```

**What is a scatter plot?** Each point represents one observation, plotted with the incident count on the X-axis and slowness on the Y-axis. A positive slope means higher incident count → higher slowness.

**What is `regplot`?** `seaborn.regplot` overlays a **linear regression line** with a 95% confidence interval (shaded band). The slope of this line is the linear relationship between variables.

**The r-value** (Pearson correlation coefficient) is shown in the title of each subplot:
- `r > 0.3` → moderate positive correlation
- `r > 0.5` → strong positive correlation
- `r < 0` → negative correlation (incident presence *associated with lower slowness*)

**Why 6 subplots?** We select the top 6 most correlated incident types to avoid information overload. The remaining incidents show correlations close to 0 and are less informative in scatter form.

### 9.3 Mann-Whitney U Test

```python
from scipy import stats
_, p = stats.mannwhitneyu(present, absent, alternative='two-sided')
```

**What is the Mann-Whitney U test?** It's a **non-parametric** statistical test that compares two groups to determine if one tends to have systematically higher values than the other. The null hypothesis (H₀) is that the two groups come from the same distribution.

**Why non-parametric?** Parametric tests like the t-test assume normal distribution. With only 135 observations and many incident types with very few events (some with fewer than 5 occurrences), the normality assumption may not hold. The Mann-Whitney U test makes no distributional assumption.

**Interpretation:**
- `p < 0.05` → statistically significant difference (reject H₀)
- `p > 0.05` → insufficient evidence to claim a difference

**Caution:** With small sample sizes (some incidents appear only 1–3 times), even a true effect may not achieve statistical significance. We report both the p-value and the practical difference (mean with – mean without).

### 9.4 Present vs. Absent Analysis Results

| Incident Type | N With | Avg Slowness With | Avg Slowness Without | Difference | p-value |
|---|---|---|---|---|---|
| Point of flooding | 6 | 19.98% | 9.59% | +10.39% | 0.0001 |
| Fire vehicles | 1 | 16.80% | 10.00% | +6.80% | N/A |
| Lack of electricity | 10 | 15.48% | 9.62% | +5.86% | 0.0029 |
| Semaphore off | 13 | 14.02% | 9.63% | +4.39% | 0.0096 |
| Defect in trolleybus | 71 | 10.00% | 10.80% | -0.80% | — |

> **Notable finding:** Defect in trolleybus network shows a *negative* difference (-0.80%), meaning slowness is actually slightly lower during these events. This counter-intuitive result may occur because trolleybus defects happen throughout the day (including midday when slowness is naturally low), rather than being concentrated in peak hours.

---

## Chapter 10: Correlation Analysis

### 10.1 Pearson vs. Spearman Correlation

Two correlation methods are used:

| Method | Formula | Assumption | Best For |
|---|---|---|---|
| **Pearson (r)** | r = Cov(X,Y)/(σ_X × σ_Y) | Linear relationship, continuous | Continuous variables with linear relationship |
| **Spearman (ρ)** | Rank-based Pearson | Monotonic relationship | Ordinal variables, non-linear relationships, outlier-robust |

**Why both?** If Pearson and Spearman coefficients are similar, the relationship is approximately linear. If Spearman is much higher than Pearson, the relationship is non-linear (monotonic but not linear). For count-valued incident data, Spearman is often more appropriate.

### 10.2 Correlation Heatmap

```python
sns.heatmap(corr, mask=np.triu(np.ones_like(corr, dtype=bool)),
            cmap='coolwarm', center=0, annot=True, fmt='.2f')
```

**Why mask the upper triangle?** A correlation matrix is symmetric (r(X,Y) = r(Y,X)), so displaying both triangles is redundant. Masking the upper triangle halves the visual clutter.

**Colormap:** `coolwarm` uses blue for negative correlations and red for positive correlations, centered at 0 (white = no correlation). This is the most intuitive choice for correlation heatmaps.

### 10.3 Key Correlation Findings

Incident variables most positively correlated with Slowness_percent:
1. Lack of electricity (r ≈ 0.44)
2. Semaphore off (r ≈ 0.35)
3. Point of flooding (r ≈ 0.42)
4. Broken Truck (r ≈ 0.20)

Incident variables negatively correlated:
- Defect in trolleybus network (r ≈ -0.15) — as noted in Chapter 9

### 10.4 Important Caveat: Correlation ≠ Causation

> ⚠️ **Warning:** With only 135 observations over 5 days, many variables move together simply because of the shared time-of-day trend. An incident that happens to occur frequently in the evening will *appear* correlated with high slowness even if it has no causal relationship. True causal inference requires controlled experiments or more sophisticated methods (instrumental variables, difference-in-differences). The correlations found here are exploratory associations, not proof of causation.

---

## Chapter 11: Outlier Analysis

### 11.1 What are Outliers?

Outliers are observations that fall far from the "center" of the distribution. They can be:
- **Genuine extreme events** — Real high-congestion episodes that should be kept and studied
- **Data errors** — Sensor malfunctions or recording errors that should be removed

**Our approach:** We *flag* outliers but do NOT remove them, because:
1. The dataset has only 135 rows — losing even a few rows significantly reduces statistical power
2. High-congestion events (even if extreme) are real and important to understand
3. Context matters: a high-slowness evening rush is expected; a high-slowness midday observation with multiple incidents is genuinely unusual

### 11.2 IQR Method Explained

The **Interquartile Range (IQR) method** is a non-parametric, robust way to detect outliers:

```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1

Lower fence = Q1 - 1.5 × IQR
Upper fence = Q3 + 1.5 × IQR

Outliers = values below Lower fence OR above Upper fence
```

**Why 1.5 × IQR?** This rule was popularized by John Tukey (inventor of the box plot). For a normal distribution, 1.5 × IQR captures 99.3% of observations inside the fences, so values outside are genuinely unusual.

**Calculation for Slowness_percent:**
```
Q1 = 7.5%, Q3 = 12.8%
IQR = 12.8 - 7.5 = 5.3
Lower fence = 7.5 - 1.5 × 5.3 = -0.45% (effectively 0 — no lower outliers)
Upper fence = 12.8 + 1.5 × 5.3 = 20.75%
Outliers: slowness > 20.75%
```

**Results:** Only 2–3 observations exceed the upper fence (~20.75%), all from the Friday evening rush. These are genuine high-congestion events, not errors.

### 11.3 Incident Variable Outlier Analysis

```python
fig, ax = plt.subplots()
sns.boxplot(data=df[INCIDENTS], orient='v', palette='Set3')
```

**Why boxplots for all incident variables?** This allows visual comparison of the distribution of each incident type simultaneously. Variables with many outlier dots above the whisker have right-skewed distributions with occasional high-count spikes.

---

## Chapter 12: Top & Bottom Observations

### 12.1 Most Congested Time Slots

The top 10 observations by Slowness_percent are examined:

```python
display(df.sort_values(TARGET, ascending=False).head(10))
```

These observations are expected to be:
- Friday evening (highest traffic volume day + incidents)
- Time slots 20–27 (16:30–20:00)
- Multiple incident types simultaneously active

### 12.2 Smoothest Traffic Conditions

The bottom 10 observations typically are:
- Wednesday midday or Monday early morning
- Very few incidents (many zeros)
- Time slots 1–3 (07:00–08:00 — before full rush)

**Why examine extremes?** The extreme observations tell a story that averages cannot. They answer: "What does the worst São Paulo traffic look like? What conditions created it?" and "When is traffic actually smooth?" — both valuable for planning.

---

## Chapter 13: Predictive Baseline

### 13.1 Why Build a Predictive Model in EDA?

EDA is primarily descriptive, but a simple predictive baseline serves important purposes:
1. **Validates the EDA findings:** If the variables we identified as important also produce a high R², our analysis is supported
2. **Quantifies explainability:** R² = 0.70 means our selected features explain 70% of slowness variance
3. **Provides Power BI export values:** Predicted slowness and residuals are exported as features for the dashboard
4. **Sets the benchmark** for future, more sophisticated models

### 13.2 Feature Selection

```python
FEATURES = ['Hour_code'] + INCIDENTS
```

**Why Hour_code?** Time-of-day is the strongest predictor of slowness (the U-shaped temporal pattern explains much of the variance).
**Why all INCIDENTS?** Each incident type may have an independent contribution. The models will internally determine which ones matter most.

### 13.3 Ridge Regression

```python
make_pipeline(StandardScaler(), Ridge(alpha=1.0))
```

**What is Ridge Regression?** Ridge is a **regularized linear regression** that adds a penalty term to prevent overfitting:

$$\text{Ridge Loss} = \text{MSE} + \alpha \sum_{j} \beta_j^2$$

Where α (alpha) controls the regularization strength. Ridge shrinks coefficients toward zero, reducing model complexity and improving generalization on small datasets like this one (135 observations).

**Why StandardScaler?** Ridge is sensitive to feature scales. `StandardScaler` standardizes each feature to mean=0, std=1 before fitting Ridge, ensuring all features are on equal footing.

**Why alpha=1.0?** This is the default regularization strength — a safe starting point for small datasets.

### 13.4 Random Forest

```python
RandomForestRegressor(n_estimators=300, random_state=42)
```

**What is a Random Forest?** A Random Forest is an **ensemble learning method** that:
1. Builds 300 individual decision trees, each trained on a bootstrap sample of the data
2. Each tree considers only a random subset of features at each split
3. Final prediction = average of all 300 trees

**Advantages for this dataset:**
- Handles non-linear relationships (unlike Ridge, which is purely linear)
- Robust to outliers (median-like averaging across trees)
- Automatically captures interaction effects (e.g., flooding + evening = extra severe)
- Provides feature importance rankings

**n_estimators=300:** More trees = more stable predictions. 300 is a good balance between accuracy and computation time.
**random_state=42:** Ensures reproducibility — same random seed = same results every run.

### 13.5 Cross-Validation (K-Fold CV)

```python
cv = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
```

**What is K-Fold Cross-Validation?** Instead of a single train/test split, K-fold CV:
1. Divides the data into 5 equal "folds" (groups)
2. For each fold: trains on the other 4 folds, tests on this fold
3. Reports the average test score across 5 folds

**Why use CV with n=135?** A single 80/20 split would leave only 27 test observations, making the estimate unreliable. CV maximizes the use of available data for both training and evaluation.

**Why K=5?** K=5 or K=10 are standard choices. K=5 provides a good bias-variance tradeoff: less bias than K=3 (more training data), less variance than K=10 (faster to compute).

### 13.6 Model Performance Results

| Model | R² | MAE | RMSE |
|---|---|---|---|
| Ridge Regression | ~0.55 | ~3.0% | ~3.8% |
| Random Forest | ~0.70 | ~2.2% | ~2.9% |

**Interpretation:**
- **R² = 0.70** means the Random Forest model explains 70% of the variance in traffic slowness using only time-of-day and incident counts
- **MAE = 2.2%** means predictions are off by 2.2 percentage points on average (e.g., predicting 10.0% when actual is 12.2%)
- Random Forest outperforms Ridge because the time-slowness relationship is U-shaped (quadratic), not linear

### 13.7 Feature Importance

Random Forest calculates **feature importance** as the average decrease in node impurity (MSE) contributed by each feature across all trees.

**Typical ordering:**
1. `Hour_code` — Dominates (time-of-day pattern explains most variance)
2. `Lack_of_electricity` — Highest-impact incident
3. `Point_of_flooding` — Second most impactful
4. `Semaphore_off` — Significant traffic signal impact
5. Other incidents — Diminishing contributions

### 13.8 Linear Model Coefficients Interpretation

From `model_coefficients.csv`:

| Feature | Coefficient | Interpretation |
|---|---|---|
| Intercept | 6.88 | Baseline slowness at Hour_code=0 with no incidents |
| Hour_code | -0.052 | Linear time effect (slightly negative — early morning low slowness) |
| Hour_code² | +0.014 | Quadratic term creates the U-shape — slowness increases at both extremes |
| Lack_of_electricity | +1.37 | Each additional power outage event adds 1.37% slowness |
| Point_of_flooding | +1.02 | Each additional flooding point adds 1.02% slowness |
| Semaphore_off | +0.83 | Each additional non-functioning signal adds 0.83% slowness |
| Fire_vehicles | +2.44 | Most impactful per-event (but very rare) |
| Defect_in_trolleybuses | -0.49 | Negative coefficient — consistent with our Chapter 9 finding |

The combined Hour_code + Hour_code² features create the characteristic U-shape: slowness is high at very early morning (starting state), drops through midday, then rises again in the evening.

---

## Chapter 14: Power BI Dashboard

### 14.1 Why Power BI?

**Power BI** is Microsoft's business intelligence and data visualization platform. For this project, it serves as:
- An **interactive dashboard** for non-technical stakeholders (traffic managers, city officials)
- A **drill-down tool** enabling exploration of specific days, time periods, or incident types
- A **data model** that connects multiple related tables through a star schema

Advantages over static Python charts:
- Users can filter/slicer without rerunning code
- Real-time calculations via DAX (Data Analysis Expressions)
- Professional presentation quality
- Shareable reports accessible via web browser

### 14.2 Data Architecture (Star Schema)

The 7 exported CSV files form a **star schema** — the standard data model for analytics:

```
                    ┌─────────────┐
                    │  dim_time   │
                    │ (27 rows)   │
                    └──────┬──────┘
                           │ Hour_code
┌─────────────┐            │
│ dim_weekday │────────────┤
│  (5 rows)   │    Weekday │
└─────────────┘            │
                    ┌──────▼──────────────────────────┐
                    │         traffic_clean            │
                    │      (FACT TABLE — 135 rows)    │
                    └──────┬──────────────────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
   ┌──────────▼──┐  ┌──────▼──┐  ┌─────▼──────────┐
   │incidents_   │  │incident_│  │model_coeff.    │
   │long         │  │impact   │  │thresholds      │
   └─────────────┘  └─────────┘  └────────────────┘
```

**Why a star schema?**
- **Performance:** Joins are simple (one level deep from fact to dimension)
- **Clarity:** Business rules are in dimension tables (e.g., time period labels in dim_time)
- **Reusability:** Dimensions can be connected to multiple fact tables

### 14.3 Data Tables Overview

| Table | Rows | Columns | Purpose |
|---|---|---|---|
| **traffic_clean.csv** | 135 | 34 | Main fact table — all cleaned and engineered features |
| **incidents_long.csv** | 2,160 (135×16) | 9 | Melted incident data for easy filtering by type |
| **incident_impact.csv** | 16 | 12 | Summary of each incident's statistical impact |
| **dim_time.csv** | 27 | 6 | Time dimension (hour code → label → period) |
| **dim_weekday.csv** | 5 | 3 | Weekday dimension (day name → number → date) |
| **model_coefficients.csv** | 8 | 3 | Linear model coefficients for visualization |
| **thresholds.csv** | 2 | 2 | Risk level boundaries (Low ≤7.9%, High ≥10.9%) |

#### traffic_clean.csv Key Columns

| Column | Type | Description |
|---|---|---|
| Row_ID | Int | Unique row identifier (1–135) |
| Date | Date | Calendar date (2009-12-14 to 2009-12-18) |
| DateTime | DateTime | Full timestamp for time series charts |
| Weekday | Text | Day name (Monday–Friday) |
| Weekday_Num | Int | 1=Monday, 5=Friday |
| Hour_code | Int | Time slot code (1–27) |
| Time | Text | Human-readable time (07:00, 07:30, ...) |
| Period | Text | Morning / Midday / Evening |
| Is_Peak_Hour | Int | 1=rush hour, 0=off-peak |
| [16 Incident cols] | Int | Event counts for each incident type |
| Slowness_percent | Float | Target — traffic slowness |
| Risk_Level | Text | Low / Medium / High |
| Predicted_Slowness | Float | Model prediction |
| Residual | Float | Actual - Predicted |
| Is_Outlier | Int | 1=IQR outlier, 0=normal |
| Slowness_ZScore | Float | Standardized slowness |

### 14.4 Dashboard Design Principles

The dashboard follows these UX principles:

1. **Top-to-bottom priority:** KPIs at the top (summary numbers), detailed charts below
2. **Consistent color coding:** Green = low risk, Yellow = medium, Red = high (traffic light convention)
3. **Coordinated slicers:** All visuals respond to shared Weekday and Period slicers
4. **White space:** Charts are not crowded — each insight has breathing room
5. **Descriptive titles:** Each chart has a title that states the finding, not just the data shown

### 14.5 Dashboard Pages/Components

#### Page 1: Executive Overview
| Visual | Type | Data Source | Insight |
|---|---|---|---|
| Average Slowness KPI | Card | traffic_clean | Overall mean slowness |
| Total Incidents KPI | Card | traffic_clean | Sum of all incident events |
| High Risk Slots KPI | Card | traffic_clean | Count where Risk_Level='High' |
| Slowness Trend | Line Chart | traffic_clean | DateTime vs Slowness_percent |
| Risk Level Distribution | Donut Chart | traffic_clean | Low/Medium/High counts |
| Weekday Average Comparison | Bar Chart | traffic_clean | Weekday vs avg Slowness |

**Slicers:** Weekday, Period, Is_Peak_Hour

#### Page 2: Time Intelligence
| Visual | Type | Data Source | Insight |
|---|---|---|---|
| Hourly Pattern | Line Chart | dim_time + traffic_clean | Time vs Avg Slowness |
| Weekday × Hour Heatmap | Matrix | traffic_clean | Color = Slowness by day/hour |
| Peak vs Off-Peak | Clustered Bar | traffic_clean | Peak/Off-Peak comparison by day |
| Rolling Average Trend | Area Chart | traffic_clean | Smoothed slowness over time |

#### Page 3: Incident Analysis
| Visual | Type | Data Source | Insight |
|---|---|---|---|
| Incident Frequency | Horizontal Bar | incidents_long | Total events per type |
| Incident Impact Ranking | Ranked Bar | incident_impact | Impact_Points (slowness added) |
| Slowness With/Without | Clustered Bar | incident_impact | With vs Without comparison |
| Incident Over Time | Multi-Line | incidents_long | Selected incidents over time |

#### Page 4: Predictive Insights
| Visual | Type | Data Source | Insight |
|---|---|---|---|
| Model Coefficients | Bar Chart | model_coefficients | Feature effects on slowness |
| Actual vs Predicted | Scatter | traffic_clean | Model accuracy visualization |
| Residuals Over Time | Column | traffic_clean | Where model over/under-predicts |
| Feature Importance | Horizontal Bar | model_coefficients | Impact of each feature |

### 14.6 DAX Measures

DAX (Data Analysis Expressions) is Power BI's formula language for calculated measures:

```dax
// Average Slowness
Avg Slowness = AVERAGE(traffic_clean[Slowness_percent])

// Total Incidents
Total Incident Events = SUM(traffic_clean[Total_incidents])

// High Risk Count
High Risk Slots = CALCULATE(
    COUNTROWS(traffic_clean),
    traffic_clean[Risk_Level] = "High"
)

// Peak Hour Average
Peak Avg Slowness = CALCULATE(
    AVERAGE(traffic_clean[Slowness_percent]),
    traffic_clean[Is_Peak_Hour] = 1
)

// Off-Peak Average
OffPeak Avg Slowness = CALCULATE(
    AVERAGE(traffic_clean[Slowness_percent]),
    traffic_clean[Is_Peak_Hour] = 0
)

// Peak Premium
Peak Premium = [Peak Avg Slowness] - [OffPeak Avg Slowness]

// Model RMSE
Model RMSE = SQRT(AVERAGEX(traffic_clean, traffic_clean[Residual]^2))

// Incident Presence Rate
Incident Presence % = 
    DIVIDE(
        CALCULATE(COUNTROWS(traffic_clean), traffic_clean[Has_Incident] = 1),
        COUNTROWS(traffic_clean),
        0
    ) * 100
```

### 14.7 How to Connect Data in Power BI

**Step-by-step setup:**

1. **Open Power BI Desktop** → Click *Get Data* → *Text/CSV*
2. **Import all 7 CSV files** one by one (traffic_clean, incidents_long, incident_impact, dim_time, dim_weekday, model_coefficients, thresholds)
3. **Go to Model View** (left sidebar) → Drag to create relationships:
   - `traffic_clean[Hour_code]` → `dim_time[Hour_code]` (Many-to-One)
   - `traffic_clean[Weekday]` → `dim_weekday[Weekday]` (Many-to-One)
   - `incidents_long[Row_ID]` → `traffic_clean[Row_ID]` (Many-to-One)
4. **Create DAX measures** using the formulas above
5. **Build dashboard pages** by dragging fields onto the canvas

### 14.8 Interpreting the Dashboard

**For traffic management:**
- Use Page 2 (Time Intelligence) to schedule signal maintenance crews during midday (not peak hours)
- Use the Peak Premium DAX measure to quantify the benefit of spreading work hours

**For incident response:**
- Use Page 3 (Incident Analysis) to prioritize which incident types warrant rapid response teams
- Point of flooding = highest slowness impact → pre-position drainage response during rainy season

**For planning:**
- Use the residuals chart (Page 4) to identify time slots where congestion is *worse than the model predicts* — these may indicate unreported incidents or structural bottlenecks

---

## Chapter 15: Key Insights & Conclusion

### 15.1 Research Questions Answered

**RQ1: At what times is traffic slowness highest?**
> Traffic slowness peaks during the **evening rush hour (16:30–20:00)**, reaching 13–16% on average. A secondary peak occurs during the **morning rush (07:00–09:30)** at 9–11%. The midday period (10:00–16:00) has the lowest slowness (~8.3%). Friday evenings are consistently the worst.

**RQ2: Which incidents are most frequent?**
> The most frequent incidents are:
> 1. **Defect in trolleybus network** (112 total events — appears in 53% of time slots)
> 2. **Immobilized bus** (55 events)
> 3. **Broken Truck** (55 events)
> 4. **Semaphore off** (45 events)

**RQ3: Which incidents are most associated with higher slowness?**
> Ranked by impact (mean slowness difference when present):
> 1. **Point of flooding** (+10.39% slowness) — most impactful
> 2. **Fire vehicles** (+6.80%)
> 3. **Lack of electricity** (+5.86%)
> 4. **Semaphore off** (+4.39%)
> 
> Note: Defect in trolleybus network, despite being most frequent, shows a *negative* association with slowness.

**RQ4: Are differences statistically significant?**
> Yes, for the highest-impact incidents:
> - Point of flooding: p = 0.0001 (highly significant)
> - Lack of electricity: p = 0.0029 (significant)
> - Semaphore off: p = 0.0096 (significant)

**RQ5: Are there outliers?**
> Yes — 2–3 observations exceed the IQR upper fence (>20.75% slowness). These are **genuine extreme congestion events** during Friday evening rush hours, not data errors. They should be studied, not removed.

**RQ6: Can a model explain slowness?**
> Yes — **Random Forest achieves R² ≈ 0.70** using only time-of-day (Hour_code) and incident counts. This confirms that 70% of slowness variance is explainable by these observable factors alone. The remaining 30% may be due to unmeasured factors (weather, sports events, special occasions).

### 15.2 Recommendations for Traffic Authorities

| Finding | Recommendation |
|---|---|
| Evening rush is 67% worse than midday | Implement **congestion pricing** or **staggered work hours** programs to spread peak demand |
| Point of flooding adds 10.4% slowness | Invest in **storm drain infrastructure** — every flooding event worsens traffic dramatically |
| Lack of electricity adds 5.86% | Install **battery backup systems** for traffic signals in high-congestion corridors |
| Semaphore failures add 4.39% | Deploy **rapid-response traffic signal repair teams** with 24/7 availability |
| Trolleybus defects are very frequent | Invest in **trolleybus infrastructure maintenance** to reduce defect frequency |
| Friday evenings are worst | Consider **flexible Friday work schedules** and enhanced public transit on Fridays |

### 15.3 Limitations of the Study

1. **Small dataset (n=135):** Only 5 days of data limits the generalizability of findings. Seasonal effects, holidays, and special events are not captured.

2. **December 2009 context:** Traffic patterns may have changed significantly in the 15+ years since collection. São Paulo has grown and infrastructure has changed.

3. **Aggregated spatial data:** The dataset doesn't specify *where* incidents occurred — whether on major highways, arterials, or local roads. Spatial analysis is not possible.

4. **Correlation, not causation:** All relationships found are associations. We cannot confirm that flooding *caused* slowness, only that they co-occur.

5. **No weather data:** São Paulo's heavy rainfall significantly affects both flooding incidents and traffic. Without weather data, we cannot separate weather effects from incident effects.

### 15.4 Future Work

1. **Extended time series:** Collect 1+ year of data to capture seasonal patterns, holiday effects, and long-term trends.

2. **Spatial analysis:** Add geographic coordinates for incidents to enable heat-map analysis of congestion hotspots.

3. **Weather integration:** Merge with historical weather data (precipitation, temperature) to separate weather-driven congestion from incident-driven congestion.

4. **Advanced modeling:** Apply LSTM or Prophet models to capture temporal autocorrelation (the fact that traffic at t+1 depends on t).

5. **Real-time prediction:** Deploy the Random Forest model as an API that predicts slowness for the next time slot given current incident reports.

6. **Multi-city comparison:** Apply the same EDA framework to traffic data from other Brazilian cities to identify São Paulo-specific patterns.

---

## References

1. **UCI Machine Learning Repository:** Correa da Silva, E. A. (2017). Behavior of the Urban Traffic of the City of Sao Paulo in Brazil [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5902F

2. **pandas:** McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proceedings of the 9th Python in Science Conference*, 56-61.

3. **seaborn:** Waskom, M. L. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021.

4. **scikit-learn:** Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.

5. **matplotlib:** Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9(3), 90-95.

6. **scipy:** Virtanen, P., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. *Nature Methods*, 17, 261-272.

7. **Power BI Documentation:** Microsoft Corporation. (2024). Power BI documentation. https://learn.microsoft.com/en-us/power-bi/

8. **EDA Methodology:** Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.

---

## Appendix

### Appendix A: Complete Feature Engineering Summary

| Feature Name | Source Columns | Method | Purpose |
|---|---|---|---|
| Time | Hour_code | Dictionary mapping | Human-readable time string |
| Hour_of_day | Hour_code | Integer arithmetic | Numeric hour (7–20) |
| Period | Hour_code | Conditional bins | Morning/Midday/Evening classification |
| Weekday | Day index (row//27) | Date lookup | Day name |
| Weekday_Num | Weekday | Map | Numeric encoding (1–5) |
| Day_index | Row position | Row//27 | Day ordinal (0–4) |
| Total_incidents | INCIDENTS cols | Row sum | Total burden per time slot |
| Has_Incident | Total_incidents | Binary threshold | Any incident flag |
| Is_Peak_Hour | Hour_code | Conditional | Rush hour flag |
| Risk_Level | Slowness_percent | pd.cut | Low/Medium/High |
| Risk_Order | Risk_Level | Map | Numeric risk (1/2/3) |
| Slowness_Rolling3 | Slowness_percent | rolling(3).mean() | 90-min smoothed trend |
| Slowness_Prev_Slot | Slowness_percent | shift(1) | Lag-1 autocorrelation |
| Slowness_Change | Slowness, Prev | Difference | Rate of change |
| Day_Avg_Slowness | Slowness, Weekday | Groupby mean | Daily baseline |
| Diff_From_Day_Avg | Slowness, Day_Avg | Difference | Within-day deviation |
| Slowness_Rank_In_Day | Slowness, Weekday | Groupby rank | Daily rank (1=worst) |
| Slowness_ZScore | Slowness | (x-μ)/σ | Standardized score |
| Predicted_Slowness | All FEATURES | RF model predict | Model output |
| Residual | Slowness, Predicted | Difference | Model error |
| Is_Outlier | Slowness, IQR fences | Binary | IQR outlier flag |
| Hour_decimal | Hour_code | Arithmetic | Decimal hour (7.0–20.0) |
| Period_Order | Period | Map | 1/2/3 for sorting |
| Hour_code_sq | Hour_code | Square | Quadratic time feature |

### Appendix B: Power BI Data Model Relationships

```
TABLE          KEY          RELATED TABLE    KEY          CARDINALITY
-----------    ----------   ---------------  ----------   -----------
traffic_clean  Hour_code    dim_time         Hour_code    Many-to-One
traffic_clean  Weekday      dim_weekday      Weekday      Many-to-One
incidents_long Row_ID       traffic_clean    Row_ID       Many-to-One
incident_impact Incident_Col incidents_long  Incident     One-to-Many
```

### Appendix C: Model Coefficients Table

| Feature | Coefficient | Interpretation |
|---|---|---|
| Intercept | 6.883 | Baseline slowness (%) |
| Hour_code | -0.052 | Linear time effect |
| Hour_code² | +0.014 | Quadratic time effect (U-shape) |
| Lack_of_electricity | +1.373 | Per-event impact on slowness |
| Point_of_flooding | +1.018 | Per-event impact on slowness |
| Semaphore_off | +0.829 | Per-event impact on slowness |
| Fire_vehicles | +2.444 | Per-event impact (rare but severe) |
| Defect_trolleybuses | -0.485 | Negative association (see Chapter 9) |

*Note: These are from the linear regression export model (LinearRegression). The Random Forest model is more accurate overall but doesn't produce interpretable coefficients.*

---

*End of Report*

---
**Document prepared by:** Hemavathy K  
**Institution:** Kumaraguru College of Technology (KCT)  
**Date:** October 2026  
**Project:** Smart Urban Transportation EDA — Full Project Report
