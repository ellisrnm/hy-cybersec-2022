from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Mood


def index(request):
    return render(request, 'moodtracker/index.html')

def rate(request):
    if request.method == 'POST':
        try:
            selected_rating = request.POST['rating']
        except:
            return render(request, 'moodtracker/rate.html', {
                'error_message': "Please select a rating",
            })
        new_rating = Mood.objects.create(rating=selected_rating, date=timezone.now())
        new_rating.save()
        return HttpResponseRedirect(reverse('results'))
    return render(request, 'moodtracker/rate.html')

def results(request):
    latest_ratings = Mood.objects.all().order_by('date')
    context = {
        'latest_ratings': latest_ratings,
    }
    return render(request, 'moodtracker/results.html', context)