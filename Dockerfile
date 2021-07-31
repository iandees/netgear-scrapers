FROM python:3

RUN pip install pipenv mechanize
WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --dev --deploy --system

COPY . .

CMD [ "python", "periodically.py" ]
