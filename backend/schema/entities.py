from sqlmodel import SQLModel, Field
from typing import Optional

"""Modèles SQLModel pour la base de données"""
class AnalysisCache(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    input_hash: str
    result: str
