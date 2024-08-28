from django.forms import ModelForm, CharField, TextInput
from .models import Quote

# class QuoteForm(ModelForm):
#     author = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
#     quote = CharField(min_length=10, max_length=500, required=True, widget=TextInput())

#     class Meta:
#         model = Quote
#         fields = ['author', 'quote']
