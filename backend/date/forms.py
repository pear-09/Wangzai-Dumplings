from django import forms


class CreateDateForm(forms.Form):
    user_id = forms.IntegerField(required=False)
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    time = forms.CharField(required=False)


