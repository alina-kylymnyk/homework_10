from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class AuthorForm(forms.Form):
    fullname = forms.CharField(max_length=255, required=True)
    born_date = forms.CharField(max_length=255, required=False)
    born_location = forms.CharField(max_length=255, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

class QuoteForm(forms.Form):
    quote = forms.CharField(widget=forms.Textarea, required=True)
    tags = forms.CharField(required=False)  # Можна передати теги через кому
    author = forms.ChoiceField(choices=[])  # Цей вибір буде динамічним

    def __init__(self, *args, **kwargs):
        authors = kwargs.pop('authors', [])
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['author'].choices = [(str(author['_id']), author['fullname']) for author in authors]
