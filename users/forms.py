from django import forms


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=20, label="Телефон")


class CodeForm(forms.Form):
    code = forms.CharField(max_length=4, label="Код")
