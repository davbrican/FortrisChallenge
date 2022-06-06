FROM node:14.16.0

RUN npm install -g http-server

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

CMD [ "http-server", "-P", "http://localhost:8000?", "dist" ]