# python -B main.py belm_crop str1330_link 42 F
import sys
import random
import numpy as np

from geotiff import ReadGeoTiff,WriteGeoTiff
from lattice import Lattice
from heap import Heap
from drainage_basins import SetDrainageBasins

filename0 = sys.argv[1]
filename1 = sys.argv[2]
seed = int(sys.argv[3])
ispbc = sys.argv[4] == 'T'

random.seed(seed)

# INPUT
info,arr0 = ReadGeoTiff(filename0) # float array
nrows = info['RasterYSize']
ncols = info['RasterXSize']
nodata = info['NoDataValue']

lattice = Lattice(nrows,ncols,arr0)

for k in range(lattice.n):
    if arr0[k] == nodata:
        lattice.sites[k].height = np.float32(nodata)
        lattice.sites[k].sigma = np.uint32(0)

_,arr1 = ReadGeoTiff(filename1,False) # int array

isfilled = False
for k in range(lattice.n):
    if arr1[k] > 0:
        isfilled = True
        lattice.sites[k].label = np.uint16(arr1[k])

if isfilled:
    heap = Heap(lattice.n)
    # INPUT

    # DRAINAGE_BASINS
    SetDrainageBasins(lattice,heap,ispbc)
    # DRAINAGE_BASINS

    for k in range(lattice.n):
        del lattice.sites[k].height
        del lattice.sites[k].sigma
        del lattice.sites[k].label
        del lattice.sites[k].parent
        del lattice.sites[k].status1

    # OUTPUT
    WriteGeoTiff(info,lattice,filename0)
    # OUTPUT
else:
    print('The dataset {} has no sink!'.format(filename1))
