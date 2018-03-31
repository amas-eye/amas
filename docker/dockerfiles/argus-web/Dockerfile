FROM node:8
MAINTAINER <eacon-tang@foxmail.com>


RUN mkdir /opt/amas
WORKDIR /opt/amas

# clone repo
RUN git clone https://github.com/amas-eye/argus-web.git


# install server dependency
RUN cd /opt/amas/argus-web/server && \
    npm install && \
    npm install -g pm2


# install app dependency
RUN cd /opt/amas/argus-web/app && \
    npm install
# build app, locate to server/
RUN cd /opt/amas/argus-web/app && \
    npm run build && \
    mv dist/ /opt/amas/argus-web/server/app


ADD init_user.sh /usr/local/bin/init_user
RUN chmod +x /usr/local/bin/init_user

ADD run.sh /usr/local/bin/run
RUN chmod +x /usr/local/bin/run

EXPOSE 8080

CMD ["run"]