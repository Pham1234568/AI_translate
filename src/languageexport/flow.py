from crewai.flow.flow import Flow,listen,start
import json
import os
from typing import List, Dict,Any
from pydantic import BaseModel, Field
from crewai.flow.flow import Flow, listen, start
import pandas as pd
from languageexport.crew import LanguagesExport
class OutputFile(Flow):
    @start()
    def get_data(self):
        path = input("Enter path to your Excel file (e.g., full_translations.xlsx): ").strip()
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        df = pd.read_excel(path)
        print(f"Loaded {path} with shape {df.shape}")
        table = [df.columns.tolist()] + df.values.tolist()
        self.state['table'] = table
        return table

    @listen(get_data)
    def ask_filename(self, table: List[List[Any]]):
        filename = input("Enter desired output filename (with .xlsx extension): ").strip()
        if not filename.lower().endswith('.xlsx'):
            filename += '.xlsx'
        self.state['filename'] = filename
        return table

    @listen(ask_filename)
    def create_file(self, table: List[List[Any]]):
        filename = self.state['filename']
        result = LanguagesExport().crew().kickoff(inputs={'data': table, 'filename': filename})
        self.state['result'] = result
        print(f"Agent returned: {result}")
        if os.path.exists(filename):
            print(f"Output file created: {filename}")
        else:
            print(f"Expected output file not found: {filename}")
        return filename

    @listen(create_file)
    def show_file(self, filename: str):
        df = pd.read_excel(filename)
        print("✅ Translated content:")
        print(df)
        return df