# python -B main.py belm_crop str1330_link 0 42
import sys
import random
from geotiff import ReadGeoTiff,ExtractFloatArrayFromGeoTiff,ExtractIntArrayFromGeoTiff,WriteGeoTiff
from lattice import Lattice
from heap import Heap
from drainage_basins import SetDrainageBasins,ReSetDrainageBasins

filename0 = sys.argv[1]
filename1 = sys.argv[2]
hcutoff = float(sys.argv[3])
seed = int(sys.argv[4])

random.seed(seed)

# INPUT
ds0 = ReadGeoTiff(filename0)
nrows,ncols,nodata0,arr0 = ExtractFloatArrayFromGeoTiff(ds0)

lattice = Lattice(nrows,ncols,arr0)

for k in range(lattice.n):
    if lattice.sites[k].height > hcutoff:
        lattice.sites[k].sigma = -1

ds1 = ReadGeoTiff(filename1)
nrows,ncols,nodata1,arr1 = ExtractIntArrayFromGeoTiff(ds1)

for k in range(lattice.n):
    lattice.sites[k].status = arr1[k]
    if lattice.sites[k].status >= 0:
        if lattice.sites[k].sigma == -1:
            lattice.sites[k].label = 1

heap = Heap(lattice.n)
# INPUT

# DRAINAGE_BASINS
SetDrainageBasins(lattice,heap)

nodata1 = ReSetDrainageBasins(nodata1,lattice)
# DRAINAGE_BASINS

# OUTPUT
WriteGeoTiff(ds0,nodata1,lattice,filename0)
# OUTPUT

del ds1
del ds0
