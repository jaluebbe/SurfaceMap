import math
from fastapi import FastAPI, Query
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
from surface_map.globcover2009 import GlobCover2009
from surface_map.udel_airt_precip import UDelAirTPrecip
import surface_map.countries as countries

gc = GlobCover2009()
air_precip = UDelAirTPrecip()

app = FastAPI(
    openapi_prefix='',
    title='SurfaceMap',
    description='Look up positions in global surface coverage sources.'
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse('static/surfacemap.html')

@app.get("/api/get_surface_cover")
def get_surface_cover(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
    ):
    return gc.get_data_at_position(lat, lon)

@app.get("/api/get_air_temp_precipitation")
def get_air_temp_precipitation(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
    ):
    air_temp_precipitation = air_precip.get_data_at_position(lat, lon)
    for key in ['annual_precip_cm', 'min_air_temp', 'max_air_temp',
        'mean_air_temp']:
        if math.isnan(air_temp_precipitation[key]):
            air_temp_precipitation[key] = 'NaN'
    return air_temp_precipitation

@app.get("/api/get_surface_data")
def get_surface_data(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
    ):
    air_temp_precipitation = air_precip.get_data_at_position(lat, lon)
    for key in ['annual_precip_cm', 'min_air_temp', 'max_air_temp',
        'mean_air_temp']:
        if math.isnan(air_temp_precipitation[key]):
            air_temp_precipitation[key] = 'NaN'
    country = countries.get_country_for_position(lat, lon)
    return {
        'surface_cover': gc.get_data_at_position(lat, lon),
        'air_temp_precipitation': air_temp_precipitation,
        'country': country.get('ADMIN'), 'continent': country.get('CONTINENT')}
