import os
import json
from surface_map.netcdf_handler import NetCDFHandler

class UDelAirTPrecip:

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'maps/udel_airt_precip')
    attribution_url = (
        'https://www.esrl.noaa.gov/psd/data/gridded/data.UDel_AirT_Precip.html')
    attribution_name = 'UDel_AirT_Precip'
    attribution = ('<a href="{}">{}</a>').format(attribution_url,
        attribution_name)
    nh_air_temp = None
    nh_precip = None

    def __init__(self, air_temp=True, precip=True):
        if air_temp:
            self.nh_air_temp = NetCDFHandler(os.path.join(self.path,
                'air.mon.ltm.v501.nc'), 'air')
        if precip:
            self.nh_precip = NetCDFHandler(os.path.join(self.path,
                'precip.mon.ltm.v501.nc'), 'precip')

    def get_data_at_position(self, lat, lon):
        if lon < 0:
            lon += 360
        response = {'source': self.attribution_name,
            'attribution': self.attribution}
        if self.nh_air_temp is not None:
            temperatures = self.nh_air_temp.get_values_at_position(lat, lon)
            response.update({
                'min_air_temp': round(min(temperatures), 2),
                'max_air_temp': round(max(temperatures), 2),
                'mean_air_temp': round(sum(temperatures) / len(temperatures), 2)
                })
        if self.nh_precip is not None:
            precipitation = self.nh_precip.get_values_at_position(lat, lon)
            response.update({'annual_precip_cm': round(sum(precipitation), 2)})
        return response

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
    
