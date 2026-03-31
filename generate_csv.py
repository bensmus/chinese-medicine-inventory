import csv
from collections import defaultdict
from typing import DefaultDict, Tuple

OUTPUT_DAY_CSV_PATH = "day_total.csv"
OUTPUT_MONTH_CSV_PATH = "month_total.csv"
MEDICINE_AND_DOSE_DELIMETER = " "  # e.g. "牛蒡子 0.3"
FORMULA_DELIMETER = "，"  # e.g. "甘露消毒丹 4，牛蒡子 0.3" - a nonstandard comma

DAY_COLUMN_INDEX = 0
FORMULA_COLUMN_INDEX = 1


def get_totals_for_medicine_day(
    patient_formula_csv,
) -> DefaultDict[Tuple[str, str], float]:
    output = defaultdict(lambda: 0.0)
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
                output[(date, medicine)] += dose
    return output


def generate_csv_per_day(totals_for_medicine_day: DefaultDict[Tuple[str, str], float]):
    rows = []
    for (day, medicine), total in totals_for_medicine_day.items():
        rows.append([day, medicine, round(total, 2)])

    with open(OUTPUT_DAY_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["day", "medicine", "total"])
        writer.writerows(rows)

    return OUTPUT_DAY_CSV_PATH


def generate_csv_per_month(totals_for_medicine_day: DefaultDict[Tuple[str, str], float]):
    month_medicine = defaultdict(lambda: 0.0)
    for (day, medicine), total in totals_for_medicine_day.items():
        month = day[:7]  # "2026-01-12" -> "2026-01"
        month_medicine[(month, medicine)] += total

    rows = []
    for (month, medicine), total in month_medicine.items():
        rows.append([month, medicine, round(total, 2)])

    with open(OUTPUT_MONTH_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "medicine", "total"])
        writer.writerows(rows)

    return OUTPUT_MONTH_CSV_PATH
