from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):
    """Formulaire pour la création de tickets.

    Ce formulaire est utilisé pour créer de nouveaux tickets dans le système.
    Il inclut les champs titre, description et image.

    Attributes:
        description: Champ de texte multiligne pour la description du ticket.
    """

    title = forms.CharField(label="Titre", widget=forms.TextInput)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    image = forms.ImageField(label="Image :")

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    """Formulaire pour la création de critiques.

    Ce formulaire est utilisé pour créer de nouvelles critiques associées à
    un ticket. Il inclut les champs titre, notation et commentaire.

    Attributes:
        rating: Champ caché pour la notation de la critique.
        body: Champ de texte multiligne pour le commentaire de la critique.
    """

    rating = forms.IntegerField(
        label="Notation", widget=forms.HiddenInput(), required=True
    )
    body = forms.CharField(label="Commentaire", widget=forms.Textarea)
    headline = forms.CharField(label="Titre", widget=forms.TextInput)

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]


class FollowUsersForm(forms.ModelForm):
    """Formulaire pour suivre d'autres utilisateurs.

    Ce formulaire est utilisé pour permettre à un utilisateur de suivre un
    autre utilisateur.
    Il inclut un champ pour entrer le nom d'utilisateur à suivre.

    Attributes:
        follows: Champ de texte pour saisir le nom d'utilisateur à suivre.
    """

    follows = forms.CharField(
        label="Nom d'utilisateur à suivre",
        max_length=128,
        widget=forms.TextInput(
            attrs={"placeholder": "Entrez le nom d'utilisateur à suivre"}
        ),
    )

    class Meta:
        model = User
        fields = ["follows"]

    def clean_follows(self):
        """Valide le nom d'utilisateur à suivre.

        Cette méthode vérifie si le nom d'utilisateur entré existe dans la
        base de données.
        Si l'utilisateur n'existe pas, une ValidationError est levée.

        Returns:
            str: Le nom d'utilisateur à suivre, s'il est valide.
        Raises:
            forms.ValidationError: Si l'utilisateur à suivre n'existe pas.
        """
        follows = self.cleaned_data["follows"]

        if not User.objects.filter(username=follows):
            raise forms.ValidationError(
                "Cet utilisateur n'est pas reconnu dans la base de donnée."
            )

        return follows
