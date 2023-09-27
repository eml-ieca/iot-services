FROM python:slim

WORKDIR /app 

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir log

COPY . .
CMD ["python", "./main.py"]