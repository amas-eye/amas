FROM python:3.6
MAINTAINER <eacon-tang@foxmail.com>


RUN mkdir /opt/amas
WORKDIR /opt/amas

# clone repo
RUN git clone https://github.com/amas-eye/argus_alert.git

# install requirements
RUN cd argus_alert/libs; pip install -r requirements.txt

ADD run.sh /usr/local/bin/run
RUN chmod +x /usr/local/bin/run

ENV PYTHONPATH /opt/amas

CMD ["run"]