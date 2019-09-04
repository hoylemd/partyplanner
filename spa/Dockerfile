FROM node:12-slim

WORKDIR /usr/app

COPY bin /usr/app/bin

COPY package.json /usr/app/
RUN npm install

COPY src/* /usr/app/src/
COPY public/* /usr/app/public/

CMD ["/usr/app/bin/runserver.sh"]
