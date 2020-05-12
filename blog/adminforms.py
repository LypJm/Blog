from django import forms
from .models import Category,Tag,Post
from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostAdminForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea,label='摘要',required=False)
    category=forms.ModelChoiceField(queryset=Category.objects.all(),
                                    widget=autocomplete.ModelSelect2(url='category-autocomplete'),
                                    label='分类')
    tags=forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                       widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
                                       label='标签')
    # content=forms.CharField(widget=CKEditorWidget(),label='正文',required=True)
    content=forms.CharField(widget=forms.HiddenInput(),required=False)

    content_ck=forms.CharField(widget=CKEditorUploadingWidget(),label='正文',required=False)
    content_md=forms.CharField(widget=forms.Textarea(),label='正文',required=False)

    #对Form做初始化，initial是Form中各字段初始化的值，instance时当前的模型的实例，例如正在编辑一篇文章，则为当前文章的实例
    def __init__(self,instance=None,initial=None,**kwargs):
        initial=initial or ()
        if instance:
            if instance.is_md:
                initial['content_md']=instance.content
            else:
                initial['content_ck']=instance.content
        super().__init__(instance=instance,initial=initial,**kwargs)

    #对用户提交的内容做处理，判断使用哪个编辑格式，Markdown或ckeditor
    def clean(self):
        is_md=self.cleaned_data.get['is_md']
        if is_md:
            content_field_name='content_md'
        else:
            content_field_name='content_ck'
        content=self.cleaned_data.get[content_field_name]
        if not content:
            self.add_error(content_field_name,'必填项')
            return

        self.cleaned_data['content']=content
        return super().clean()

    class Media:
        js=('js/post_editor.js',)

    class Meta:
        model=Post
        fields=('category','tags','title','description','content','status')