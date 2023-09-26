FROM python:slim

WORKDIR /app 

RUN mkdir db
COPY requirements.txt .

RUN pip install -r requirements.txt

ADD main.py .
CMD ["python", "./main.py"]