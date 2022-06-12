from osgeo import gdal
import numpy as np
import random as rand

def ReadGeoTiff(filename):
    ds = gdal.Open(r'datasets/{}.tif'.format(filename))
    return ds

def ExtractFloatArrayFromGeoTiff(ds):
    nrows,ncols = ds.RasterYSize,ds.RasterXSize
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray()

    new_nodata = -99999.
    arr = np.where(arr == nodata,new_nodata,arr)

    return nrows,ncols,new_nodata,arr.flatten()

def ExtractIntArrayFromGeoTiff(ds):
    nrows,ncols = ds.RasterYSize,ds.RasterXSize
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray()

    new_nodata = 0
    arr = np.where(arr == nodata,new_nodata,arr)
    
    return nrows,ncols,new_nodata,arr.flatten()

def WriteGeoTiff(ds,nodata,lattice,filename):
    arr = np.zeros((lattice.nrows,lattice.ncols),dtype=np.uint16)
    for j in range(lattice.nrows):
        for i in range(lattice.ncols):
            k = i+j*lattice.ncols
            
            arr[j,i] = lattice.sites[k].status

    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(r'results/{}.tif'.format(filename),
                           ds.RasterXSize,
                           ds.RasterYSize,
                           1,
                           gdal.GDT_UInt16)
    out_ds.SetGeoTransform(ds.GetGeoTransform())
    out_ds.SetProjection(ds.GetProjection())
    
    d = np.unique(arr)
    N = d.shape[0]
    colors = [(0.0,0.0,0.0)]+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N)]

    out_ds.GetRasterBand(1).SetNoDataValue(0)
    out_ds.GetRasterBand(1).WriteArray(arr)
    
    band = out_ds.GetRasterBand(1)
    color_table = gdal.ColorTable()
    
    for i,color in enumerate(colors):
        color_table.SetColorEntry(i,(int(255*color[0]),
                                     int(255*color[1]),
                                     int(255*color[2])))
    
    band.SetRasterColorTable(color_table)
    band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
    
    out_ds.FlushCache()
    
    del band
    del out_ds
