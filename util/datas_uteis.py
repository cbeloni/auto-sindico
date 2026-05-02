from datetime import datetime, timedelta

meses_portugues = {
    'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
    'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto',
    'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
}

def ultimo_dia_mes_atual():
    today = datetime.now()
    next_month = today.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def first_day_of_current_month(strftime_format: str = '%d/%m/%Y'):
    today = datetime.today()
    return today.replace(day=1).strftime(strftime_format)

def last_day_of_previous_month():
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    return last_day_of_previous_month.strftime('%d/%m/%Y')

def last_day_of_current_month(strftime_format: str = '%d/%m/%Y'):
    today = datetime.today()
    next_month = today.replace(day=28) + timedelta(days=4)
    return (next_month - timedelta(days=next_month.day)).strftime(strftime_format)

def format_date_to_ddmmyyyy(date_obj: datetime) -> str:
    """Convert datetime object to 'dd/mm/yyyy' format"""
    return date_obj.strftime('%d/%m/%Y')
