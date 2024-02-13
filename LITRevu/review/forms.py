from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()
class TicketForm(forms.ModelForm):
    description = forms.CharField(label='description', widget=forms.Textarea)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']