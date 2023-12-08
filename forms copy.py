from django import forms

import datetime


class UserForm(forms.Form):
    # name = forms.CharField(max_length=50, min_length=2, label='Имя *',
    #                        error_messages={'required': 'Введите корректное имя'},
    #                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    
    # surname = forms.CharField(max_length=50, min_length=2, label='Фамилия *',
    #                           error_messages={'required': 'Введите корректную фамилию'}, 
    #                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    
    # patronymic = forms.CharField(max_length=50, min_length=4, label='Отчество', required=False,
    #                              error_messages={'reequired': 'Введите корректное отчество'},
    #                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}))
    
    phone_email = forms.CharField(max_length=50, min_length=6, label='Телефон / E-mail *',
                                  error_messages={'required': 'Обязательно введите телефон или e-mail'},
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон или e-mail'}))
                                                        
    password = forms.CharField(max_length=50, min_length=6, label='Пароль *',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    
    confirm_password = forms.CharField(max_length=50, min_length=6, label='Подтверждение пароля *',
                                       error_messages={'required': 'Пароли должны совпадать'},
                                       widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))

    # birthday = forms.DateField(label='Дата рождения', required=False,
    #                            widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date'}))
    
    # gender = forms.ChoiceField(label='Пол', required=False, choices=[('U', 'Не указан'), ('M', 'Мужской'), ('F','Женский')])

    # birth_place = forms.CharField(min_length=3, label='Место рождения', required=False,
    #                               error_messages={'required': 'Обязательно укажите регион и населенный пункт'},
    #                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес рождения'}))

    # place_residense = forms.CharField(min_length=3, label='Адрес проживания', required=False,
    #                                   error_messages={'required': 'Обязательно укажите регион, населенный пункт, улицу и дом'},
    #                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес местожительства'}))
    
    def clean_phone_email(self):
        phone_email: str = self.cleaned_data['phone_email']
        if not '@' in phone_email and not phone_email.isdigit():
            raise forms.ValidationError('Введите корректный номер телефона или адрес электронной почты')
        return phone_email

    # def clean_password(self):
    #     password: str = self.cleaned_data['password']
    #     if not any(map(str.isdigit, password)) and\
    #        not any(map(str.isalpha, password)) and\
    #        not any(map(str.islower, password)):
    #         raise forms.ValidationError('Пароль должен содержать цифры, а также заглавные и строчные буквы')
    #     return password
    
    # def clean_confirm_password(self):
    #     password: str = self.cleaned_data['password']
    #     confirm_password: str = self.cleaned_data['confirm_password']
    #     if password != confirm_password:
    #         raise forms.ValidationError('Пароли должны совпадать')
    #     return confirm_password


# email =
# forms.EmailField(widget=forms.EmailInput(attrs={'class':
# 'form-control',
# 'placeholder': 'user@mail.ru'}))
# age = forms.IntegerField(min_value=18,
# widget=forms.NumberInput(attrs={'class': 'form-control'}))
# height =
# forms.FloatField(widget=forms.NumberInput(attrs={'class':
# 'form-control'}))
# is_active = forms.BooleanField(required=False,
# widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
# birthdate = forms.DateField(initial=datetime.date.today,
# widget=forms.DateInput(attrs={'class': 'form-control'}))
# gender = forms.ChoiceField(choices=[('M', 'Male'), ('F',
# 'Female')],
# widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
# message =
# forms.CharField(widget=forms.Textarea(attrs={'class':
# 'form-control'}))
# 13
