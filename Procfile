release: python manage.py migrate
web: daphne mediaapp.asgi:application
worker: python manage.py runworker -v2