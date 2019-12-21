# SurfaceMap

## Software requirements

### conda/apt

gdal pandas xlrd gunicorn

### pip

fastapi uvicorn aiofiles

## Data Sources

### GlobCover2009:

http://due.esrin.esa.int/page_globcover.php

&copy; ESA 2010 and UCLouvain

Download http://due.esrin.esa.int/files/Globcover2009_V2.3_Global_.zip and extract the contents to surface_map/maps/globcover2009/ .

### University of Delaware Air Temperature & Precipitation (UDel_AirT_Precip):

https://www.esrl.noaa.gov/psd/data/gridded/data.UDel_AirT_Precip.html

UDel_AirT_Precip data provided by the NOAA/OAR/ESRL PSD, Boulder, Colorado, USA, from their Web site at https://www.esrl.noaa.gov/psd/ .

Download ftp://ftp.cdc.noaa.gov/Datasets/udel.airt.precip/precip.mon.ltm.v501.nc and ftp://ftp.cdc.noaa.gov/Datasets/udel.airt.precip/air.mon.ltm.v501.nc to surface_map/maps/udel_airt_precip/ .

## Startup of the web interface

The web interface and API is hosted using FastAPI. It could also be run as a Docker container.

### FastAPI
```
gunicorn -w8 -b 0.0.0.0:8000 backend_fastapi:app -k uvicorn.workers.UvicornWorker
```
### Build and run as a Docker container
```
docker build -t surfacemap ./
docker run -d -p 8000:80 --mount src=`pwd`/surface_map/maps,target=/app/surface_map/maps,type=bind surfacemap
```
or for the alpine based image which consumes less disk space:
```
docker build -t surfacemap:alpine -f Dockerfile.alpine ./
docker run -d -p 8000:80 --mount src=`pwd`/surface_map/maps,target=/app/surface_map/maps,type=bind surfacemap:alpine
```
### Downloading images from hub.docker.com
Instead of building the image, you may try to download it from hub.docker.com. 
Simply use jaluebbe/surfacemap or jaluebbe/surfacemap:alpine as image to run.

## Accessing the API and web interface

You'll find an interative map at http://127.0.0.1:8000. 
Click anywhere on the map to obtain the local surface information. 
You may drag the marker on the map. 
Documentation of the API is available at http://127.0.0.1:8000/docs (you can try out the API) and http://127.0.0.1:8000/redoc (more information but less interactive).
