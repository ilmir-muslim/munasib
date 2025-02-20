FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean && rm -rf /var/lib/apt/lists/

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./src /app

RUN python manage.py collectstatic --noinput

CMD python manage.py migrate && \
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" && \
    gunicorn munasib_admin.wsgi:application --bind 0.0.0.0:8000 --log-level info