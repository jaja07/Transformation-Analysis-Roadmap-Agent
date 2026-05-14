from sqlmodel import SQLModel, Field
from typing import Optional


class AnalysisCache(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    input_hash: str
    result: str
