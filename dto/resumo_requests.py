from pydantic import BaseModel, Field
from util.datas_uteis import last_day_of_current_month, first_day_of_current_month

class ResumoRequest(BaseModel):
    data_inicial: str = Field(default_factory=first_day_of_current_month)
    data_final: str = Field(default_factory=last_day_of_current_month)
