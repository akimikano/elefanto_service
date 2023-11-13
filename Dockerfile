FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

#CMD bash -c "python manage.py collectstatic --no-input && python manage.py migrate && gunicorn -b 0.0.0.0:8000 --log-level debug -w 4 m_uslugi.wsgi:application"
