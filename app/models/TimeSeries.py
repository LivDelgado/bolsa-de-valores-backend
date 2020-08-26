from typing import List, Optional
from pydantic import BaseModel

class TimeEntry(BaseModel):
    data: Optional[str] = None
    open_value: Optional[str] = None
    high_value: Optional[str] = None
    low_value: Optional[str] = None
    close_value: Optional[str] = None
    volume_value: Optional[str] = None

class BovespaTimeSeries(BaseModel):
    ultima_atualizacao: Optional[str] = None
    simbolo: Optional[str] = None
    atualizacoes: List[TimeEntry] = []
