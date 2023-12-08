from django import forms
from django.core.validators import RegexValidator


from .models import Diploma

number_valid = RegexValidator(
    r'^[0-9]+$', 'Введите корректное значение года')


class DiplomaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].empty_label = "Выберите тип документа"

    class Meta:
        model = Diploma

        fields = ['name', 'series', 'number', 'date_registration',
                  'registration_number', 'name_institution',
                  'year_of_start_edu', 'year_of_finish_edu',
                  'spiciality', 'spicialization', 'description']
        
        widgets = {
            'series': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Серия'}),
            'number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Номер'}),
            'date_registration': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'}),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Регистрационный номер'}),
            'name_institution': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Учебное заведение'}),
            'year_of_start_edu': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Начало обучения'}),
            'year_of_finish_edu': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Окончание обучения'}),
            'spiciality': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Специальность'}),
            'spicialization': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Специализация'}),
            'description': forms.Textarea(attrs={
                'class':'form-control',
                'placeholder': 'Дополнительные сведения'}),
                }