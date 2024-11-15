from django import forms
from .models import Note, Tag

class CreateNoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'content', 'folder_id', 'tags']

class UpdateNoteForm(forms.ModelForm):
    note_id = forms.IntegerField(required=True, error_messages={'required': 'note_id 不能为空'})
    content = forms.CharField(required=True, error_messages={'required': 'content 不能为空'})
    class Meta:
        model = Note
        fields = ['note_id', 'content']

class NoteQueryForm(forms.Form):
    note_id = forms.IntegerField()  # 笔记 ID

    class Meta:
        model = Note
        fields = ['note_id']
