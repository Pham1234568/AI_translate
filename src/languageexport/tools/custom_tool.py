from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from typing import List, Any,Annotated
import pandas as pd
class SaveTranslationInput(BaseModel):
    data: List[List[Any]] = Field(..., description="2D list representing the full translation table. The first row is the header.",strict=True)
