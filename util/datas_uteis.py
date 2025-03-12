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