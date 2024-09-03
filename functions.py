def get_zodiac_sign(day, month):
    zodiac_signs = [
        (120, 'Козерог'), (218, 'Водолей'), (320, 'Рыбы'), 
        (420, 'Овен'), (521, 'Телец'), (621, 'Близнецы'),
        (722, 'Рак'), (823, 'Лев'), (923, 'Дева'),
        (1023, 'Весы'), (1122, 'Скорпион'), (1222, 'Стрелец'), 
        (1231, 'Козерог')
    ]
    
    date_num = month * 100 + day
    for end_date, sign in zodiac_signs:
        if date_num <= end_date:
            return sign
    return 'Козерог'
