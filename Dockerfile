FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install anyio==3.4.0

EXPOSE 8080
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]