FROM python:3.12-slim
LABEL authors="lovesuper"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

COPY . /app

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
