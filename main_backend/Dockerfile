FROM python:3.11
ENV PYTHONBUFFERED=1
RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
