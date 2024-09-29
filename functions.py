import requests
from bs4 import BeautifulSoup

def get_zodiac_sign(day, month):
    zodiac_signs = [
        (120, 'Козерог', 10), (218, 'Водолей', 11), (320, 'Рыбы', 12), 
        (420, 'Овен', 1), (521, 'Телец', 2), (621, 'Близнецы', 3),
        (722, 'Рак', 4), (823, 'Лев', 5), (923, 'Дева', 6),
        (1023, 'Весы', 7), (1122, 'Скорпион', 8), (1222, 'Стрелец', 9), 
        (1231, 'Козерог', 10)
    ]
    
    date_num = month * 100 + day
    for end_date, sign, sign_number in zodiac_signs:
        if date_num <= end_date:
            return sign, sign_number
    return 'Козерог', 10


def get_horoscope_by_day(zodiac_sign: int, day: str):
    # Проверка, является ли запрос на конкретный день (архив или текущий)
    if "-" not in day:
        # Запрос на текущий или предопределенный день (например, today, yesterday)
        url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign}"
    else:
        # Запрос на архивную дату
        day = day.replace("-", "")
        url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign={zodiac_sign}&laDate={day}"
    
    # Выполняем запрос
    res = requests.get(url)
    
    # Парсим страницу
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # Извлекаем данные гороскопа
    data = soup.find('div', attrs={'class': 'main-horoscope'})
    if data and data.p:
        return data.p.text
    return "Гороскоп не найден."


def get_horoscope_by_week(zodiac_sign: int):
    # Запрос на недельный гороскоп
    url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-weekly.aspx?sign={zodiac_sign}"
    res = requests.get(url)
    
    # Парсим страницу
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # Извлекаем данные гороскопа
    data = soup.find('div', attrs={'class': 'main-horoscope'})
    if data and data.p:
        return data.p.text
    return "Гороскоп не найден."


def get_horoscope_by_month(zodiac_sign: int):
    url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-monthly.aspx?sign={zodiac_sign}"
    res = requests.get(url)
    
    # Парсим страницу
    soup = BeautifulSoup(res.content, 'html.parser')
    # Извлекаем данные гороскопа
    data = soup.find('div', attrs={'class': 'main-horoscope'})
    if data and data.p:
        return data.p.text
    return "Гороскоп не найден."


# Пример использования
if __name__ == "__main__":

    day = 29
    month = 9
    zodiac_sign, zodiac_sign_number = get_zodiac_sign(day, month)

    print(f"Знак зодиака: {zodiac_sign}, Номер знака: {zodiac_sign_number}")
    
    day = "today"
    daily_horoscope = get_horoscope_by_day(zodiac_sign_number, day)
    print(f"Гороскоп на день для {zodiac_sign}: \n{daily_horoscope}\n")

    # weekly_horoscope = get_horoscope_by_week(zodiac_sign_number)
    # print(f"Гороскоп на неделю для {zodiac_sign}: \n{weekly_horoscope}\n")

    # monthly_horoscope = get_horoscope_by_month(zodiac_sign_number)
    # print(f"Гороскоп на месяц для {zodiac_sign}: \n{monthly_horoscope}")
