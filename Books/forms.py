from django.forms import ModelForm
from .models import Books

class BooksForm(ModelForm):
    class Meta:
        model = Books
        fields = '__all__'
