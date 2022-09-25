FROM node:12.2.0-alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
# COPY ../../../frontend/propacienta/package*.json /app/package.json
COPY ../../../frontend/propacienta/package*.json /app/
RUN npm install --silent
RUN npm install @vue/cli@3.7.0 -g
COPY ../../../frontend/propacienta /app
RUN npm run build

# production environment
FROM nginx:latest
COPY --from=build /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
# EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]