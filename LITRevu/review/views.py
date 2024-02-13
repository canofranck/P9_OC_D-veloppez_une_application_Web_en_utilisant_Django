
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models

@login_required
def home(request):
    ticket= models.Ticket.objects.all()
    return render(request, 'review/home.html', context={'tickets': ticket})

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


