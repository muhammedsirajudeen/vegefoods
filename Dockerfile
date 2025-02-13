FROM python:3.10-slim

WORKDIR /app
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libpango1.0-0 \
    && rm -rf /var/lib/apt/lists/*
COPY . . 

RUN pip install -r requirements.txt

WORKDIR /app/vegefoods
EXPOSE 8000
RUN python manage.py makemigrations
# RUN python manage.py migrate
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver "]
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]