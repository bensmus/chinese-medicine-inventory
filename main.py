from generate_csv import (
    generate_csv_per_day,
    generate_csv_per_month,
    get_totals_for_medicine_day,
)
import gradio as gr


def process(patient_formula_csv):
    totals_for_medicine_day = get_totals_for_medicine_day(patient_formula_csv)
    return generate_csv_per_day(totals_for_medicine_day), generate_csv_per_month(
        totals_for_medicine_day
    )


gr.Interface(
    fn=process,
    inputs="file",
    outputs=["file", "file"],
    flagging_mode="never",
).launch(share=True)
