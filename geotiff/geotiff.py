from osgeo import gdal
import numpy as np
import random as rand

def ReadGeoTiff(filename,isfloat=True):
    ds = gdal.Open(r'datasets/{}.tif'.format(filename))
    
    info = {}
    info['RasterYSize'] = ds.RasterYSize
    info['RasterXSize'] = ds.RasterXSize
    info['GeoTransform'] = ds.GetGeoTransform()
    info['Projection'] = ds.GetProjection()
    
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray()

    info['NoDataValue'] = -99999. if isfloat else 0
    arr = np.where(arr == nodata,info['NoDataValue'],arr)

    del band
    del ds

    return info,arr.flatten()

def WriteGeoTiff(info,lattice,filename):
    arr = np.zeros((lattice.nrows,lattice.ncols),dtype=np.uint16)
    for j in range(lattice.nrows):
        for i in range(lattice.ncols):
            k = i+j*lattice.ncols
            
            arr[j,i] = lattice.sites[k].status

    driver = gdal.GetDriverByName('GTiff')
    ds = driver.Create(r'results/{}.tif'.format(filename),
                       info['RasterXSize'],
                       info['RasterYSize'],
                       1,
                       gdal.GDT_UInt16)
    ds.SetGeoTransform(info['GeoTransform'])
    ds.SetProjection(info['Projection'])
    
    d = np.unique(arr)
    N = d.shape[0]
    colors = [(0.0,0.0,0.0)]+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N)]

    ds.GetRasterBand(1).SetNoDataValue(0)
    ds.GetRasterBand(1).WriteArray(arr)
    
    band = ds.GetRasterBand(1)
    color_table = gdal.ColorTable()
    
    for i,color in enumerate(colors):
        color_table.SetColorEntry(i,(int(255*color[0]),
                                     int(255*color[1]),
                                     int(255*color[2])))
    
    band.SetRasterColorTable(color_table)
    band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
    
    ds.FlushCache()
    
    del band
    del ds
