FROM python:3.12.6

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py collectstatic

RUN mkdir media && cd media && mkdir recipes && cd ..

RUN cp -r initial_data/recipes media

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]