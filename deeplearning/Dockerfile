FROM python


RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi


WORKDIR /app
COPY app /app
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

USER root

EXPOSE 8888

CMD ["./cmd.sh"]

