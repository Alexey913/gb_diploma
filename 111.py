# import os
# from string import ascii_lowercase as low_alpha
# from string import ascii_uppercase as up_alpha

# password = ':::::::'

# print(any(map(str.isdigit, password)))
# print(any(map(lambda x: x in low_alpha, password)))
# print(any(map(lambda x: x in up_alpha, password)))

# if not any(map(str.isdigit, password)) or\
#     not any(map(lambda x: x in low_alpha, password)) or\
#     not any(map(lambda x: x in up_alpha, password)):
#     print('Исключение')
# else:
#     print('Передаем пароль')

# print('-------')
# j = None
# if j:
#     print('+')
# else:
#     print('=')
# print('Email')
# def check_phone_email(input_data: str) -> bool:
#     if input_data.isdigit():
#         return True
#     else:
#         parts_of_email = input_data.split('.')
#         print(parts_of_email)
#         if len(parts_of_email) == 2 and '@' in parts_of_email[0] and not parts_of_email[0].endswith('@') and parts_of_email[1]:
#             return True
#     return False

# phone_email = 'al913@tu'
# print(check_phone_email(phone_email))

# print(type(os.urandom(32)))

# class Aa:

#     def __init__(self, k: str, b: str, j: str) -> None:
#         self.k = k
#         self.j = j
#         self.b = b

#     def __str__(self) -> str:
#         r = vars(self)
#         return (', '.join("%s: %s" % item for item in r.items()))
    

# aaaa = Aa('l', 'c', 'k')
# print(aaaa)
# print(check_phone_email.__name__)


import numpy as np
from datetime import datetime, timedelta
from dateutil import rrule

# неделя/день
end_date_year = int(str(np.datetime64(str(datetime.now().year))+ np.timedelta64(100,'Y')))
end_date=datetime(year=end_date_year, month=1, day=1)
current_day = datetime.now()
delta = timedelta(days=7)
# while current_day < end_date:
#     print(current_day)
#     current_day += delta


for dt in rrule.rrule(rrule.YEARLY, dtstart=current_day, until=end_date):
    print(dt)
print('-\n-\n-\n-\n-\n-\n-\n')
for dt in rrule.rrule(rrule.DAILY, dtstart=current_day, until=end_date):
    print(dt)
print('-\n-\n-\n-\n-\n-\n-\n')
for dt in rrule.rrule(rrule.WEEKLY, dtstart=current_day, until=end_date):
    print(dt)
print('-\n-\n-\n-\n-\n-\n-\n')
for dt in rrule.rrule(rrule.MONTHLY, dtstart=current_day, until=end_date):
    print(dt)


    # if remind.repeat == 'Каждый день':

    #     delta = timedelta(days=1)
    # elif remind.repeat == 'Каждую неделю':
    #     delta = timedelta(weeks=1)
    # elif remind.repeat == 'Каждый месяц':
    #     delta = 0
    #     month = datetime.today().month
    # elif remind.repeat == 'Каждый год':
    #     delta = 0