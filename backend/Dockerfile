FROM python:3.7-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
RUN mkdir -p media/recipes/images
RUN chmod 755 start-backend-server.sh

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["./start-backend-server.sh"]
