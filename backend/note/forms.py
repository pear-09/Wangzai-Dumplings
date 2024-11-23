from django import forms
from .models import Note, Tag

class CreateNoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'content', 'folder_id', 'tags']

     # 设置字段的默认值和空值处理
    title = forms.CharField(required=False, initial="新建笔记")  # 默认值为 "新建笔记"
    content = forms.CharField(required=False, widget=forms.Textarea)  # 内容字段可选

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

class FolderQueryForm(forms.Form):
    folder_id = forms.IntegerField()  # 笔记 ID

    class Meta:
        model = Note
        fields = ['folder_id']