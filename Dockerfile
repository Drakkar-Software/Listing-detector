FROM python:3.10.10-slim-buster

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
