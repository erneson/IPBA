# python -B main.py belm_crop str1330_link 42
import sys
import random
import numpy as np

from geotiff import ReadGeoTiff,ExtractFloatArrayFromGeoTiff,ExtractIntArrayFromGeoTiff,WriteGeoTiff
from lattice import Lattice
from heap import Heap
from drainage_basins import SetDrainageBasins

filename0 = sys.argv[1]
filename1 = sys.argv[2]
seed = int(sys.argv[3])

random.seed(seed)

# INPUT
ds0 = ReadGeoTiff(filename0)
nrows,ncols,nodata0,arr0 = ExtractFloatArrayFromGeoTiff(ds0)

lattice = Lattice(nrows,ncols,arr0)

for k in range(lattice.n):
    if arr0[k] == nodata0:
        lattice.sites[k].height = np.float32(nodata0)
        lattice.sites[k].sigma = np.uint32(0)

ds1 = ReadGeoTiff(filename1)
nrows,ncols,nodata1,arr1 = ExtractIntArrayFromGeoTiff(ds1)

for k in range(lattice.n):
    if arr1[k] > 0:
        lattice.sites[k].label = np.uint16(arr1[k])

heap = Heap(lattice.n)
# INPUT

# DRAINAGE_BASINS
SetDrainageBasins(lattice,heap)
# DRAINAGE_BASINS

# OUTPUT
WriteGeoTiff(ds0,nodata1,lattice,filename0)
# OUTPUT

del ds1
del ds0
