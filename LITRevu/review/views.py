from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from authentication.models import User
from . import forms, models
from django.contrib import messages
from django.db.models import Q
from itertools import chain

# from django.db.models import Avg

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def home(request):
    current_user_id = request.user.id
    tickets = models.Ticket.objects.filter(
        Q(
            user_id__in=models.UserFollows.objects.filter(
                user_id=current_user_id
            ).values("followed_user_id")
        )
        | Q(user_id=current_user_id)
    )

    reviews = models.Review.objects.filter(
        Q(
            user_id__in=models.UserFollows.objects.filter(
                user_id=current_user_id
            ).values("followed_user_id")
        )
        | Q(user_id=current_user_id)
        | Q(ticket__user_id=current_user_id)
    )

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    paginator = Paginator(tickets_and_reviews, 3)  # Nombre d'éléments par page

    page_number = request.GET.get("page")
    try:
        tickets_and_reviews = paginator.page(page_number)
    except PageNotAnInteger:
        tickets_and_reviews = paginator.page(1)
    except EmptyPage:
        tickets_and_reviews = paginator.page(paginator.num_pages)

    return render(
        request,
        "review/home.html",
        context={"tickets_and_reviews": tickets_and_reviews},
    )


@login_required
def create_ticket(request):
    """Affiche le formulaire de création de ticket.

    Cette fonction affiche le formulaire permettant à l'utilisateur
    de créer un nouveau ticket.

    Args:
        request (HttpRequest): L'objet de requête HTTP Django.

    Returns:
        HttpResponse: La réponse HTTP contenant le formulaire de création de
                      ticket.

    Raises:
        Aucune exception n'est levée.
    """
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")
    return render(request, "review/create_ticket.html", context={"form": form})


@login_required
def edit_ticket(request, ticket_id):
    """Affiche le formulaire d'édition de ticket.

    Cette fonction affiche le formulaire permettant à l'utilisateur
    de modifier un ticket existant.

    Args:
        request (HttpRequest): L'objet de requête HTTP Django.
        ticket_id (int): L'identifiant du ticket à modifier.

    Returns:
        HttpResponse: La réponse HTTP contenant le formulaire d'édition de
        ticket.

    Raises:
        Aucune exception n'est levée.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.TicketForm(instance=ticket)
    if ticket:
        if ticket.user != request.user:
            return redirect("error_change_ticket", ticket.id)
        else:
            if request.method == "POST":
                form = forms.TicketForm(
                    request.POST, request.FILES, instance=ticket
                )
                if form.is_valid():
                    ticket_save = form.save(commit=False)
                    ticket_save.user = request.user
                    ticket_save.save()
                    return redirect("edit_post")
    return render(
        request,
        "review/edit_ticket.html",
        context={"ticket": ticket, "form": form},
    )


@login_required
def delete_ticket(request, ticket_id):
    """Supprime un ticket.

    Cette fonction permet à un utilisateur connecté de supprimer un ticket
    spécifié s'il est l'auteur du ticket. Si l'utilisateur n'est pas l'auteur
    du ticket, il sera redirigé vers une page d'erreur appropriée.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.
        ticket_id (int): L'identifiant du ticket à supprimer.

    Returns:
        HttpResponseRedirect: Redirige l'utilisateur vers la page d'accueil ou
        une autre page appropriée après la suppression du ticket.

    Raises:
        Http404: Si le ticket spécifié n'existe pas.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    # Vérifiez si l'utilisateur actuel est bien celui qui a créé le ticket
    if ticket.user != request.user:
        return redirect(
            "error_delete_ticket", ticket.id
        )  # Redirigez vers une page d'erreur appropriée

    if request.method == "POST":
        ticket.delete()
        return redirect("home")
    return render(
        request, "review/delete_ticket.html", context={"ticket": ticket}
    )


@login_required
def error_delete_ticket(request, ticket_id):
    """Affiche une erreur lors de la suppression d'un ticket.

    Cette fonction affiche une page d'erreur indiquant à l'utilisateur
    qu'il n'est pas autorisé à supprimer le ticket spécifié.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.
        ticket_id (int): L'identifiant du ticket pour lequel la suppression
        a échoué.

    Returns:
        HttpResponse: La réponse HTTP affichant la page d'erreur avec le
        ticket concerné.

    Raises:
        Http404: Si le ticket spécifié n'existe pas.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(
        request, "review/error_delete_ticket.html", context={"ticket": ticket}
    )


@login_required
def ticket_detail(request, ticket_id):
    """Affiche les détails d'un ticket.

    Cette fonction récupère les détails d'un ticket spécifié à partir de son
    identifiant et les affiche sur une page dédiée.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.
        ticket_id (int): L'identifiant du ticket à afficher en détail.

    Returns:
        HttpResponse: La réponse HTTP affichant les détails du ticket sur la
        page de détail.

    Raises:
        Http404: Si le ticket spécifié n'existe pas.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(
        request, "review/ticket_detail.html", context={"ticket": ticket}
    )


@login_required
def create_review(request, ticket_id):
    """Crée une nouvelle critique.

    Cette fonction permet à un utilisateur connecté de créer une nouvelle
    critique pour un ticket spécifié.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.
        ticket_id (int): L'identifiant du ticket pour lequel la critique
        est crée.

    Returns:
        HttpResponseRedirect: Redirige l'utilisateur vers la page d'accueil
        après la création de la critique.

    Raises:
        Http404: Si le ticket spécifié n'existe pas.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.ReviewForm()
    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        print(form.errors)
        if form.is_valid():
            rating_value = int(request.POST.get("rating", 0))
            review = form.save(commit=False)
            review.user = request.user
            review.rating = rating_value
            review.ticket = ticket
            review.save()
            return redirect("home")
        else:
            # Afficher les erreurs dans le formulaire
            print(form.errors)
    return render(
        request,
        "review/create_review.html",
        context={"ticket": ticket, "form": form},
    )


@login_required
def edit_review(request, ticket_id, review_id):
    """Modifie une critique existante.

    Cette fonction permet à un utilisateur connecté de modifier une critique
    existante.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.
        ticket_id (int): L'identifiant du ticket associé à la critique.
        review_id (int): L'identifiant de la critique à modifier.

    Returns:
        HttpResponseRedirect: Redirige l'utilisateur vers la page de
        modification après avoir enregistré les modifications.

    Raises:
        Http404: Si le ticket ou la critique spécifiée n'existe pas.
    """
    review = get_object_or_404(models.Review, id=review_id)
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        print("requette post", request.POST)
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("edit_post")
    else:
        form = forms.ReviewForm(
            instance=review
        )  # Initialiser le formulaire avec l'instance de la critique

    return render(
        request,
        "review/edit_review.html",
        context={"ticket": ticket, "review": review, "form": form},
    )


@login_required
def delete_review(request, ticket_id, review_id):
    """Supprime une critique existante.

    Cette fonction permet à un utilisateur connecté de supprimer une critique
    existante.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.
        ticket_id (int): L'identifiant du ticket associé à la critique.
        review_id (int): L'identifiant de la critique à supprimer.

    Returns:
        HttpResponseRedirect: Redirige l'utilisateur vers la page de
        modification après la suppression de la critique.

    Raises:
        Http404: Si le ticket ou la critique spécifiée n'existe pas.
    """
    review = get_object_or_404(models.Review, id=review_id)
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if review:
        if review.user != request.user:
            return redirect("error_change_review", ticket.id, review.id)
        else:

            if request.method == "POST":
                review.delete()
                return redirect("edit_post")

    return render(
        request,
        "review/delete_review.html",
        context={"ticket": ticket, "review": review},
    )


@login_required
def review_detail(request, ticket_id, review_id):
    """Affiche les détails d'une critique.

    Cette fonction récupère les détails d'une critique spécifique et les
    affiche à l'utilisateur.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.
        ticket_id (int): L'identifiant du ticket associé à la critique.
        review_id (int): L'identifiant de la critique à afficher.

    Returns:
        HttpResponse: La réponse HTTP contenant les détails de la critique
        demandée.

    Raises:
        Http404: Si le ticket ou la critique spécifiée n'existe pas.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review = get_object_or_404(models.Review, id=review_id)
    return render(
        request,
        "review/review_detail.html",
        context={"ticket": ticket, "review": review},
    )


@login_required
def follow_users(request):
    """Permet à l'utilisateur de suivre d'autres utilisateurs.

    Cette fonction permet à l'utilisateur connecté de suivre d'autres
    utilisateurs en saisissant leur nom d'utilisateur.
    Elle affiche également les utilisateurs suivis par l'utilisateur actuel
    ainsi que ceux qui le suivent.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.

    Returns:
        HttpResponse: La réponse HTTP contenant le formulaire pour suivre les
        utilisateurs et les listes des utilisateurs suivis et des followers.

    Raises:
        Aucune exception n'est levée.
    """
    followed_users_ids = models.UserFollows.objects.filter(
        user=request.user
    ).values_list("followed_user_id", flat=True)

    followers_ids = models.UserFollows.objects.filter(
        followed_user=request.user
    ).values_list("user_id", flat=True)

    print(
        "IDs des utilisateurs suivis par l'utilisateur connecté :",
        followed_users_ids,
    )
    print(
        "IDs des utilisateurs abonnés à l'utilisateur connecté :",
        followers_ids,
    )

    followed_users = User.objects.filter(
        id__in=followed_users_ids
    ).values_list("username", flat=True)
    followers = User.objects.filter(id__in=followers_ids).values_list(
        "username", flat=True
    )

    print(
        "Noms des utilisateurs suivis par l'utilisateur connecté :",
        followed_users,
    )
    print(
        "Noms des utilisateurs abonnés à l'utilisateur connecté :",
        followers,
    )
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["follows"]
            try:
                followed_user = User.objects.get(username=username)
                if followed_user != request.user:
                    models.UserFollows.objects.get_or_create(
                        user_id=request.user.id,
                        followed_user_id=followed_user.id,
                    )
                else:
                    messages.error(
                        request, "Vous ne pouvez pas vous abonner à vous-même."
                    )
                return redirect("/follow-users/listing/")
            except User.DoesNotExist:
                # Gérez le cas où l'utilisateur n'existe pas
                pass
    else:
        form = forms.FollowUsersForm()
    context = {
        "form": form,
        "followed_users": followed_users,
        "followers": followers,
    }
    return render(request, "review/follow_users.html", context=context)


@login_required
def delete_follow(request, followed_user):
    """Permet à l'utilisateur de supprimer un abonnement à un autre
    utilisateur.

    Cette fonction permet à l'utilisateur connecté de supprimer un abonnement
    à un autre utilisateur.
    Si la méthode de la requête est POST, elle supprime l'abonnement
    correspondant dans la base de données
    et redirige l'utilisateur vers une autre page. Sinon, elle affiche la page
    de confirmation de suppression de l'abonnement.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.
        followed_user (str): Le nom d'utilisateur de l'utilisateur suivi.

    Returns:
        HttpResponse: La réponse HTTP redirigeant vers une autre page si la
        méthode de la requête est POST,sinon la page de confirmation de
        suppression de l'abonnement.

    Raises:
        Aucune exception n'est levée.
    """
    utilisateur_abonnement = get_object_or_404(User, username=followed_user)
    if request.method == "POST":
        # Récupérez l'ID de l'utilisateur suivi
        utilisateur_abonnement_id = utilisateur_abonnement.id
        # Supprimez l'abonnement correspondant dans UserFollows
        abonnement = models.UserFollows.objects.filter(
            user=request.user, followed_user_id=utilisateur_abonnement_id
        )
        abonnement.delete()
        return redirect("/follow-users/listing/")
    else:
        return render(
            request,
            "review/delete_follow.html",
            context={"followed_user": utilisateur_abonnement},
        )


@login_required
def edit_post(request):
    """Affiche la vue de l'édition des publications de l'utilisateur.

    Cette fonction récupère tous les tickets et les critiques associés à
    l'utilisateur connecté,les trie par date de création décroissante,
    puis les passe à la vue de l'édition des publications pour affichage.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.

    Returns:
        HttpResponse: La réponse HTTP contenant la vue de l'édition des
        publications de l'utilisateur.

    Raises:
        Aucune exception n'est levée.
    """
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )
    paginator = Paginator(tickets_and_reviews, 2)  # Nombre d'éléments par page

    page_number = request.GET.get("page")
    try:
        tickets_and_reviews = paginator.page(page_number)
    except PageNotAnInteger:
        tickets_and_reviews = paginator.page(1)
    except EmptyPage:
        tickets_and_reviews = paginator.page(paginator.num_pages)
    context = {"tickets_and_reviews": tickets_and_reviews}
    return render(request, "review/edit_post.html", context=context)


@login_required
def create_ticket_and_review(request):
    """Crée un nouveau ticket et une nouvelle critique.

    Cette fonction gère le formulaire de création de ticket et de critique.
    Si le formulaire est soumis avec des données valides, un nouveau ticket
    et une nouvelle critique sont créés et associés à l'utilisateur connecté.

    Args:
        request (HttpRequest): L'objet HttpRequest reçu par la vue.

    Returns:
        HttpResponse: La réponse HTTP redirigeant l'utilisateur vers la page
        d'accueil après la création réussie du ticket et de la critique.

    Raises:
        Aucune exception n'est levée.
    """
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }
    return render(request, "review/create_ticket_review.html", context=context)
