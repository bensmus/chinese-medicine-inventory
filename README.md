Run python script to get "medicine, day" totals in day_total.csv.

Turning "medicine, day" totals into "medicine, month" totals:
=sumifs(TOTALS, MEDICINES, TARGET_MEDICINE, DAYS, ">"&TARGET_MONTH, DAYS, "<="&EOMONTH(TARGET_MONTH,0)+1)
