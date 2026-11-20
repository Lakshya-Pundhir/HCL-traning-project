# Software Requirements Specification (SRS)
## Banking Transaction Pattern Analysis – Project 10

**Industry:** Banking / FinTech  
**Dataset:** `10_bank_transactions.csv` (synthetic)  
**Prepared by:** Lakshya  
**Version:** 1.0  
**Date:** 19 November 2026  

---

## Table of Contents
1. [Introduction](#1-introduction)
   - 1.1 [Purpose](#11-purpose)
   - 1.2 [Scope](#12-scope)
   - 1.3 [Important Disclaimer](#13-important-disclaimer)
   - 1.4 [Definitions and Abbreviations](#14-definitions-and-abbreviations)
   - 1.5 [Intended Audience](#15-intended-audience)
2. [General Description](#2-general-description)
   - 2.1 [Product Perspective](#21-product-perspective)
   - 2.2 [Business Scenario](#22-business-scenario)
   - 2.3 [User Classes](#23-user-classes)
   - 2.4 [Operating Environment](#24-operating-environment)
   - 2.5 [Assumptions and Dependencies](#25-assumptions-and-dependencies)
3. [Functional Requirements](#3-functional-requirements)
   - 3.1 [Analysis Functions (FR-01 to FR-15)](#31-analysis-functions)
   - 3.2 [Cautious Observations Requirement](#32-cautious-observations-requirement)
4. [Interface Requirements](#4-interface-requirements)
   - 4.1 [User Interface](#41-user-interface)
   - 4.2 [Software Interface](#42-software-interface)
   - 4.3 [Hardware Interface](#43-hardware-interface)
   - 4.4 [Input Interface](#44-input-interface)
   - 4.5 [Output Interface](#45-output-interface)
5. [Performance Requirements](#5-performance-requirements)
6. [Design Constraints](#6-design-constraints)
7. [Non-Functional Attributes](#7-non-functional-attributes)
8. [Preliminary Schedule and Budget](#8-preliminary-schedule-and-budget)
   - 8.1 [Preliminary Schedule](#81-preliminary-schedule)
   - 8.2 [Budget](#82-budget)
9. [Appendices](#9-appendices)
   - [Appendix A: Data Dictionary](#appendix-a-data-dictionary)
   - [Appendix B: Processing Flow](#appendix-b-processing-flow)
   - [Appendix C: Acceptance Criteria](#appendix-c-acceptance-criteria)
   - [Appendix D: Risks and Limitations](#appendix-d-risks-and-limitations)
   - [Appendix E: Future Enhancements](#appendix-e-future-enhancements)
   - [Appendix F: Revision History](#appendix-f-revision-history)

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for a data-analysis solution that explores bank transaction records and summarizes transaction behavior by amount, channel, city, account type, transaction type and flagged status. It defines what the analysis must do, the data it consumes, the outputs it produces and the criteria used to judge it complete.

### 1.2 Scope
The system is a Python-based analytical workflow (pandas and NumPy, run in a notebook or script) that loads one CSV file, cleans it, computes descriptive statistics and group summaries, detects amount outliers, and produces a short set of cautious operational observations. It does not build a fraud-detection model, does not connect to live banking systems and does not make decisions about any customer or account.

### 1.3 Important Disclaimer
> **Important:** The dataset is **synthetic**. The `Flagged` column is a supplied label only and is **not proof of fraud**. No output of this project may be used to claim, imply or investigate fraud by any person or institution.

### 1.4 Definitions and Abbreviations

| Term | Meaning |
| :--- | :--- |
| **SRS** | Software Requirements Specification |
| **IQR** | Interquartile range ($Q_3 - Q_1$), used for outlier detection |
| **Credit** | Money coming into an account |
| **Debit** | Money going out of an account |
| **Flagged** | A supplied 0/1 label on a transaction; not a fraud verdict |
| **Channel** | The route used for a transaction (e.g., UPI, ATM, Branch) |
| **Outlier** | An amount outside $Q_1 - 1.5 \times \text{IQR}$ or $Q_3 + 1.5 \times \text{IQR}$ |

### 1.5 Intended Audience
The student or analyst completing the assignment, the reviewer or instructor evaluating it, and any business reader who will consume the summary tables and recommendations.

---

## 2. General Description

### 2.1 Product Perspective
A standalone, offline analysis workflow. Input is a single CSV file; outputs are tables, optional charts and a written findings section. It has no dependency on external services.

### 2.2 Business Scenario
A bank wants a first-pass understanding of how transactions behave: how large they are, which channels and cities carry the most activity, how credits and debits compare, and how flagged records are distributed. The goal is descriptive insight to guide operational attention, not accusation.

### 2.3 User Classes

| User | Need |
| :--- | :--- |
| **Analyst / student** | Run the workflow end to end and reproduce results |
| **Reviewer** | Verify each task is answered and results are traceable |
| **Business stakeholder** | Read concise summaries and cautious recommendations |

### 2.4 Operating Environment
Python 3.9 or later with pandas, NumPy and (optionally) matplotlib; Jupyter Notebook or any Python runtime. Any operating system.

### 2.5 Assumptions and Dependencies
- The file `10_bank_transactions.csv` is available in the working directory.
- Column names match the data dictionary in Appendix A.
- `Transaction_Amount` is a positive number in a single currency; direction is given by `Transaction_Type`.
- Each `Transaction_ID` should be unique; violations are reported, not silently hidden.

---

## 3. Functional Requirements

### 3.1 Analysis Functions

Each requirement maps to one assignment task:

| ID | Requirement | Method / Hint |
| :--- | :--- | :--- |
| **FR-01** | The system shall load the CSV and display shape, column names, data types, head and basic info. | `pd.read_csv`, `.info()`, `.head()` |
| **FR-02** | The system shall count missing `Transaction_Amount` values and handle them using a documented strategy (e.g., median imputation, with the reason stated), keeping a record of how many rows were affected. | `.isna().sum()`, `.fillna()` |
| **FR-03** | The system shall detect duplicate `Transaction_ID` values, report how many and which, and state how they are treated. | `.duplicated()` |
| **FR-04** | The system shall calculate total credits and total debits and show their difference (net flow). | `groupby('Transaction_Type')` |
| **FR-05** | The system shall calculate mean, median and standard deviation of `Transaction_Amount`. | `.mean()`, `.median()`, `.std()` |
| **FR-06** | The system shall compare transaction volume (count, with optional share) by channel. | `value_counts()` / `groupby` |
| **FR-07** | The system shall compare total transaction value by city. | `groupby('City') sum` |
| **FR-08** | The system shall calculate the flagged transaction count and its percentage of all transactions. | `Flagged.sum()`, `.mean()*100` |
| **FR-09** | The system shall compare flagged percentage across channels. | `groupby('Channel') mean` |
| **FR-10** | The system shall list the 10 largest transactions. | `.nlargest(10, 'Transaction_Amount')` |
| **FR-11** | The system shall group credit and debit totals by account type. | `groupby(['Account_Type','Transaction_Type'])` |
| **FR-12** | The system shall identify amount outliers using the IQR rule, reporting Q1, Q3, IQR, the two fences and the outlier count. | `np.percentile(amount, [25, 75])` |
| **FR-13** | The system shall assign each transaction to an amount band (e.g., Low, Medium, High, Very High) and report counts per band. | `pd.cut` / `pd.qcut` |
| **FR-14** | The system shall use NumPy Boolean indexing to isolate transactions above a stated threshold and report how many were found and their total value. | `arr[arr > threshold]` |
| **FR-15** | The system shall produce five cautious operational observations with recommendations (see Section 3.2). | Written findings |

### 3.2 Cautious Observations Requirement

The five observations and recommendations must follow these rules:
1. They describe patterns in the data, never guilt or intent.
2. They state that `Flagged` is a supplied label and **not proof of fraud**.
3. They avoid causal claims that the data cannot support.
4. They recommend review, monitoring or further data collection rather than enforcement action.
5. They mention data-quality limits (missing amounts, duplicates, synthetic origin).

---

## 4. Interface Requirements

### 4.1 User Interface
The system is operated through a Jupyter Notebook or a Python script run from the command line. Results appear as printed tables and optional charts in the notebook output.

### 4.2 Software Interface
The system relies on Python, pandas (data loading and grouping), NumPy (percentiles and Boolean indexing) and, optionally, matplotlib (charts). No database or web service is used.

### 4.3 Hardware Interface
A standard laptop or desktop computer. No special hardware is required.

### 4.4 Input Interface
A single comma-separated file, `10_bank_transactions.csv`, with a header row and the columns listed in Appendix A (approximately 1,000 rows, 9 columns).

### 4.5 Output Interface
The system shall present the following deliverables:
- **Channel summary:** transaction count, share and flagged percentage per channel.
- **City summary:** total transaction value (and optionally count) per city.
- **Credit/debit comparison:** overall totals and a breakdown by account type.
- **Flagged-record summary:** overall count and percentage, plus the comparison across channels.
- **Cautious recommendations:** five observations, each with a recommendation.

---

## 5. Performance Requirements
- The full workflow shall run in under one minute on a standard laptop for about 1,000 rows.
- Loading and cleaning the CSV shall complete within a few seconds.
- The solution shall remain usable (under a few minutes) if the dataset grows to around 100,000 rows.
- Results shall be reproducible: running the notebook top to bottom gives identical output.

---

## 6. Design Constraints
- Individual work; results must be reproducible from the code.
- Only Python with pandas and NumPy is required; matplotlib is optional.
- Synthetic data only; no real customer data may be introduced.
- Language and conclusions must stay cautious and descriptive; the Flagged label must never be presented as proof of fraud.
- Outlier detection must use the IQR rule computed with `np.percentile`; threshold filtering must use NumPy Boolean indexing.

---

## 7. Non-Functional Attributes

| ID | Attribute | Requirement |
| :--- | :--- | :--- |
| **NFR-01** | Reproducibility | A fixed random seed is used wherever randomness appears, so repeated runs give the same results. |
| **NFR-02** | Readability | Code shall be commented and organized by task number. |
| **NFR-03** | Accuracy | Totals shall reconcile: credits + debits equals the overall sum; band counts sum to the row count. |
| **NFR-04** | Transparency | Every cleaning decision (imputation, duplicate handling) shall be documented in the notebook. |
| **NFR-05** | Data privacy | Only synthetic data is used; no personal information is stored or shown. |
| **NFR-06** | Ethical use | Output text must not contain fraud accusations or imply a real-world verdict. |
| **NFR-07** | Maintainability | Each task is kept in a separate, clearly titled code section so it can be updated independently. |
| **NFR-08** | Portability | The solution runs on any operating system with Python 3.9 or later. |

---

## 8. Preliminary Schedule and Budget

### 8.1 Preliminary Schedule

| Phase | Activities | Estimated Duration |
| :--- | :--- | :--- |
| **Phase 1** | Load, inspect and clean the data (FR-01 to FR-03) | 1 day |
| **Phase 2** | Statistics and group summaries (FR-04 to FR-11) | 1–2 days |
| **Phase 3** | Outliers, bands and Boolean indexing (FR-12 to FR-14) | 1 day |
| **Phase 4** | Observations, recommendations and report writing (FR-15) | 1 day |
| **Phase 5** | Review, verification of totals and final submission | 0.5 day |

### 8.2 Budget
No monetary cost is expected. All tools used (Python, pandas, NumPy, Jupyter and matplotlib) are free and open source, and the dataset is synthetic. The main resource is the analyst's time, estimated at roughly 20–30 working hours in total.

---

## 9. Appendices

### Appendix A: Data Dictionary

| Column | Type | Description |
| :--- | :--- | :--- |
| `Transaction_ID` | String | Identifier of the transaction (expected unique) |
| `Transaction_Date` | Date (`YYYY-MM-DD`) | Date of the transaction |
| `Account_ID` | String | Identifier of the account |
| `Account_Type` | Category | Savings, Current, Salary, Business |
| `Transaction_Type` | Category | Credit or Debit |
| `Channel` | Category | UPI, ATM, Branch, Net Banking, Mobile App, POS |
| `City` | Category | City where the transaction was recorded |
| `Transaction_Amount` | Float | Amount of the transaction (may contain missing values) |
| `Flagged` | Integer (0/1) | Supplied label: 1 = flagged, 0 = not flagged |

### Appendix B: Processing Flow
1. Load and inspect the data.
2. Clean: handle missing amounts, check and document duplicate IDs.
3. Compute overall statistics (credits, debits, mean, median, standard deviation).
4. Aggregate by channel, city and account type.
5. Analyse flagged records overall and by channel.
6. Rank the 10 largest transactions.
7. Detect outliers with IQR and create amount bands.
8. Apply NumPy Boolean indexing for the threshold view.
9. Write the five observations and recommendations.
10. Assemble the final summary tables.

### Appendix C: Acceptance Criteria
- All 15 tasks are completed and traceable to FR-01 to FR-15.
- Missing-value and duplicate handling is explained in one or two sentences each.
- IQR fences are computed with `np.percentile` and shown.
- The Boolean-indexing threshold is stated and justified (for example, the upper IQR fence or a round business figure).
- All five required deliverables in Section 4.5 are present.
- The disclaimer that the data is synthetic and the flag is not proof of fraud appears in the report.
- Totals reconcile as per NFR-03.

### Appendix D: Risks and Limitations

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Median imputation hides the true value of missing amounts** | Totals slightly distorted | State the number imputed; also show results excluding missing rows |
| **Duplicate IDs may be errors or repeats** | Double counting | Report clearly; show totals with and without duplicates |
| **Heavy skew from large amounts** | Mean misleads | Report median and IQR alongside the mean |
| **Flagged label misread as fraud** | Wrongful conclusions | Repeat the disclaimer in outputs and recommendations |
| **Synthetic data differs from real behavior** | Findings not transferable | Present findings as an exercise, not as evidence about real banking activity |

### Appendix E: Future Enhancements
- Time-based analysis (day of week, month, seasonality).
- Interactive dashboard for channel and city filters.
- Comparison of flagged rates by amount band with statistical testing.
- A documented data-validation step that runs before every load.

### Appendix F: Revision History

| Version | Date | Author | Change |
| :--- | :--- | :--- | :--- |
| 1.0 | 19 Nov 2026 | Lakshya | Initial SRS |
