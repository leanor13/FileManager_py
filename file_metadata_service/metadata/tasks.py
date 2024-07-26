from celery import shared_task


# testing celery
@shared_task
def add(x, y):
    return x + y
