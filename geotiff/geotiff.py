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
    
    new_nodata = -9999.
    arr = np.where(arr == nodata,new_nodata,arr)
    
    return nrows,ncols,new_nodata,arr.flatten()

def ExtractIntArrayFromGeoTiff(ds):
    nrows,ncols = ds.RasterYSize,ds.RasterXSize
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray()
    
    new_nodata = -9999
    arr = np.where(arr == nodata,float(new_nodata),arr).astype(np.int32)
    
    return nrows,ncols,new_nodata,arr.flatten()

def WriteGeoTiff(ds,nodata,lattice,filename):
    d = {}
    arr = np.zeros((lattice.nrows,lattice.ncols),dtype=np.int32)
    for j in range(lattice.nrows):
        for i in range(lattice.ncols):
            k = i+j*lattice.ncols
            
            arr[j,i] = lattice.sites[k].sigma
            
            s = arr[j,i]
            if s in d:
                d[s].append((j,i))
            else:
                d[s] = [(j,i)]
    
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(r'results/{}.tif'.format(filename),
                           ds.RasterXSize,
                           ds.RasterYSize,
                           1,
                           gdal.GDT_UInt16)
    out_ds.SetGeoTransform(ds.GetGeoTransform())
    out_ds.SetProjection(ds.GetProjection())
    
    N = len(d)
    keys = sorted(d.keys())
    
    for t,k in enumerate(keys):
        for j,i in d[k]:
            arr[j,i] = t
    
    if keys[0] == nodata:
        out_ds.GetRasterBand(1).SetNoDataValue(0)
        
        if keys[1] == -2:
            if keys[2] == -1:
                colors = [(0.5,0.5,0.5)]
                colors = colors+[(1.0,1.0,1.0)]
                colors = colors+[(0.0,0.0,0.0)]
                colors = colors+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N-3)]
            else:
                colors = [(0.5,0.5,0.5)]
                colors = colors+[(1.0,1.0,1.0)]
                colors = colors+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N-2)]
        else:
            if keys[1] == -1:
                colors = [(0.5,0.5,0.5)]
                colors = colors+[(0.0,0.0,0.0)]
                colors = colors+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N-2)]
            else:
                colors = [(0.5,0.5,0.5)]
                colors = colors+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N-1)]
    else:
        if keys[0] == -2:
            if keys[1] == -1:
                colors = [(1.0,1.0,1.0)]
                colors = colors+[(0.0,0.0,0.0)]
                colors = colors+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N-2)]
            else:
                colors = [(1.0,1.0,1.0)]
                colors = colors+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N-1)]
        else:
            if keys[0] == -1:
                colors = colors+[(0.0,0.0,0.0)]
                colors = colors+[(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N-1)]
            else:
                colors = [(0.2+0.6*rand.random(),0.2+0.6*rand.random(),0.2+0.6*rand.random()) for i in range(N)]
    
    out_ds.GetRasterBand(1).WriteArray(arr.astype(np.uint16))
    
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
