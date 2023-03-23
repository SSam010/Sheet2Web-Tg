from django.shortcuts import render

from .models import Orders
from .scripts.single import plot


def index(request):
    data = Orders.objects.all()
    # Creating plot
    plot.create_plot()
    return render(request, 'single/index.html', {'data': data})
