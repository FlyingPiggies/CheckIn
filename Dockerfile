FROM python:3.7.0

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ['python3', "checkin.py"]