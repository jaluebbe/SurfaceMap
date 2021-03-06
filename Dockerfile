FROM debian:buster

RUN apt-get -y update &&  \
    apt-get -y install python3-pip python3-gdal wget && \
    pip3 install uvicorn gunicorn fastapi aiofiles
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY surface_map /app/surface_map
COPY static /app/static
COPY backend_fastapi.py /app/main.py

WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g.
# for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
