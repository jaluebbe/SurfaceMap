from fastapi import FastAPI, Query
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
from surface_map.globcover2009 import GlobCover2009
gc = GlobCover2009()

app = FastAPI(
    openapi_prefix='',
    title='SurfaceMap',
    description='Look up positions in global surface coverage sources.'
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse('static/surfacemap.html')

@app.get("/api/get_surface_data")
def get_surface_data(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
    ):
    return gc.get_data_at_position(lat, lon)
