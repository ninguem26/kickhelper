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
    success_rate = int(result[0][0] * 100)
    failure_rate = int(result[0][1] * 100)

    if success_rate < 40:
        color = '#DB0118'
        message = 'Your idea is very risky, review your scope and plan better both the category you want to launch the project and the budget you think you will need.'
    elif success_rate < 70:
        color = '#E6DA07'
        message = 'Your idea is interesting, but there is still room for improvement.'
    else:
        color = '#04CF77'
        message = "Your idea hits safe targets with a realistic fundraising value, it's a great base to start your crowdfunding campaign!"

    template = loader.get_template('kickhelper/results.html')
    context = {
        'success': success_rate,
        'failure': failure_rate,
        'mainCategory': main_category,
        'category': category,
        'goal': goal,
        'country': country,
        'currency': currency,
        'color': color,
        'message': message
    }

    return HttpResponse(template.render(context, request))
