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
RUN pip3 install Pillow
USER root



CMD ["./cmd.sh"]

