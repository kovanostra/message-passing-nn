FROM python:3.7.6

RUN mkdir /app/

COPY /dist/message-passing-nn-*tar.gz /app/app.tar.gz
COPY /data /app/data
COPY ./docker-entrypoint.sh /app/
RUN chmod 777 /app/docker-entrypoint.sh && ln -s /app/docker-entrypoint.sh /

RUN pip install --upgrade pip && pip install /app/app.tar.gz

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
RUN cd /app/
CMD ["message-passing-nn", "start-training", "--dataset=sample-dataset", "--data_path=./app/data/"]