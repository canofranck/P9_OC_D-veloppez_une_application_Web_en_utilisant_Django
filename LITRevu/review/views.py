
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    pass
    return render(request, 'review/home.html')

