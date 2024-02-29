
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from authentication.models import User
from . import forms, models
from django.contrib import messages
from django.db.models import Q
from itertools import chain
from django.db.models import Avg


@login_required
def home(request):
    main_user_id = request.user.id
    tickets = models.Ticket.objects.filter(
        Q(user_id__in=models.UserFollows.objects.filter(followed_user_id=main_user_id).values('user_id')) |
        Q(user_id=main_user_id)
    )
    print(tickets)
    # ticket= models.Ticket.objects.all()
    # review= models.Review.objects.all()
    reviews = models.Review.objects.filter(
    Q(user_id__in=models.UserFollows.objects.filter(followed_user_id=main_user_id).values('user_id')) |
    Q(user_id=main_user_id) |
    Q(ticket__user_id=main_user_id)
).annotate(avg_rating=Avg('rating'))  # Annotate each review with the average rating
    print(reviews)
    # main_user = forms.User.objects.get(username=request.user)
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
     
    # return render(request, 'review/home.html', context={'tickets': ticket, 'reviews': review,'user': main_user})
    return render(request, 'review/home.html', context={'tickets_and_reviews': tickets_and_reviews})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'review/create_ticket.html', context={'form': form})

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.TicketForm(instance=ticket)
    if ticket:
        if ticket.user != request.user:
            return redirect('error_change_ticket', ticket.id)
        else:
            if request.method == 'POST':
                form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
                if form.is_valid():
                    ticket_save = form.save(commit=False)
                    ticket_save.user = request.user
                    ticket_save.save()
                    return redirect('home')
    return render(
        request, 'review/edit_ticket.html',
        context={'ticket': ticket, 'form': form})
    
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    # Vérifiez si l'utilisateur actuel est bien celui qui a créé le ticket
    if ticket.user != request.user:
        return redirect('error_delete_ticket',ticket.id)  # Redirigez vers une page d'erreur appropriée

    if request.method == 'POST':
        ticket.delete()
        return redirect('home')  # Redirigez l'utilisateur vers la page d'accueil ou une autre page appropriée après la suppression du ticket

    return render(
        request, 'review/delete_ticket.html', context={'ticket': ticket})
    
@login_required
def error_delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(
        request, 'review/error_delete_ticket.html',
        context={'ticket': ticket})
    
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(
        request, 'review/ticket_detail.html',
        context={'ticket': ticket})
    
@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            rating_value = int(request.POST.get('rating', 0))
            review = form.save(commit=False)
            review.user = request.user
            review.rating = rating_value
            review.ticket = ticket
            review.save()
            return redirect('home')
        else:
            # Afficher les erreurs dans le formulaire
            print(form.errors)
    return render(
        request, 'review/create_review.html',
        context={'ticket': ticket, 'form': form})
    
@login_required
def edit_review(request, ticket_id, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.ReviewForm(instance=review)
    if review:
        if review.user != request.user:
            return redirect('error_change_review', ticket.id, review.id)
        else:

            if request.method == 'POST':
                form = forms.ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.ticket = ticket
                    review.save()
                    return redirect('post_edit')
    return render(
        request, 'review/edit_review.html',
        context={'ticket': ticket, 'review': review, 'form': form})

@login_required
def delete_review(request, ticket_id, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if review:
        if review.user != request.user:
            return redirect('error_change_review', ticket.id, review.id)
        else:

            if request.method == 'POST':
                review.delete()
                return redirect('post_edit')

    return render(
        request, 'review/delete_review.html',
        context={'ticket': ticket, 'review': review})  
    
@login_required
def review_detail(request, ticket_id, review_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review = get_object_or_404(models.Review, id=review_id)
    return render(
        request, 'review/review_detail.html',
        context={'ticket': ticket, 'review': review})
    
@login_required
def follow_users(request):
    followed_users_ids = models.UserFollows.objects.filter(user=request.user).values_list('followed_user_id', flat=True)
    followers_ids = models.UserFollows.objects.filter(followed_user=request.user).values_list('user_id', flat=True)

    print("IDs des utilisateurs suivis par l'utilisateur connecté :", followed_users_ids)
    print("IDs des utilisateurs abonnés à l'utilisateur connecté :", followers_ids)

    followed_users = User.objects.filter(id__in=followed_users_ids).values_list('username', flat=True)
    followers = User.objects.filter(id__in=followers_ids).values_list('username', flat=True)

    print("Noms d'utilisateur des utilisateurs suivis par l'utilisateur connecté :", followed_users)
    print("Noms d'utilisateur des utilisateurs abonnés à l'utilisateur connecté :", followers)


    if request.method == 'POST':
        form =forms.FollowUsersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['follows']
            try:
                followed_user = User.objects.get(username=username)
                if followed_user != request.user:
                    models.UserFollows.objects.get_or_create(user_id=request.user.id, followed_user_id=followed_user.id)
                else:
                    messages.error(request, "Vous ne pouvez pas vous abonner à vous-même.")
                return redirect('/follow-users/listing/')  
            except User.DoesNotExist:
                # Gérez le cas où l'utilisateur n'existe pas
                pass
    else:
        form = forms.FollowUsersForm()
    context = {
        'form': form,
        'followed_users': followed_users,
        'followers': followers,
    }
    return render(request, 'review/follow_users.html', context=context)


@login_required
def delete_follow(request, followed_user):
    utilisateur_abonnement = get_object_or_404(User, username=followed_user)
    if request.method == 'POST':
        # Récupérez l'ID de l'utilisateur suivi
        utilisateur_abonnement_id = utilisateur_abonnement.id
        # Supprimez l'abonnement correspondant dans UserFollows
        abonnement = models.UserFollows.objects.filter(user=request.user, followed_user_id=utilisateur_abonnement_id)
        abonnement.delete()
        return redirect('/follow-users/listing/')
    else:
        return render(request, 'review/delete_follow.html', context={'followed_user': utilisateur_abonnement})


@login_required
def post_edit(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    context = {'tickets_and_reviews': tickets_and_reviews}
    return render(request, 'review/post_edit.html', context=context)



   



