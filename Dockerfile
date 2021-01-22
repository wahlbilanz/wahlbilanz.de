FROM binfalse/jekyll AS compiler
ADD . .
RUN /usr/local/bin/jekyll build -d /site

FROM nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=compiler /site /usr/share/nginx/html
