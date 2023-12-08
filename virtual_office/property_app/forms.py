from django import forms

from .models import Property, Transport, Realty

class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property

        fields = ['date_registration', 'description']
        
        widgets = {
            'date_registration': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={
                'class':'form-control', 'placeholder': 'Описание'}),
                }

class TransportForm(PropertyForm):

    class Meta(PropertyForm.Meta):
        model = Transport

        fields = ['type_property', 'brand', 'model', 'year_release',
                  'power_engine', 'weigth', 'carrying'] + PropertyForm.Meta.fields

        widget_list = {
            'brand': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Марка'}),
            'model': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Модель'}),
            'year_rlease': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Год выпуска'}),
            'power_engine': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Мощность двигателя'}),
            'weigth': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Масса'}),    
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Регистрационный номер'}),
            'carrying': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Грузоподъемность'}),
                }
        
        widgets = PropertyForm.Meta.widgets
        for k, v in widget_list.items():
            widgets[k] = v


class RealtyForm(PropertyForm):
    
    class Meta(PropertyForm.Meta):
        model = Realty

        fields = ['type_property', 'cadastral_number', 'cadastral_cost',
                  'adress', 'area'] + PropertyForm.Meta.fields

        widget_list = {
            'cadastral_number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Кадастровый номер'}),
            'cadastral_cost': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Кадастровая стоимость'}),
            'adress': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Адрес объекта'}),
            'area': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Площадь объекта'}),
                }
        
        widgets = PropertyForm.Meta.widgets
        for k, v in widget_list.items():
            widgets[k] = v