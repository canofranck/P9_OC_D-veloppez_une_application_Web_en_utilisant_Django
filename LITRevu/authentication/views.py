from django.shortcuts import render, redirect
from . import forms
from django.conf import settings
from django.contrib.auth import login, logout


def signup_page(request):
    """Affiche et traite la page d'inscription des utilisateurs.

    Cette vue affiche le formulaire d'inscription des utilisateurs
    et traite les données soumises par l'utilisateur pour créer un nouveau compte.
    Si les données du formulaire sont valides, un nouveau compte utilisateur est créé
    et l'utilisateur est automatiquement connecté. Ensuite, l'utilisateur est redirigé
    vers l'URL de redirection après la connexion définie dans les paramètres.

    Args:
        request (HttpRequest): L'objet HttpRequest représentant la requête HTTP.

    Returns:
        HttpResponse: Une réponse HTTP renvoyant la page d'inscription avec le formulaire
        d'inscription des utilisateurs.

    """
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", context={"form": form})


def logout_user(request):
    """Déconnecte l'utilisateur actuellement authentifié.

    Cette vue permet à l'utilisateur actuellement authentifié de se déconnecter
    en invalidant sa session d'authentification. Une fois déconnecté, l'utilisateur
    est redirigé vers la page de connexion.

    Args:
        request (HttpRequest): L'objet HttpRequest représentant la requête HTTP.

    Returns:
        HttpResponseRedirect: Une redirection HTTP vers la page de connexion après
        la déconnexion de l'utilisateur.

    """
    logout(request)
    return redirect("login")


def upload_profile_photo(request):
    """Affiche le formulaire pour télécharger une photo de profil pour l'utilisateur actuel.

    Cette vue affiche un formulaire permettant à l'utilisateur actuellement authentifié
    de télécharger une nouvelle photo de profil. Si la méthode de requête est POST et que
    le formulaire est valide, la photo de profil de l'utilisateur est mise à jour avec le
    fichier téléchargé et l'utilisateur est redirigé vers la page d'accueil.

    Args:
        request (HttpRequest): L'objet HttpRequest représentant la requête HTTP.

    Returns:
        HttpResponse: Un objet HttpResponse représentant la réponse HTTP pour afficher
        le formulaire de téléchargement de la photo de profil.

    """
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == "POST":
        form = forms.UploadProfilePhotoForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(
        request, "authentication/upload_profile_photo.html", context={"form": form}
    )
