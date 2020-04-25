from django import forms

class PostAdminForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea,label='摘要',required=False)