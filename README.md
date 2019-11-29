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
gunicorn -w8 -b 0.0.0.0:5000 backend_fastapi:app -k uvicorn.workers.UvicornWorker
```
### Build and run as a Docker container
```
docker build -t surface_map_docker ./
docker run -d -p 80:80 --mount src=`pwd`/surface_map/maps,target=/app/surface_map/maps,type=bind surface_map_docker
```
