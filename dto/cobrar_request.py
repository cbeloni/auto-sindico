from pydantic import BaseModel
from datetime import datetime, timedelta
from util.datas_uteis import meses_portugues

def get_mes():
    mes = meses_portugues[datetime.today().strftime("%B")]
    return mes

def get_ano():
    today = datetime.today()
    return str(today.year)

class CobrarRequest(BaseModel):
    mes: str = get_mes()
    ano: str = get_ano()
        
        