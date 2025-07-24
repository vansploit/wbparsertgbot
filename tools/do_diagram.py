import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from datetime import datetime

def create_and_price_chart(prices, dates, title="График цен"):

    # Преобразуем даты в datetime если они строки
    if isinstance(dates[0], str):
        dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
    
    # Создаем DataFrame для удобства
    df = pd.DataFrame({'Дата': dates, 'Цена': prices})
    df.sort_values('Дата', inplace=True)
    
    # Создаем график
    plt.figure(figsize=(10, 6))
    plt.plot(df['Дата'], df['Цена'], marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Сохраняем график в буфер
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Закрываем график
    plt.close()
    return buf