import gdal
import gdalconst
import ogr
import struct
import logging

class GeoTiffHandler:

    logger = logging.getLogger(__name__)

    def __init__(self, file_name):
        self.file_name = file_name
        self._fmttypes = {
	    gdalconst.GDT_Byte: 'B',
	    gdalconst.GDT_Int16: 'h',
	    gdalconst.GDT_UInt16: 'H',
	    gdalconst.GDT_Int32: 'i',
	    gdalconst.GDT_UInt32: 'I',
	    gdalconst.GDT_Float32: 'f',
	    gdalconst.GDT_Float64: 'f'
	    }

    def _pt2fmt(self, pt):
        return self._fmttypes.get(pt, 'x')

    def get_value_at_position(self, lat, lon):
        ds = gdal.Open(self.file_name, gdalconst.GA_ReadOnly)
        if ds is None:
            self.logger.warning('Failed open file')
            return
        transf = ds.GetGeoTransform()
        cols = ds.RasterXSize
        rows = ds.RasterYSize
        bands = ds.RasterCount
        band = ds.GetRasterBand(1)
        bandtype = gdal.GetDataTypeName(band.DataType)
        driver = ds.GetDriver().LongName
        transfInv = gdal.InvGeoTransform(transf)
        px, py = gdal.ApplyGeoTransform(transfInv, lon, lat)
        structval = band.ReadRaster(int(px), int(py), 1, 1,
            buf_type=band.DataType)
        fmt = self._pt2fmt(band.DataType)
        value = struct.unpack(fmt, structval)
        return value[0]

if __name__ == "__main__":

    import pandas as pd
    data = pd.read_excel('maps/globcover2009/Globcover2009_Legend.xls')
    legend = data.set_index('Value').to_dict('index')
    gth = GeoTiffHandler('maps/globcover2009/GLOBCOVER_L4_200901_200912_V2.3.tif')
    print(legend.get(gth.get_value_at_position(52, 8)))
