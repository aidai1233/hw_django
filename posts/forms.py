from django import forms
from posts.models import Comment, Post, Tag


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField(max_length=100)
    content = forms.CharField()


def clean_title(self):
    title = self.cleaned_data('title')
    if title.lower() == "python":
        raise forms.ValidationError("Такое название нельзя!")
    else:
        return title


def clean(self):
    cleaned_data = super().clean()
    title = cleaned_data.get('title')
    content = cleaned_data.get('content')
    if title.lower() == content.lower():
        raise forms.ValidationError("title and content must be different")


class PostForm2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.lower() == "python":
            raise forms.ValidationError("Такое название нельзя!")
        else:
            return title

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title.lower() == content.lower():
            raise forms.ValidationError("title and content must be different")


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False, max_length=100, min_length=2, widget=forms.TextInput(
            attrs={'placeholder': 'Search',
                   'class': 'form-control',
                   }
        )
    )
    tag = forms.ModelMultipleChoiceField(
        required=False, queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    orderings = (
        ('created_at', 'По дате создания'),
        ('-created_at', 'По дате создания (по убыванию)'),
        ('title', 'По названию'),
        ('-itle', 'По названию (по убыванию)'),
        ('rate', 'По рейтингу'),
        ('-rate', 'По рейтингу (по убыванию)'),
    )

    ordering = forms.ChoiceField(required=False, choices=orderings, widget=forms.RadioSelect)








