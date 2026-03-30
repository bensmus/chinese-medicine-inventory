from build_day_total_csv import build_day_total_csv
import gradio as gr

gr.Interface(
    fn=build_day_total_csv, inputs="file", outputs="file", flagging_mode="never"
).launch()
