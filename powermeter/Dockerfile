FROM python:3.9.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /powermeter
COPY requirements.txt /powermeter/
RUN pip install -r requirements.txt
COPY manage.py /powermeter
COPY . /powermeter/