FROM python


RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

EXPOSE 5000
WORKDIR /app
COPY app /app
COPY requirements.txt ./
COPY God /God

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

USER root

CMD ["./cmd.sh"]

