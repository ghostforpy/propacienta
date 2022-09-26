FROM node:lts-alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./frontend/propacienta/package*.json /app/
# RUN npm install --silent
RUN npm install
RUN npm install @vue/cli@3.7.0 -g
COPY ./frontend/propacienta /app
RUN npm run build

# production environment
FROM nginx:latest
COPY --from=build /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/nginx.conf /etc/nginx/nginx.conf
# EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]