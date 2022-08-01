from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import timezone as tz
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required

from .models import Mood
from django.contrib.auth.models import User


def index(request):
    return render(request, 'moodtracker/index.html')

#@login_required(login_url='/moodtracker/login')
def rate(request):
    if request.method == 'POST':
        try:
            selected_rating = request.POST['rating']
        except:
            return render(request, 'moodtracker/rate.html', {
                'error_message': "Please select a rating",
            })
        new_rating = Mood.objects.create(rating=selected_rating, date=timezone.now(), user_id=request.user)
        new_rating.save()
        return HttpResponseRedirect(reverse('results'))
    return render(request, 'moodtracker/rate.html')

#@login_required(login_url='/moodtracker/login')
def results(request):
    ratings = Mood.objects.filter(user_id=request.user.id)

    dates = []
    own_ratings = []
    for rating in ratings:
        dates.append(rating.date.replace(tzinfo=tz.utc).timestamp() * 1000)
        own_ratings.append(rating.rating)

    context = {
        'dates': dates,
        'own_ratings': own_ratings,
    }
    return render(request, 'moodtracker/results.html', context)

def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                context = {'error_message': "Wrong username or password"}
        except:
            context = {'error_message': "Something went wrong"}
        return render(request, 'moodtracker/login.html', context)
    return render(request, 'moodtracker/login.html')

def register_view(request):
    if request.method == 'POST':
        try:
            selected_username = request.POST['username']
            selected_password = request.POST['password']
            user = User.objects.create_user(username=selected_username, password=selected_password)
            user.save()
        except:
            return render(request, 'moodtracker/register.html', {
                'error_message': "Please select a valid username and password",
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'moodtracker/register.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))