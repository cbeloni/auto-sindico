from pydantic import BaseModel

from util.datas_uteis import first_day_of_current_month, last_day_of_current_month


class ExtratoApiRequest(BaseModel):
    data_inicial: str = first_day_of_current_month()
    data_final: str = last_day_of_current_month()
    provider: str = "pluggy"