# folder/forms.py
from django import forms
from .models import Folder

class CreateFolderForm(forms.Form):
    name = forms.CharField(max_length=255)
    folder_type = forms.CharField(max_length=50, required=False)
    parent_folder_id = forms.IntegerField(required=False)
