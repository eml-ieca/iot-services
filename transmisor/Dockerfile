FROM python:slim

WORKDIR /app 

RUN mkdir db
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
CMD ["python", "./main.py"]