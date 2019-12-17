import os
import json
from surface_map.geotiff_handler import GeoTiffHandler

class GlobCover2009:

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'maps/globcover2009')
    attribution_url = ('http://due.esrin.esa.int/page_globcover.php')
    attribution_name = 'GlobCover 2009'
    attribution = ('&copy <a href="{}">{}</a>').format(attribution_url,
        attribution_name)

    def __init__(self):
        legend_file = os.path.join(self.path, 'globcover2009_legend.json')
        with open(legend_file, 'r') as f:
            self.legend = json.load(f)
        self.gth = GeoTiffHandler(os.path.join(self.path,
            'GLOBCOVER_L4_200901_200912_V2.3.tif'))

    def get_value_at_position(self, lat, lon):
        return self.gth.get_value_at_position(lat, lon)

    def get_data_at_position(self, lat, lon):
        value = self.get_value_at_position(lat, lon)
        if value is None:
            # set to the value describing no data.
            value = 230
        legend = self.legend[str(value)]
        return {
            'value': value, 'label': legend['label'], 'color': legend['color'],
            'source': self.attribution_name, 'attribution': self.attribution}

if __name__ == "__main__":

    gc2009 = GlobCover2009()
    # London
    print(gc2009.get_data_at_position(51.5, -0.12))
    # Black Forest    
    print(gc2009.get_data_at_position(47.94, 8.3))
    # Black Forest
    print(gc2009.get_data_at_position(48, 8))
    # Lake Constance
    print(gc2009.get_data_at_position(47.56, 9.5))
    # Hambach open pit
    print(gc2009.get_data_at_position(50.91, 6.51))
    # high moor in Emsland region
    print(gc2009.get_data_at_position(52.8, 7.4))
    # farmland in Emsland region
    print(gc2009.get_data_at_position(52.78, 7.4))
