from pathlib import Path

import matplotlib.pyplot as plt
import mpld3 as mpld3

from ...models import Orders


# Creating plot, where x - "номер заказа", y - "цена в долларах";
def create_plot():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot()
    orders_sort = Orders.objects.order_by('order_number').values()
    x = [order['order_number'] for order in orders_sort]
    y = [order['price_usd'] for order in orders_sort]
    plt.plot(x, y)
    plt.xlabel("Номер заказа", fontsize=20)
    plt.ylabel("Цена в долларах", fontsize=20)

    # Getting plot html
    html_str = mpld3.fig_to_html(fig)

    # Saving HTML to a file
    dir_app = Path(__file__).resolve().parent.parent.parent

    with open(f'{dir_app}/templates/single/plot.html', 'w') as ht:
        ht.write(html_str)
