import hashlib
import os
from django.shortcuts import render, HttpResponse

import logging

from .forms import UserForm

from .models import User

def pass_to_hash(password: str) -> int:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 1_000_000)
    return key, salt

def check_phone_mail(input_data: str) -> str:
    if '@' in input_data:
        return 'email'
    elif input_data.isdigit():
        return 'phone'
    return 'error'


def check_user(email):
    if User.query.filter((User.email == email)).first():
        return True
    return False


def check_login(email, password):
    if check_user(email):
        extention_user = User.query.filter((User.email == email)).first()
        user_salt = extention_user.salt
        user_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user_salt, 1_000_000)
        if user_password == extention_user.password:
            return True
    return False



def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # for k, v in data.items():
            #     if v == "":
            #         data[k] = None 
           
            # name = data['name']
            # surname = data['surname']
            # patronymic = data['patronymic']
            phone_email = data['phone_email']
            hash_password, salt = pass_to_hash(data['password'])
            confirm_password, confirm_salt = pass_to_hash(data['confirm_password'])
            # birthday = data['birthday']
            # gender = data['gender']
            # birth_place = data['birth_place']
            # place_residense = data['place_residense']

            email = phone = None
            # if jdate > ldate:
            #     raise form.ValidationError('Leaving Date must be after Joining Date')
            check_result = check_phone_mail(phone_email)
            if check_result == 'phone':
                phone = phone_email
            elif check_result == 'email':
                email = phone_email
            elif check_result == 'error':
                form = UserForm()
                return render(request, 'user_app/registration.html', {'form':form})
            #флэш сообщение, что необходимо ввести корректный телефон или e-mail или пароль неверный

            user = User(phone=phone, email=email, salt=salt,
                        hash_password=hash_password)
            user.save()
            logger.info(f'Создан пользователь {user.pk} - {user}')
            return HttpResponse('Создан пользователь')
    else:
        form = UserForm()
        return render(request, 'user_app/registration.html', {'form':form})


# @app.route('/registration/', methods=['GET', 'POST'])
# def registration():
#     form = RegistrationForm()
#     if request.method == 'POST' and form.validate():
#         name = form.name.data
#         email = form.email.data
#         password = form.password.data
#         existing_user = User.query.filter((User.name == name) | (User.email == email)).first()
#         # existing_user = User.query.filter_by(name=user)
#         if existing_user:
#             error_msg = 'Пользователь с таким именем или email уже существует!'
#             form.name.errors.append(error_msg)
#             return render_template("registration.html", form=form, title='Регистрация')
#         user = User(name=name, email=email, password=password)
#         db.session.add(user)
#         db.session.commit()
#         return render_template("registration_sucsess.html", title='Регистрация завершена')
#     return render_template("registration.html", form=form, title='Регистрация')




# Логгер перенести в отдельный пакет
logger = logging.getLogger(__name__) 

def authorization(request):
    logger.info('Index page accessed')
    return HttpResponse("Hello, world!")

def about(request):
    try:
        # some code that might raise an exception
        result = 1 / 0
    except Exception as e:
        logger.exception(f'Error in about page: {e}')
        return HttpResponse("Oops, something went wrong.") 
    else:
        logger.debug('About page accessed')
        return HttpResponse("This is the about page.")