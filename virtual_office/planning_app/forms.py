from django import forms

from .models import Remind

class RemindForm(forms.ModelForm):

    class Meta:
        model = Remind

        fields = ['title', 'date', 'time', 'all_day', 'repeat', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'all_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Описание события'}),
        }

class SearchRemindTitleForm(forms.ModelForm):

    class Meta:
        model = Remind

        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
        }


class SearchRemindDateForm(forms.ModelForm):

    class Meta:
        model = Remind

        fields = ['date']

        widgets = {'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})}