FROM python:3.7.2

LABEL maintainer="Pieter-Jan Cassiman <pieterjan.cassiman@gmail.com>"

COPY requirement.txt /app/

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirement.txt

COPY . /app

ENTRYPOINT ["python3"]

# CMD ["app.py"]