import os
import json
from surface_map.netcdf_handler import NetCDFHandler

class UDelAirTPrecip:

    path = 'surface_map/maps/udel_airt_precip'
    attribution_url = (
        'https://www.esrl.noaa.gov/psd/data/gridded/data.UDel_AirT_Precip.html')
    attribution_name = 'UDel_AirT_Precip'
    attribution = ('<a href="{}">{}</a>').format(attribution_url,
        attribution_name)

    def __init__(self):
        self.nh_air_temp = NetCDFHandler(os.path.join(self.path,
            'air.mon.ltm.v501.nc'), 'air')
        self.nh_precip = NetCDFHandler(os.path.join(self.path,
            'precip.mon.ltm.v501.nc'), 'precip')

    def get_temperature_values_at_position(self, lat, lon):
        values = self.nh_air_temp.get_values_at_position(lat, lon)
        nodata = float(self.nh_air_temp.metadata['air#missing_value'])
        values = [i if i >= -273.15 else float('nan') for i in values]
        return values
        
    def get_precipitation_values_at_position(self, lat, lon):
        values = self.nh_precip.get_values_at_position(lat, lon)
        nodata = float(self.nh_precip.metadata['precip#missing_value'])
        values = [i if i >= 0 else float('nan') for i in values]
        return values

    def get_data_at_position(self, lat, lon):
        if lon < 0:
            lon += 360
        temperatures = self.get_temperature_values_at_position(lat, lon)
        precipitation = self.get_precipitation_values_at_position(lat, lon)
        return {
            'annual_precip_cm': round(sum(precipitation), 2),
            'min_air_temp': round(min(temperatures), 2),
            'max_air_temp': round(max(temperatures), 2),
            'mean_air_temp': round(sum(temperatures) / len(temperatures), 2),
            'source': self.attribution_name, 'attribution': self.attribution}

if __name__ == "__main__":

    air_precip = UDelAirTPrecip()
    # London
    print(air_precip.get_data_at_position(51.5, -0.12))
    # Black Forest    
    print(air_precip.get_data_at_position(47.94, 8.3))
    # high moor in Emsland region
    print(air_precip.get_data_at_position(52.8, 7.4))
    # Salt Lake City
    print(air_precip.get_data_at_position(40.8, -112))
    
