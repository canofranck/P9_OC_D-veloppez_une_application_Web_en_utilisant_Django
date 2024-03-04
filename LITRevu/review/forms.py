from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()
class TicketForm(forms.ModelForm):
    description = forms.CharField(label='description', widget=forms.Textarea)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        
class ReviewForm(forms.ModelForm):
  
    rating = forms.IntegerField(label='Notation', widget=forms.HiddenInput(), required=True)
    body = forms.CharField(label='comments', widget=forms.Textarea)
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        
class FollowUsersForm(forms.ModelForm):
    follows = forms.CharField(label="",
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le nom d\'utilisateur à suivre'}),
    )

    class Meta:
        model = User
        fields = ['follows']

    def clean_follows(self):
        follows = self.cleaned_data['follows']
        
        if not User.objects.filter(username=follows):
            raise forms.ValidationError("Cet utilisateur n'est pas reconnu dans la base de donnée.")

        return follows
