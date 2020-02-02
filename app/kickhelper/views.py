from django.http import HttpResponse
from django.template import loader
from datetime import date

from .ml import model

def index(request):
    template = loader.get_template('kickhelper/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def results(request):
    main_category = request.POST['mainCategory']
    category = request.POST['category']
    goal = request.POST['goal']
    country = request.POST['country']
    currency = request.POST['currency']
    today = date.today()

    result = model.predict([main_category, category, goal, country, currency, today])

    return HttpResponse(result)
