# build environment
FROM node:latest as build
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
RUN yarn install 
COPY . /app 
RUN yarn run build 

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /var/www
# new
# COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]