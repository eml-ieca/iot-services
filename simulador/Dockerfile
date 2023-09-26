FROM python:slim

WORKDIR /app 

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir log

ADD main.py .
CMD ["python", "./main.py"]