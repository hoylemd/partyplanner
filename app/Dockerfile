FROM python:3.7-slim

WORKDIR /usr/app
COPY requirements.txt /usr/app/
RUN pip install -r requirements.txt

COPY partyplanner /usr/app/partyplanner/
COPY events /usr/app/events/
COPY manage.py pytest.ini gunicorn_config.py /usr/app/

CMD ["gunicorn", "-c", "gunicorn_config.py"]
