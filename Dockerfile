FROM python:3

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -r /code/requirements.txt

# Устанавливает переменную окружения, которая гарантирует,
# что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

COPY . .