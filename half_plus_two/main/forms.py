from django.forms import ModelForm, fields
from .models import Request

class RequestsFormField(ModelForm):
    class Meta:
        model = Request
        fields = ['request']