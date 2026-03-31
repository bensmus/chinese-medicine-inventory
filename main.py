from build_day_total_csv import build_day_total_csv, build_month_total_csv
import gradio as gr


def process(patient_formula_csv):
    return build_day_total_csv(patient_formula_csv), build_month_total_csv(patient_formula_csv)


gr.Interface(
    fn=process,
    inputs="file",
    outputs=["file", "file"],
    flagging_mode="never",
).launch()
