FROM python:3.10-alpine

RUN apk add postgresql-dev gcc python3-dev musl-dev && \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
ADD ./core /app/core
COPY ./main.py /app/main.py


RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt


ENTRYPOINT ["python3"]
CMD [ "main.py"]
