from typing import List, Optional
from pydantic import BaseModel

class EnterpriseInfo(BaseModel):
    symbol: Optional[str] = None
    open_value: Optional[float]
    high_value: Optional[float]
    low_value: Optional[float]
    price_value: Optional[float]
    volume_value: Optional[float]
    data: Optional[str] = None
    previous_close: Optional[float]
    change: Optional[str]
    change_percentage: Optional[str]

class TimeEntry(BaseModel):
    data: Optional[str] = None
    value: Optional[float]

class BovespaTimeSeries(BaseModel):
    informacoes: Optional[EnterpriseInfo]
    atualizacoes: List[TimeEntry] = []