"""
PROJECT 10: BANKING TRANSACTION PATTERN ANALYSIS
Software Requirements Specification (SRS) Implementation
Prepared by: Lakshya
Date: November 2026
Industry: Banking / FinTech
Dataset: 10_bank_transactions.csv (Synthetic)
"""

import os
import csv
import math

def run_analysis(csv_file_path=None):
    if csv_file_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(base_dir, "10_bank_transactions.csv")
    print("=" * 70)
    print("BANKING TRANSACTION PATTERN ANALYSIS - PROJECT 10")
    print("=" * 70)

    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_file_path}")

    # ------------------------------------------------------------
    # 1. LOAD AND INSPECT DATASET (FR-01)
    # ------------------------------------------------------------
    print("\n--- [FR-01] LOAD AND INSPECT DATASET ---")
    with open(csv_file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_columns = reader.fieldnames
        raw_rows = list(reader)

    print(f"Dataset Shape: ({len(raw_rows)}, {len(original_columns)})")
    print("\nOriginal Column Names:")
    print(original_columns)

    print("\nFIRST 5 RECORDS:")
    for idx, row in enumerate(raw_rows[:5]):
        print(f"Row {idx}: {row}")

    # Standardized Column Names
    standard_columns = list(original_columns)
    print("\nSTANDARDIZED COLUMN NAMES:")
    print(standard_columns)

    # ------------------------------------------------------------
    # 2. FIND AND HANDLE MISSING TRANSACTION AMOUNTS (FR-02)
    # ------------------------------------------------------------
    print("\n--- [FR-02] MISSING TRANSACTION AMOUNTS ---")
    missing_count = sum(1 for r in raw_rows if not r["Transaction_Amount"].strip())
    print(f"MISSING TRANSACTION AMOUNTS: {missing_count}")

    valid_amounts = [float(r["Transaction_Amount"]) for r in raw_rows if r["Transaction_Amount"].strip()]
    valid_amounts.sort()
    n_valid = len(valid_amounts)
    if n_valid % 2 == 1:
        median_imputed = valid_amounts[n_valid // 2]
    else:
        median_imputed = (valid_amounts[n_valid // 2 - 1] + valid_amounts[n_valid // 2]) / 2.0

    print(f"Missing amounts handled using median: {median_imputed}")

    # Impute missing values
    for r in raw_rows:
        if not r["Transaction_Amount"].strip():
            r["Transaction_Amount"] = str(median_imputed)
        r["Amount_Abs"] = abs(float(r["Transaction_Amount"]))

    # ------------------------------------------------------------
    # 3. CHECK AND HANDLE DUPLICATE TRANSACTION IDs (FR-03)
    # ------------------------------------------------------------
    print("\n--- [FR-03] DUPLICATE TRANSACTION IDs ---")
    id_counts = {}
    for r in raw_rows:
        tid = r["Transaction_ID"].strip()
        id_counts[tid] = id_counts.get(tid, 0) + 1

    duplicate_ids = [tid for tid, count in id_counts.items() if count > 1]
    duplicate_rows_count = sum(count for tid, count in id_counts.items() if count > 1)

    print(f"DUPLICATE TRANSACTION IDs: {len(duplicate_ids)}")
    print(f"ROWS WITH DUPLICATE IDs: {duplicate_rows_count}")

    # Deduplicate: keep first occurrence
    seen_ids = set()
    cleaned_rows = []
    for r in raw_rows:
        tid = r["Transaction_ID"].strip()
        if tid not in seen_ids:
            seen_ids.add(tid)
            cleaned_rows.append(r)

    print(f"Records after duplicate handling: {len(cleaned_rows)}")

    # ------------------------------------------------------------
    # 4. CALCULATE TOTAL CREDITS AND TOTAL DEBITS (FR-04)
    # ------------------------------------------------------------
    print("\n--- [FR-04] TOTAL CREDITS AND DEBITS ---")
    total_credit = sum(r["Amount_Abs"] for r in cleaned_rows if r["Transaction_Type"].strip().lower() == "credit")
    total_debit = sum(r["Amount_Abs"] for r in cleaned_rows if r["Transaction_Type"].strip().lower() == "debit")
    net_flow = total_credit - total_debit

    print(f"TOTAL CREDIT VALUE: {total_credit:.2f}")
    print(f"TOTAL DEBIT VALUE: {total_debit:.2f}")
    print(f"NET FLOW (Credits - Debits): {net_flow:.2f}")

    # ------------------------------------------------------------
    # 5. MEAN, MEDIAN AND STANDARD DEVIATION (FR-05)
    # ------------------------------------------------------------
    print("\n--- [FR-05] TRANSACTION STATISTICS ---")
    all_amounts = [r["Amount_Abs"] for r in cleaned_rows]
    all_amounts.sort()
    n_records = len(all_amounts)
    mean_amount = sum(all_amounts) / n_records
    if n_records % 2 == 1:
        median_amount = all_amounts[n_records // 2]
    else:
        median_amount = (all_amounts[n_records // 2 - 1] + all_amounts[n_records // 2]) / 2.0

    variance = sum((x - mean_amount) ** 2 for x in all_amounts) / (n_records - 1)
    std_dev = math.sqrt(variance)

    print(f"Mean: {mean_amount:.10f}")
    print(f"Median: {median_amount}")
    print(f"Standard Deviation: {std_dev:.10f}")

    # ------------------------------------------------------------
    # 6. COMPARE TRANSACTION VOLUME BY CHANNEL (FR-06)
    # ------------------------------------------------------------
    print("\n--- [FR-06] TRANSACTION CHANNEL SUMMARY ---")
    channels = {}
    for r in cleaned_rows:
        c = r["Channel"].strip()
        if c not in channels:
            channels[c] = {"count": 0, "total": 0.0, "flagged": 0}
        channels[c]["count"] += 1
        channels[c]["total"] += r["Amount_Abs"]
        if r["Flagged"].strip() in ["1", "true", "True"]:
            channels[c]["flagged"] += 1

    sorted_channels = sorted(channels.items(), key=lambda x: x[1]["count"], reverse=True)
    print(f"{'Channel':<15} {'Transaction_Count':<20} {'Total_Value':<18} {'Average_Value':<15}")
    print("-" * 70)
    for c, d in sorted_channels:
        avg_val = d["total"] / d["count"]
        print(f"{c:<15} {d['count']:<20} {d['total']:<18.2f} {avg_val:<15.6f}")

    # ------------------------------------------------------------
    # 7. TOTAL TRANSACTION VALUE BY CITY (FR-07)
    # ------------------------------------------------------------
    print("\n--- [FR-07] CITY TRANSACTION SUMMARY ---")
    cities = {}
    for r in cleaned_rows:
        city = r["City"].strip()
        if city not in cities:
            cities[city] = {"count": 0, "total": 0.0}
        cities[city]["count"] += 1
        cities[city]["total"] += r["Amount_Abs"]

    sorted_cities = sorted(cities.items(), key=lambda x: x[1]["total"], reverse=True)
    print(f"{'City':<15} {'Transaction_Count':<20} {'Total_Transaction_Value':<20}")
    print("-" * 58)
    for city, d in sorted_cities:
        print(f"{city:<15} {d['count']:<20} {d['total']:<20.2f}")

    # ------------------------------------------------------------
    # 8. FLAGGED TRANSACTION COUNT AND PERCENTAGE (FR-08)
    # ------------------------------------------------------------
    print("\n--- [FR-08] FLAGGED TRANSACTION SUMMARY ---")
    total_txns = len(cleaned_rows)
    valid_flag_count = total_txns
    flagged_count = sum(1 for r in cleaned_rows if r["Flagged"].strip() in ["1", "true", "True"])
    flagged_percentage = (flagged_count / valid_flag_count) * 100.0

    print(f"Total Transactions: {total_txns}")
    print(f"Valid Flag Labels:  {valid_flag_count}")
    print(f"Flagged Count:       {flagged_count}")
    print(f"Flagged Percentage:  {flagged_percentage:.2f}%")

    # ------------------------------------------------------------
    # 9. FLAGGED PERCENTAGE BY CHANNEL (FR-09)
    # ------------------------------------------------------------
    print("\n--- [FR-09] FLAGGED PERCENTAGE BY CHANNEL ---")
    print(f"{'Channel':<15} {'Total_Transactions':<20} {'Flagged_Count':<15} {'Valid_Labels':<15} {'Flagged_Percentage':<20}")
    print("-" * 85)
    for c, d in sorted(channels.items(), key=lambda x: x[0]):
        pct = (d["flagged"] / d["count"]) * 100.0
        print(f"{c:<15} {d['count']:<20} {d['flagged']:<15} {d['count']:<15} {pct:<20.6f}")

    # ------------------------------------------------------------
    # 10. FIND 10 LARGEST TRANSACTIONS (FR-10)
    # ------------------------------------------------------------
    print("\n--- [FR-10] 10 LARGEST TRANSACTIONS ---")
    top_10 = sorted(cleaned_rows, key=lambda x: x["Amount_Abs"], reverse=True)[:10]
    print(f"{'Transaction_ID':<18} {'Type':<10} {'Amount':<15} {'Channel':<15} {'City':<15}")
    print("-" * 75)
    for r in top_10:
        print(f"{r['Transaction_ID']:<18} {r['Transaction_Type']:<10} {r['Amount_Abs']:<15.2f} {r['Channel']:<15} {r['City']:<15}")

    # ------------------------------------------------------------
    # 11. CREDIT AND DEBIT TOTALS BY ACCOUNT TYPE (FR-11)
    # ------------------------------------------------------------
    print("\n--- [FR-11] CREDIT AND DEBIT TOTALS BY ACCOUNT TYPE ---")
    accounts = {}
    for r in cleaned_rows:
        acc = r["Account_Type"].strip()
        ttype = r["Transaction_Type"].strip().title()
        if acc not in accounts:
            accounts[acc] = {"Credit": 0.0, "Debit": 0.0}
        accounts[acc][ttype] += r["Amount_Abs"]

    print(f"{'Account_Type':<15} {'Credit':<18} {'Debit':<18}")
    print("-" * 51)
    for acc in sorted(accounts.keys()):
        print(f"{acc:<15} {accounts[acc]['Credit']:<18.2f} {accounts[acc]['Debit']:<18.2f}")

    # ------------------------------------------------------------
    # 12. IDENTIFY OUTLIERS USING IQR RULE (FR-12)
    # ------------------------------------------------------------
    print("\n--- [FR-12] IQR OUTLIER ANALYSIS ---")
    # Linear interpolation matching numpy.percentile
    def percentile(data, p):
        k = (len(data) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return data[int(k)]
        d0 = data[int(f)] * (c - k)
        d1 = data[int(c)] * (k - f)
        return d0 + d1

    q1 = percentile(all_amounts, 25)
    q3 = percentile(all_amounts, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = [r for r in cleaned_rows if r["Amount_Abs"] < lower_bound or r["Amount_Abs"] > upper_bound]

    print(f"Q1:          {q1}")
    print(f"Q3:          {q3}")
    print(f"IQR:         {iqr}")
    print(f"Lower Bound: {lower_bound}")
    print(f"Upper Bound: {upper_bound}")
    print(f"Number of Outliers: {len(outliers)}")

    # ------------------------------------------------------------
    # 13. CREATE TRANSACTION AMOUNT BANDS (FR-13)
    # ------------------------------------------------------------
    print("\n--- [FR-13] TRANSACTION AMOUNT BANDS ---")
    p25 = percentile(all_amounts, 25)
    p50 = percentile(all_amounts, 50)
    p75 = percentile(all_amounts, 75)

    band_counts = {"Low": 0, "Medium": 0, "High": 0, "Very High": 0}
    band_totals = {"Low": 0.0, "Medium": 0.0, "High": 0.0, "Very High": 0.0}

    for r in cleaned_rows:
        amt = r["Amount_Abs"]
        if amt <= p25:
            b = "Low"
        elif amt <= p50:
            b = "Medium"
        elif amt <= p75:
            b = "High"
        else:
            b = "Very High"
        r["Amount_Band"] = b
        band_counts[b] += 1
        band_totals[b] += amt

    print(f"{'Amount_Band':<15} {'Transaction_Count':<20} {'Total_Value':<18}")
    print("-" * 55)
    for b in ["Low", "Medium", "High", "Very High"]:
        print(f"{b:<15} {band_counts[b]:<20} {band_totals[b]:<18.2f}")

    # ------------------------------------------------------------
    # 14. BOOLEAN INDEXING THRESHOLD FILTERING (FR-14)
    # ------------------------------------------------------------
    print("\n--- [FR-14] TRANSACTIONS ABOVE THE 90TH PERCENTILE ---")
    p90 = percentile(all_amounts, 90)
    above_p90 = [r for r in cleaned_rows if r["Amount_Abs"] > p90]
    total_val_p90 = sum(r["Amount_Abs"] for r in above_p90)

    print(f"SELECTED TRANSACTION THRESHOLD: {p90}")
    print(f"Number of Transactions Above 90th Percentile: {len(above_p90)}")
    print(f"Total Value Above Threshold: {total_val_p90:.2f}")

    # ------------------------------------------------------------
    # 15. FIVE CAUTIOUS OPERATIONAL OBSERVATIONS (FR-15)
    # ------------------------------------------------------------
    print("\n" + "=" * 70)
    print("OPERATIONAL OBSERVATIONS AND RECOMMENDATIONS")
    print("=" * 70)

    top_channel_name = sorted_channels[0][0]
    top_channel_count = sorted_channels[0][1]["count"]
    top_city_name = sorted_cities[0][0]
    top_city_val = sorted_cities[0][1]["total"]
    top_debit_acc = max(accounts.items(), key=lambda x: x[1]["Debit"])[0]
    top_debit_val = accounts[top_debit_acc]["Debit"]

    print("\n1. CHANNEL PERFORMANCE:")
    print(f"{top_channel_name} has the highest transaction volume with {top_channel_count} records.")
    print("Recommendation: Review channel capacity, availability and transaction processing performance.")

    print("\n2. CITY TRANSACTION VALUE:")
    print(f"{top_city_name} has the highest recorded transaction value of {top_city_val:.2f}.")
    print("Recommendation: Review regional transaction volume and ensure appropriate service capacity.")

    print("\n3. FLAGGED RECORDS:")
    print(f"{flagged_count} transactions are flagged out of {valid_flag_count} records with valid labels ({flagged_percentage:.2f}%).")
    print("Recommendation: Review the rules that generate these labels and validate records individually. A flagged label is not proof of fraud.")

    print("\n4. ACCOUNT TYPE:")
    print(f"{top_debit_acc} has the highest recorded debit value ({top_debit_val:.2f}).")
    print("Recommendation: Compare credit and debit patterns across account types and review whether the differences are expected.")

    print("\n5. TRANSACTION OUTLIERS:")
    print(f"The IQR method identified {len(outliers)} outlier records.")
    print("Recommendation: Review these records with transaction context and data-quality checks. An outlier is not automatically suspicious.")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("Summary CSV files have been created.")
    print("=" * 70)

if __name__ == "__main__":
    run_analysis()
