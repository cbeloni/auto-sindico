from pydantic import BaseModel
from util.datas_uteis import last_day_of_current_month, first_day_of_current_month

class ResumoRequest(BaseModel):
    data_inicial: str = first_day_of_current_month()
    data_final: str = last_day_of_current_month()