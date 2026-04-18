from pydantic import BaseModel, Field

from util.datas_uteis import first_day_of_current_month, last_day_of_current_month


class ExtratoApiRequest(BaseModel):
    data_inicial: str = Field(default_factory=lambda: first_day_of_current_month('%Y-%m-%d'))
    data_final: str = Field(default_factory=lambda: last_day_of_current_month('%Y-%m-%d'))
    provider: str = "pluggy"
    gravar: bool = True
