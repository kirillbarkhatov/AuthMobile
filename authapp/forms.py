from django import forms

class InviteCodeForm(forms.Form):
    code = forms.CharField(max_length=6, label="Код приглашения")
