import csv
from collections import defaultdict

CSV_PATH = "medicine.csv"
medicine_and_dose_delimeter = " "  # e.g. "牛蒡子 0.3"
formula_delimeter = "，"  # e.g. "甘露消毒丹 4，牛蒡子 0.3" - a nonstandard comma

DAY_COLUMN_INDEX = 0
FORMULA_COLUMN_INDEX = 1


def build_day_medicine_dict():
    output = defaultdict(lambda: defaultdict(lambda: 0.0))
    with open(CSV_PATH, encoding="utf-8") as f:
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
            for medicine_and_dose in formula.split(formula_delimeter):
                parts = medicine_and_dose.strip().rsplit(medicine_and_dose_delimeter, 1)
                if len(parts) != 2:
                    raise Exception(f"Cannot parse medicine and amount {parts}")
                medicine = parts[0]
                dose = float(parts[1])
                output[date][medicine] += dose
    return output


print(build_day_medicine_dict())
