from django import forms
from django.forms import ModelForm

class IsiForm(ModelForm):
    isi = forms.Textarea()