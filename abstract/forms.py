from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Abstract


class AbstractForm(forms.ModelForm):
    background = forms.CharField(widget=CKEditorUploadingWidget())
    objective = forms.CharField(widget=CKEditorUploadingWidget())
    method = forms.CharField(widget=CKEditorUploadingWidget())
    result = forms.CharField(widget=CKEditorUploadingWidget())
    conclusion = forms.CharField(widget=CKEditorUploadingWidget())
    name_author = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name of Authors ",
            }
        ),
        label="Name of Authors",
    )
    upload = forms.FileField(label='Upload the your write up')

    class Meta:
        model = Abstract
        fields = (
            "title",
            "name_author",
            "background",
            "objective",
            "method",
            "result",
            "conclusion",
            "event",
            "upload",
            "corresponding_author",
            "corresponding_author_phone",
            "corresponding_author_email",
        )



class AbstractEditForm(forms.ModelForm):
    background = forms.CharField(widget=CKEditorUploadingWidget())
    objective = forms.CharField(widget=CKEditorUploadingWidget())
    method = forms.CharField(widget=CKEditorUploadingWidget())
    result = forms.CharField(widget=CKEditorUploadingWidget())
    conclusion = forms.CharField(widget=CKEditorUploadingWidget())
    name_author = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name of Authors ",
            }
        ),
        label="Name of Authors",
    )
    upload = forms.FileField(label='Upload the your write up')

    class Meta:
        model = Abstract
        fields = (
            "title",
            "name_author",
            "background",
            "objective",
            "method",
            "result",
            "conclusion",
            "event",
            "upload",
            "corresponding_author",
            "corresponding_author_phone",
            "corresponding_author_email",
        )
