from django.shortcuts import render
from django.http import HttpResponse

from .models import Mood


def index(request):
    return render(request, 'moodtracker/index.html')

def rate(request):
    return render(request, 'moodtracker/rate.html')

def results(request):
    latest_ratings = Mood.objects.order_by('date')
    context = {
        'latest_ratings': latest_ratings,
    }
    return render(request, 'moodtracker/results.html', context)