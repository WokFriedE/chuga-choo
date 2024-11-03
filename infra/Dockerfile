FROM nginx:alpine

WORKDIR /app
COPY . .

RUN echo hello
COPY ./full.conf /etc/nginx/conf.d/full.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]