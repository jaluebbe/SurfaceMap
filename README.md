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

## Startup of the web interface

The web interface and API is hosted using FastAPI. It could also be run as a Docker container.

### FastAPI
```
gunicorn -w8 -b 0.0.0.0:5000 backend_fastapi:app -k uvicorn.workers.UvicornWorker
```
