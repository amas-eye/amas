FROM python:2.7
MAINTAINER <eacon-tang@foxmail.com>


RUN mkdir /opt/amas
WORKDIR /opt/amas

# clone repo
RUN git clone https://github.com/amas-eye/argus_collector.git

ADD run.sh /usr/local/bin/run
RUN chmod +x /usr/local/bin/run

ENV PYTHONPATH /opt/amas

CMD ["run"]