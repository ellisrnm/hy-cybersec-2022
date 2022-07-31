from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import timezone as tz

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
    ratings = Mood.objects.all()

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