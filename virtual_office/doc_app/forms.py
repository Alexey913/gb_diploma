from django import forms
from django.core.validators import RegexValidator


from .models import Spouce, Children, DriverCategoryShedule, Passport, Inn, Snils, DriverLicense, ForeignPassport, MilitaryTicket, DocTemplate

number_valid = RegexValidator(
    r'^[0-9]+$', 'Введите корректное значение номера')


class DocForm(forms.ModelForm):

    class Meta:
        model = DocTemplate

        fields = ['series', 'number', 'date_registration',
                  'id_inspection', 'name_inspection']

        widgets = {
            'series': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Серия'}),
            'number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Номер'}),
            'date_registration': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'}),
            'id_inspection': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Код подразделения'}),
            'name_inspection': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Название подразделения'}),
        }


class PassportForm(DocForm):

    class Meta(DocForm.Meta):
        model = Passport
        fields = DocForm.Meta.fields + \
            ['adress_registration', 'adress_reg_eq_place', 'date_adress_reg']
        widget_list = {
            'adress_registration': forms.TextInput(attrs={'class': 'form-control', 
                                                          'placeholder': 'Адрес регистрации'}),
            'adress_reg_eq_place': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_adress_reg': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        widgets = DocForm.Meta.widgets
        for k, v in widget_list.items():
            widgets[k] = v


class InnForm(DocForm):

    class Meta(DocForm.Meta):
        model = Inn
        fields = ['inn'] + DocForm.Meta.fields
        widgets = DocForm.Meta.widgets
        widgets['inn'] = forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'ИНН',
                                                'title': 'Введите корректный ИНН'})


class SnilsForm(DocForm):

    class Meta(DocForm.Meta):
        model = Snils
        widgets = DocForm.Meta.widgets
        exclude = ['series']
        

class DriverLicenseForm(DocForm):

    class Meta(DocForm.Meta):
        model = DriverLicense
        fields = DocForm.Meta.fields + \
            ['date_end_action', 'categories', 'date_start_expirience', 'special_marks']
        widget_list = {
            'date_end_action': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'date_start_expirience': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'special_marks': forms.TextInput(attrs={'class':'form-control',
                                                   'placeholder': 'Особые отметки'}),
            'categories': forms.CheckboxSelectMultiple(),
        }
        widgets = DocForm.Meta.widgets
        for k, v in widget_list.items():
            widgets[k] = v


class DriverCategoryEditForm(forms.ModelForm):
    
    class Meta(DocForm.Meta):
        model = DriverCategoryShedule
        fields = ['date_begin', 'date_end', 'note']
        widgets = {
            'date_begin': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'note': forms.TextInput(attrs={'class':'form-control',
                                                   'placeholder': 'Отметка о категории'}),
        }

class DriverCategoryAddForm(DriverCategoryEditForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Не выбрана"

    class Meta(DriverCategoryEditForm.Meta):
        model = DriverCategoryShedule
        fields = ['category'] + DriverCategoryEditForm.Meta.fields
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date_begin': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'note': forms.TextInput(attrs={'class':'form-control',
                                                   'placeholder': 'Отметка о категории'}),
        }


class MilitaryTicketForm(DocForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Не указана"

    class Meta(DocForm.Meta):
        model = MilitaryTicket
        fields = DocForm.Meta.fields + \
            ['category', 'speciality', 'description']
        widget_list = {
            'speciality': forms.TextInput(attrs={'class':'form-control',
                                                 'placeholder': 'Военная специальность'}),
            'description': forms.Textarea(attrs={'class':'form-control',
                                                 'placeholder': 'Дополнительные сведения'}),
        }
        widgets = DocForm.Meta.widgets
        for k, v in widget_list.items():
            widgets[k] = v

class ForeignPassportForm(DocForm):

    class Meta(DocForm.Meta):
        model = ForeignPassport
        fields = DocForm.Meta.fields + \
            ['date_end_action', 'foreign_name', 'foreign_surname']
        widget_list = {
            'date_end_action': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'foreign_name': forms.TextInput(attrs={'class':'form-control',
                                                   'placeholder': 'Имя латиницей'}),
            'foreign_surname': forms.TextInput(attrs={'class':'form-control',
                                                     'placeholder': 'Фамилия латиницей'})
        }
        widgets = DocForm.Meta.widgets
        for k, v in widget_list.items():
            widgets[k] = v

class ChildrenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].empty_label = "Не указан"

    class Meta:
        model = Children
        fields = ['surname', 'name', 'patronymic', 'birthday', 'gender']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SpouceForm(ChildrenForm):

    class Meta(Children.Meta):
        model = Spouce
        fields = ChildrenForm.Meta.fields + ['date_marriage']

        widgets = ChildrenForm.Meta.widgets
        widgets['date_marriage'] = forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})