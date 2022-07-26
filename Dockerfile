FROM python:3.10
WORKDIR /store_subs
ENV PYTHONDONTWIRTEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY Pipfile Pipfile.lock /store_subs/
RUN pip install pipenv && pipenv install --system