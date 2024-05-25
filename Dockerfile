FROM python:3.10

WORKDIR /api
COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port 8000