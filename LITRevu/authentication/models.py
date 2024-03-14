from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle représentant un utilisateur dans le système.

    Ce modèle étend le modèle d'utilisateur par défaut de Django:
    (`AbstractUser`)
    pour inclure des champs et des fonctionnalités supplémentaires, tels
    qu'une photo de profil.

    Attributs:
        profile_photo (ImageField): La photo de profil de l'utilisateur.
            Ce champ stocke la photo de profil de l'utilisateur.
    """

    profile_photo = models.ImageField(verbose_name="photo de profil")
