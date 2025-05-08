#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
from typing import List, Dict, Any

import os

import json
from pydantic import BaseModel, Field
from languageexport.flow import OutputFile
from languageexport.crew import LanguagesExport
import pandas as pd
import tkinter as Tk
from tkinter import Tk

from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    Tk().withdraw()

    # Mở hộp thoại chọn file
    print("Vui lòng chọn file Excel đầu vào")
    
    file_path = askopenfilename(
        title="Chọn file Excel đầu vào",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    print(f"đường dẫn:{file_path}")
    file_name=input("Enter the file name: ")
    file_name_save=f"{file_name}.xlsx"
    df= pd.read_excel(file_path)
    table = [df.columns.tolist()] + df.values.tolist()
    print(table)
    rs=LanguagesExport().crew().kickoff(inputs={'data':table})
    df = pd.DataFrame(data=rs["data"][1:], columns=rs["data"][0])
    df.to_excel(file_name_save, index=False)

def train():
    """
    Train the crew for a given number of iterations.
    """
    
    inputs = {
        'data':'table'
    }
    try:
        LanguagesExport().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LanguagesExport().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        LanguagesExport().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
