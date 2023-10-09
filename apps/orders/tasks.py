from celery import shared_task
from .models import Order


@shared_task
def process_order(order_id):
    import time
    time.sleep(10)
    order = Order.objects.get(id=order_id)
    order.status = 'completed'
    order.save()
