import csv

CSV_PATH = "medicine.csv"
medicine_and_dose_delimeter = " "  # e.g. "牛蒡子 0.3"
formula_delimeter = "，"  # e.g. "甘露消毒丹 4，牛蒡子 0.3" - a nonstandard comma

DAY_COLUMN_INDEX = 0
FORMULA_COLUMN_INDEX = 1


def get_medicine_total_for_day(target_date: str, target_medicine: str) -> float:
    medicine_total_for_day = 0.0

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
            if date != target_date:
                continue
            for medicine_and_dose in formula.split(formula_delimeter):
                parts = medicine_and_dose.strip().rsplit(medicine_and_dose_delimeter, 1)
                if len(parts) != 2:
                    raise Exception(f"Cannot parse medicine and amount {parts}")
                medicine, dose = parts
                if target_medicine == medicine:
                    medicine_total_for_day += float(dose)

    return round(medicine_total_for_day, 2)


print(get_medicine_total_for_day("2026-01-12", "牛蒡子"))
print(get_medicine_total_for_day("2026-01-14", "梔子豉湯"))  # Expected: 2.9
