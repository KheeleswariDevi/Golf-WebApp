from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Golfer, GolfCourse
from .forms import AddGolferForm, AddGolfCourseForm
import requests
import sys

# Create your views here.
def index(request):
    '''View function for home page.'''
    num_golfers = Golfer.objects.all().count()
    num_courses = GolfCourse.objects.all().count()
    ctx = {
        'num_golfers': num_golfers,
        'num_courses': num_courses
    }
    return render(request, 'golf/index.html', context=ctx)

def golferlist(request):
    '''View function for golfer list.'''
    golfers = Golfer.objects.all()
    ctx = {
        'golfers': golfers
    }
    return render(request, 'golf/golferlist.html', context=ctx)

def courselist(request):
    '''View function for course list.'''
    courses = GolfCourse.objects.all()
    ctx = {
        'courses': courses
    }
    return render(request, 'golf/courselist.html', context=ctx)

def golferdetails(request, gid):
    '''View function for golfer details.'''
    golfer = Golfer.objects.get(id=gid)
    ctx = {
        'golfer': golfer
    }
    return render(request, 'golf/golferdetails.html', context=ctx)

def coursedetails(request, cid):
    '''View function for course details.'''
    course = GolfCourse.objects.get(id=cid)
    ctx = {
        'course': course
    }
    return render(request, 'golf/coursedetails.html', context=ctx)


from django.shortcuts import render

def faq(request):
    return render(request, 'golf/faq.html')



HOLES = 18

def calc_points(par, net_strokes):
    '''Return points given par and net strokes'''
    try:
        points = par - int(net_strokes) + 2
        return (points > 0) * points
    except ValueError:
        if net_strokes == 'X':
            return 0
        raise ValueError

def main(lines):
    results = []
    disqualified = []

    pars = [int(x) for x in lines.pop(0).strip().split()]
    indices = [int(x) for x in lines.pop(0).strip().split()]

    for line in lines:
        tokens = line.split()
        scores = tokens[-HOLES:]
        hcap = int(tokens[-(HOLES+1)])
        name = ' '.join(tokens[:-(HOLES+1)])

        hpars = pars[:]
        for i in range(1, hcap+1):
            idx = i % HOLES
            if not idx:
                idx = HOLES
            hpars[indices.index(idx)] += 1

        try:
            points = sum([calc_points(p, s) for (p, s) in zip(hpars, scores)])
        except ValueError:
            disqualified.append(name)
        else:
            results.append((name, points))

    return results, disqualified

@csrf_exempt
def stableford_view(request):
    if request.method == 'POST':
        data = request.POST.get('data', '')
        lines = data.splitlines()
        output, disqualified = main(lines)
        results = []
        for name, points in output:
            results.append(f'{name}: {points}')
        disqualified_str = ', '.join(disqualified) if disqualified else 'None'
        ctx = {
            'output': results,
            'disqualified': disqualified_str
        }
        return render(request, 'golf/stableford.html', context=ctx)
    else:
        return render(request, 'golf/stableford.html')

        
@csrf_exempt
def addgolfer(request):
  '''View function for add golfer form.'''
  if request.method == 'POST':
    form = AddGolferForm(request.POST)

    if form.is_valid():
      golfer = Golfer(
        forename = form.cleaned_data['forename'],
        surname = form.cleaned_data['surname'],
        handicap = form.cleaned_data['handicap'])
      golfer.save()
      messages.success(request, "Added {}".format(golfer))
      return HttpResponseRedirect(reverse('golferlist'))
  else:
    form = AddGolferForm()

  context = {
    'form' : form
  }

  return render(request, 'golf/addgolfer.html', context)

@csrf_exempt
def addgolfcourse(request):
  '''View function for add golf course form.'''
  if request.method == 'POST':
    form = AddGolfCourseForm(request.POST)

    if form.is_valid():
      course = GolfCourse(
        name = form.cleaned_data['name'],
        latitude = form.cleaned_data['latitude'],
        longitude = form.cleaned_data['longitude'])
      course.save()
      messages.success(request, "Added {}".format(course))
      return HttpResponseRedirect(reverse('courselist'))
  else:
    form = AddGolfCourseForm()

  context = {
    'form' : form
  }

  return render(request, 'golf/addgolfcourse.html', context)

def get_daily_temperatures(forecast_data):
    daily_temperatures = []

    today = None
    temperature_points = []

    for data in forecast_data:
        # Date from the data point
        date = data['dt_txt'].split()[0]

        # Store the temperature points for the previous day if a new day is encountered
        if date != today:
            if temperature_points:
                daily_temperatures.append(temperature_points)
            today = date
            temperature_points = []

        # Temperature for morning, afternoon, and evening
        if data['dt_txt'].split()[1] in ('09:00:00', '15:00:00', '18:00:00', '21:00:00'):
            temperature_points.append({
                'date': data['dt_txt'],
                'temperature': data['main']['temp'],
                'weather_description': data['weather'][0]['description']
            })

    return daily_temperatures


def weather_forecast(request):
    api_key = '99f9c427e22a60c77c0f4809c3335295'
    location = '2964574'
    url = f"https://api.openweathermap.org/data/2.5/forecast?id=2964574&appid=99f9c427e22a60c77c0f4809c3335295&units=metric"
    response = requests.get(url)
    data = response.json()

    # Check if the API response contains the 'list' key
    if 'list' in data:
        forecast = data['list']
        daily_temperatures = get_daily_temperatures(forecast)
    else:
        daily_temperatures = []

    context = {
        'daily_temperatures': daily_temperatures
    }

    return render(request, 'golf/weather.html', context)