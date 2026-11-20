# Banking Transaction Pattern Analysis (Project 10)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Lakshya-Pundhir/HCL-traning-project/blob/main/banking_transaction_pattern_analysis.ipynb)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **HCL Training Project 10 — FinTech Analytics & Transaction Pattern Exploration**  
> **Author:** Lakshya Pundhir  
> **Specification:** Software Requirements Specification (SRS) Version 1.0 (19 November 2026)  
> **Dataset:** `10_bank_transactions.csv` (1,000 synthetic transaction records)

---

## 📌 Executive Summary

Modern retail banking institutions process millions of financial interactions daily across diverse payment networks, user accounts, and physical geographies. Understanding operational distributions, channel capacity loads, transaction velocity, and anomaly fences is essential for ensuring liquidity management, infrastructural resilience, and data integrity.

This repository implements **Project 10: Banking Transaction Pattern Analysis** in accordance with the formal **Software Requirements Specification (SRS)**. The analytical pipeline ingests raw banking records, cleans and standardizes columns, handles missing amounts via median imputation, deduplicates transaction IDs, analyzes descriptive statistics and net financial flows, detects statistical outliers via the Interquartile Range (IQR) rule, evaluates high-value transactions above the 90th percentile using NumPy Boolean indexing, and articulates **five cautious operational observations and recommendations**.

---

## ⚠️ Important Ethical & Data Governance Disclaimer

> **Critical Notice:** The dataset analyzed in this project is **entirely synthetic**. The `Flagged` column represents an arbitrary, supplied label and is **not proof or verdict of fraud or illicit activity**. In strict accordance with **NFR-06 (Ethical Use)** and **Section 3.2 of the SRS**, no output or observation from this project may be interpreted, claimed, or utilized to imply illegal conduct, financial culpability, or customer intent. All findings are purely descriptive and aimed at operational resource planning and data-quality assurance.

---

## 📋 Software Requirements Specification (SRS) Traceability

Every functional requirement (FR-01 through FR-15) and non-functional attribute (NFR-01 through NFR-08) specified in [docs/SRS.md](docs/SRS.md) has been implemented and validated:

| Requirement ID | Requirement Description | Implementation Method | Status |
| :--- | :--- | :--- | :---: |
| **FR-01** | Load CSV, display shape `(1000, 9)`, column names, data types, head, info | `pd.read_csv()`, `.info()`, `.head()` | ✅ Complete |
| **FR-02** | Detect missing `Transaction_Amount` (30 rows), impute using median (`3581.51`) | `.isna().sum()`, `.fillna()` | ✅ Complete |
| **FR-03** | Detect duplicate `Transaction_ID` (5 IDs / 10 rows), keep first occurrence (995 left) | `.duplicated()`, Boolean mask | ✅ Complete |
| **FR-04** | Calculate total credits (₹4,544,679.75), debits (₹5,589,877.03), and net flow (-₹1,045,197.28) | `.groupby('Transaction_Type')` | ✅ Complete |
| **FR-05** | Calculate mean (₹10,185.48), median (₹3,581.51), and standard deviation (₹41,539.33) | `.mean()`, `.median()`, `.std()` | ✅ Complete |
| **FR-06** | Analyze transaction volume, total value, and average value by channel | `groupby('Channel')` aggregated | ✅ Complete |
| **FR-07** | Compare total transaction value by city | `groupby('City')['Amount_Abs'].sum()` | ✅ Complete |
| **FR-08** | Calculate flagged count (44) and percentage (4.42% of 995 valid records) | `.sum()`, `(flagged / valid) * 100` | ✅ Complete |
| **FR-09** | Compare flagged percentage distribution across channels | Channel group flag rate calculation | ✅ Complete |
| **FR-10** | Extract and rank the 10 largest transactions by value | `.nlargest(10, 'Amount_Abs')` | ✅ Complete |
| **FR-11** | Group credit and debit totals across account types (Business, Current, Salary, Savings) | Cross-tabulation / unstack summary | ✅ Complete |
| **FR-12** | IQR outlier detection ($Q_1 = 1976.91$, $Q_3 = 6252.06$, $\text{IQR} = 4275.15$, 91 outliers) | `np.percentile([25, 75])` & fences | ✅ Complete |
| **FR-13** | Segment records into 4 amount bands (Low, Medium, High, Very High) | Quartile segmentation (`pd.cut` / `np.select`) | ✅ Complete |
| **FR-14** | Boolean indexing threshold filter (90th percentile = ₹11,746.19, 100 transactions) | `arr[arr > threshold]` | ✅ Complete |
| **FR-15** | Deliver 5 cautious operational observations and recommendations (Section 3.2 rules) | Documented operational findings | ✅ Complete |

---

## 📊 Summary of Key Findings & Metrics

### 1. Overall Financial Flow & Transaction Statistics
- **Total Valid Records:** 995 (after removing 5 duplicate occurrences)
- **Total Credits:** ₹4,544,679.75
- **Total Debits:** ₹5,589,877.03
- **Net Flow:** -₹1,045,197.28 (Debit outflow exceeds credit inflow)
- **Mean Amount:** ₹10,185.48
- **Median Amount:** ₹3,581.51
- **Standard Deviation:** ₹41,539.33  
  *(Note: The heavy positive skew between the mean of ₹10,185 and median of ₹3,581 illustrates the strong influence of a small subset of high-value transactions).*

---

### 2. Transaction Channel Breakdown

| Channel | Transaction Count | Volume Share | Total Value (₹) | Average Value (₹) | Flagged Count | Flagged Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **UPI** | **311** | **31.26%** | 3,149,922.11 | 10,128.37 | 13 | 4.18% |
| **Mobile App** | 197 | 19.80% | 2,573,568.89 | 13,063.80 | 9 | 4.57% |
| **Net Banking** | 155 | 15.58% | 1,010,033.29 | 6,516.34 | 10 | **6.45%** |
| **POS** | 149 | 14.97% | 1,141,050.90 | 7,658.06 | 4 | 2.68% |
| **ATM** | 105 | 10.55% | 750,679.70 | 7,149.33 | 4 | 3.81% |
| **Branch** | 78 | 7.84% | 1,509,301.89 | **19,350.02** | 4 | 5.13% |

*Key Insight:* UPI leads in absolute transaction volume (311 transactions), while Branch banking carries the highest average ticket size (₹19,350.02). Net Banking exhibits the highest proportion of flagged records (6.45%).

---

### 3. Geographic Distribution (City Totals)

| City | Transaction Count | Total Transaction Value (₹) | Share of Total Value |
| :--- | :---: | :---: | :---: |
| **Mumbai** | **135** | **1,954,548.74** | **19.29%** |
| **Pune** | 119 | 1,630,580.38 | 16.09% |
| **Chennai** | 128 | 1,400,657.07 | 13.82% |
| **Ghaziabad** | 119 | 1,340,181.90 | 13.22% |
| **Bengaluru** | 125 | 1,184,160.36 | 11.68% |
| **Hyderabad** | 118 | 1,163,803.28 | 11.48% |
| **Kolkata** | 133 | 907,001.68 | 8.95% |
| **Delhi** | 118 | 553,623.37 | 5.46% |

---

### 4. Account Type Flow Comparison

| Account Type | Credit Total (₹) | Debit Total (₹) | Net Movement (₹) |
| :--- | :---: | :---: | :---: |
| **Current** | **1,739,034.29** | 1,365,861.95 | +373,172.34 (Net Inflow) |
| **Savings** | 1,044,191.26 | **1,893,374.76** | -849,183.50 (Net Outflow) |
| **Salary** | 994,329.39 | 1,431,457.60 | -437,128.21 (Net Outflow) |
| **Business** | 767,124.81 | 899,182.72 | -132,057.91 (Net Outflow) |

---

### 5. Outlier & Amount Band Segmentation

- **Quartile 1 ($Q_1$):** ₹1,976.91
- **Median ($Q_2$):** ₹3,581.51
- **Quartile 3 ($Q_3$):** ₹6,252.06
- **Interquartile Range (IQR):** ₹4,275.15
- **Lower Fence:** -₹4,435.82 *(Clamped at ₹0)*
- **Upper Fence:** ₹12,664.79
- **Statistical Outliers Identified:** **91 records** exceeding the upper fence.

#### Transaction Amount Bands
| Band | Range (₹) | Transaction Count | Total Value (₹) |
| :--- | :--- | :---: | :---: |
| **Low** | $\le 1,976.91$ | 249 | 322,858.03 |
| **Medium** | $(1,976.91, 3,581.51]$ | 264 | 747,444.30 |
| **High** | $(3,581.51, 6,252.06]$ | 233 | 1,121,215.49 |
| **Very High** | $> 6,252.06$ | 249 | 7,943,038.96 |

#### 90th Percentile Threshold Analysis (FR-14)
- **Threshold Value (90th Percentile):** ₹11,746.19
- **Transactions Above Threshold:** 100 records
- **Aggregate Value of Top 10%:** ₹6,666,414.68 (65.78% of overall transaction value)

---

## 🔍 Five Cautious Operational Observations and Recommendations

Following the strict guidelines in **SRS Section 3.2**:

1. **Channel Performance (Volume Concentration):**
   - *Observation:* UPI demonstrates the highest customer adoption and transaction throughput, accounting for 311 of 995 records (31.26%).
   - *Recommendation:* Evaluate server capacity, API gateway availability, and real-time settlement processing infrastructure for UPI endpoints to ensure resilience during peak traffic windows.

2. **Regional Transaction Value:**
   - *Observation:* Mumbai recorded the highest aggregate transaction value across all surveyed metros at ₹1,954,548.74 (19.29% of system volume).
   - *Recommendation:* Review regional transaction liquidity limits and branch service infrastructure in Mumbai to ensure optimal merchant and retail support.

3. **Flagged Records Analysis:**
   - *Observation:* Exactly 44 transactions (4.42%) were marked as flagged. Net Banking showed the highest rate (6.45%), while POS recorded the lowest (2.68%).
   - *Recommendation:* Audit the rule-based trigger thresholds that generate automated alerts. Since flagged records are preliminary markers and **not proof of fraud**, analysts should validate individual entries and conduct contextual reviews before escalating.

4. **Account Type Debit Dynamics:**
   - *Observation:* Savings accounts recorded the largest total debit outflow at ₹1,893,374.76, exceeding its credit volume by ₹849,183.50.
   - *Recommendation:* Compare debit and credit seasonality cycles across retail accounts to establish whether outflow peaks represent routine end-of-month expenditure or systemic liquidity movement.

5. **Statistical Outlier Evaluation:**
   - *Observation:* The standard IQR method identified 91 records exceeding the upper fence of ₹12,664.79, with top transactions reaching up to ₹499,612.04.
   - *Recommendation:* Treat outliers as statistical candidates for data verification rather than immediate anomalies. High-value transactions are typical in business and commercial banking; review data logging accuracy and establish tiered alert thresholds based on account type.

---

## 📂 Repository Structure

```text
.
├── 10_bank_transactions.csv                  # Raw dataset (1,000 synthetic banking records)
├── banking_transaction_pattern_analysis.ipynb # Primary analysis notebook (fully executed with outputs)
├── Untitled2.ipynb                           # Colab-linked analysis notebook (synchronized)
├── banking_transaction_pattern_analysis.py    # Standalone runnable Python script
├── requirements.txt                          # Python dependencies
├── .gitignore                                # Git ignore file
├── docs/                                     # Documentation deliverables
│   ├── SRS.md                                # Full Software Requirements Specification (Markdown)
│   ├── Software_Requirements_Specification_SRS.pdf # Original 8-page SRS PDF
│   └── Banking_Transaction_Pattern_Analysis_Notebook_Output.pdf # Expected outputs PDF (5 pages)
└── outputs/                                  # Exported summary data tables
    ├── account_summary.csv                   # Credit & Debit totals by Account Type
    ├── amount_band_summary.csv               # Distribution across Low, Medium, High, Very High
    ├── channel_flag_summary.csv              # Flagged percentages per channel
    ├── channel_summary.csv                   # Channel volume, value, and averages
    ├── city_summary.csv                      # Total transaction value per city
    ├── flagged_summary.csv                   # Overall flagged metric statistics
    ├── outliers.csv                          # 91 IQR outlier records
    └── top_10_transactions.csv               # 10 largest transactions
```

---

## 🚀 How to Run

### Method 1: Google Colab (One-Click)
Click the badge below to open and run the notebook directly in your browser:  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Lakshya-Pundhir/HCL-traning-project/blob/main/banking_transaction_pattern_analysis.ipynb)

### Method 2: Local Jupyter Notebook
1. Clone the repository:
   ```bash
   git clone https://github.com/Lakshya-Pundhir/HCL-traning-project.git
   cd HCL-traning-project
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch Jupyter:
   ```bash
   jupyter notebook banking_transaction_pattern_analysis.ipynb
   ```

### Method 3: Command-Line Python Script
Run the standalone analysis script to reproduce all console metrics and regenerate output CSV files:
```bash
python banking_transaction_pattern_analysis.py
```

---

## 📜 Metadata & Version History

- **Version:** 1.0
- **Release Date:** 19 November 2026
- **Prepared By:** Lakshya Pundhir
- **Project:** HCL Training Project 10 — Banking Transaction Pattern Analysis
