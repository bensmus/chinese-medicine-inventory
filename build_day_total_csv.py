import csv
from collections import defaultdict

OUTPUT_DAY_CSV_PATH = "day_total.csv"
OUTPUT_MONTH_CSV_PATH = "month_total.csv"
MEDICINE_AND_DOSE_DELIMETER = " "  # e.g. "牛蒡子 0.3"
FORMULA_DELIMETER = "，"  # e.g. "甘露消毒丹 4，牛蒡子 0.3" - a nonstandard comma

DAY_COLUMN_INDEX = 0
FORMULA_COLUMN_INDEX = 1


def build_day_medicine_dict(patient_formula_csv):
    output = defaultdict(lambda: defaultdict(lambda: 0.0))
    with open(patient_formula_csv, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) < 2:
                raise Exception(
                    "Invalid CSV: All rows need to have at least length 2 (DAY and FORMULA)"
                )
            date = row[DAY_COLUMN_INDEX].strip()
            formula = row[FORMULA_COLUMN_INDEX].strip()
            if formula == "":
                raise Exception("Empty FORMULA")
            for medicine_and_dose in formula.split(FORMULA_DELIMETER):
                parts = medicine_and_dose.strip().rsplit(MEDICINE_AND_DOSE_DELIMETER, 1)
                if len(parts) != 2:
                    raise Exception(f"Cannot parse medicine and amount {parts}")
                medicine = parts[0]
                dose = float(parts[1])
                output[date][medicine] += dose
    return output


def build_day_total_csv(patient_formula_csv):
    day_medicine_dict = build_day_medicine_dict(patient_formula_csv)
    rows = []
    for day in day_medicine_dict:
        medicine_dict = day_medicine_dict[day]
        for medicine, total in medicine_dict.items():
            rows.append([day, medicine, round(total, 2)])

    with open(OUTPUT_DAY_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["day", "medicine", "total"])
        writer.writerows(rows)

    return OUTPUT_DAY_CSV_PATH


def build_month_total_csv(patient_formula_csv):
    day_medicine_dict = build_day_medicine_dict(patient_formula_csv)
    month_medicine = defaultdict(lambda: 0.0)
    for day, medicine_dict in day_medicine_dict.items():
        month = day[:7]  # "2026-01-12" -> "2026-01"
        for medicine, total in medicine_dict.items():
            month_medicine[(month, medicine)] += total

    rows = []
    for (month, medicine), total in month_medicine.items():
        rows.append([month, medicine, round(total, 2)])

    with open(OUTPUT_MONTH_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "medicine", "total"])
        writer.writerows(rows)

    return OUTPUT_MONTH_CSV_PATH
