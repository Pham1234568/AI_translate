import gradio as gr
import pandas as pd
from languageexport.crew import LanguagesExport
import tempfile
import os

def process_excel(file, output_name):
    if not file or not output_name.strip():
        return "Please upload a file and provide a valid name.", None, None

    try:
        df = pd.read_excel(file.name)
        table = [df.columns.tolist()] + df.values.tolist()

        result = LanguagesExport().crew().kickoff(inputs={"data": table})
        result_df = pd.DataFrame(data=result["data"][1:], columns=result["data"][0])
        
        temp_dir = tempfile.mkdtemp()
        output_file_path = os.path.join(temp_dir, f"{output_name.strip()}.xlsx")
        result_df.to_excel(output_file_path, index=False)

        return "✅ Export completed successfully!", result_df, output_file_path

    except Exception as e:
        return f"❌ Error: {str(e)}", None, None


def show_input_table(file):
    if file is None:
        return gr.update(visible=True, value=None)
    try:
        df = pd.read_excel(file.name)
        return gr.update(visible=True, value=df)
    except Exception as e:
        return gr.update(visible=True, value=None)

with gr.Blocks() as demo:
    gr.Markdown("# 📄 Language Export Assistant")
    gr.Markdown("Upload an Excel file, define the export filename, and run the export process.")

    with gr.Row():
        file_input = gr.File(label="Upload Excel File", file_types=[".xlsx", ".xls"])
        file_name = gr.Textbox(label="Output file name (without extension)", placeholder="e.g. translated_table")

    run_button = gr.Button("Run Export")

    status_output = gr.Textbox(label="Status", interactive=False)

    # Luôn hiển thị layout, chỉ update nội dung
    with gr.Row():
        table_input = gr.Dataframe(label="Input Table")
        table_output = gr.Dataframe(label="Result Table")
    
    download_output = gr.File(label="Download Result File", visible=False)

    file_input.change(fn=show_input_table, inputs=file_input, outputs=table_input)

    def on_run(file, name):
        status, df, path = process_excel(file, name)
        is_valid_df = df is not None and not df.empty
        return (
            status,
            gr.update(value=df if is_valid_df else None),
            gr.update(value=path if path else None, visible=path is not None),
        )

    run_button.click(on_run, inputs=[file_input, file_name], outputs=[status_output, table_output, download_output])

if __name__ == "__main__":
    demo.launch(share=True)
