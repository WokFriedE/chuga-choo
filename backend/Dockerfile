FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "wsgi:app"]
