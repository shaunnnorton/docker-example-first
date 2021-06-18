FROM python:3.7-slim-buster

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=developement
ENV DATABASE_URL=sqlite:///database.db
ENV SECRET_KEY=8675309FRIDAY

EXPOSE 5000

CMD [ "python", "app.py" ]

