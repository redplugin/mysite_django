from django import forms

from blog.models import Post, Comment


class CreatePostForm(forms.ModelForm):
    # title = forms.CharField(label='Title')
    # content = forms.CharField(label='Content')

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        # fields = '__all__'
        # exclude = ['created_at', 'updated_at']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'author']


