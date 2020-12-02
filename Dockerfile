FROM python:3.7-alpine

WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN apk --no-cache add build-base
RUN pip install pipenv --no-cache-dir && pipenv install --system --deploy && pip uninstall -y pipenv virtualenv-clone virtualenv

COPY *.py .
CMD python app.py