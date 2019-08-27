FROM python:3.7-slim

WORKDIR /usr/app
COPY requirements.txt /usr/app/
RUN pip install -r requirements.txt

COPY partyplanner events manage.py pytest.ini partyplanner.wsgi /usr/app/
CMD ["gunicorn", "partyplanner.wsgi"]
