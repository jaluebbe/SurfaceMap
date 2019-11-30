import gdal
import gdalconst
import struct

class GeoTiffHandler:

    def __init__(self, file_name):
        self._fmttypes = {
	    gdalconst.GDT_Byte: 'B',
	    gdalconst.GDT_Int16: 'h',
	    gdalconst.GDT_UInt16: 'H',
	    gdalconst.GDT_Int32: 'i',
	    gdalconst.GDT_UInt32: 'I',
	    gdalconst.GDT_Float32: 'f',
	    gdalconst.GDT_Float64: 'f'
	    }
        self.ds = gdal.Open(file_name, gdalconst.GA_ReadOnly)
        if self.ds is None:
            raise FileNotFoundError(file_name)
        self.transf = self.ds.GetGeoTransform()
        self.cols = self.ds.RasterXSize
        self.rows = self.ds.RasterYSize
        self.bands = self.ds.RasterCount
        self.transfInv = gdal.InvGeoTransform(self.transf)

    def _pt2fmt(self, pt):
        return self._fmttypes.get(pt, 'x')

    def get_value_at_position(self, lat, lon, raster_band=1):
        band = self.ds.GetRasterBand(raster_band)
        bandtype = gdal.GetDataTypeName(band.DataType)
        px, py = gdal.ApplyGeoTransform(self.transfInv, lon, lat)
        if px > self.cols or py > self.rows:
            return None
        structval = band.ReadRaster(int(px), int(py), 1, 1,
            buf_type=band.DataType)
        fmt = self._pt2fmt(band.DataType)
        value = struct.unpack(fmt, structval)
        if value[0] == band.GetNoDataValue():
            if fmt == 'f':
                return float('nan')
            else:
                return None
        else:
            result = value[0]
        return value[0]

    def get_values_at_position(self, lat, lon):
        results = []
        for raster_band in range(1, self.bands+1):
            results.append(self.get_value_at_position(lat, lon, raster_band))
        return results
