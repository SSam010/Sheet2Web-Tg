from django.shortcuts import render
from django.views.decorators.cache import cache_page

from orders_website.settings import UPDATE_PERIOD
from .models import Orders
from .scripts.single import plot


@cache_page(int(UPDATE_PERIOD))
def index(request):
    data = Orders.objects.all()
    # Creating plot
    plot.create_plot()
    return render(request, 'single/index.html', {'data': data})
