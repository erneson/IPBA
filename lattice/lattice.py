from .site import Site
import numpy as np

class Lattice:
    def __init__(self,nrows,ncols,arr):
        self.nrows = nrows
        self.ncols = ncols
        self.n = self.nrows*self.ncols
        
        self._SetLattice(arr)
        
        self.burner1 = []
    
    def _SetLattice(self,arr):
        self.sites = np.empty(self.n,dtype=Site)
        for k in range(self.n):
            self.sites[k] = Site(arr[k])
    
    def GetNeighbors(self,k,ispbc=False):
        neighbors = []
        if k < self.ncols:
            if k%self.ncols == 0:
                neighbors.append(k+1)
                for r in range(self.ncols):
                    s = r
                    if s != k+self.ncols-1 and s != k and s != k+1:
                        if ispbc:
                            neighbors.append(s)
                if ispbc:
                    neighbors.append(k+self.ncols-1)
                neighbors.append(k+self.ncols)
            elif k%self.ncols == self.ncols-1:
                if ispbc:
                    neighbors.append(k-self.ncols+1)
                for r in range(self.ncols):
                    s = r
                    if s != k-1 and s != k and s != k-self.ncols+1:
                        if ispbc:
                            neighbors.append(s)
                neighbors.append(k-1)
                neighbors.append(k+self.ncols)
            else:
                for r in range(self.ncols):
                    s = r
                    if s != k-1 and s != k and s != k+1:
                        if ispbc:
                            neighbors.append(s)
                    else:
                        if s == k-1 or s == k+1:
                            neighbors.append(s)
                neighbors.append(k+self.ncols)
        elif k >= self.ncols*(self.nrows-1):
            if k%self.ncols == 0:
                neighbors.append(k-self.ncols)
                neighbors.append(k+1)
                for r in range(self.ncols):
                    s = r+self.ncols*(self.nrows-1)
                    if s != k-1+self.ncols and s != k and s != k+1:
                        if ispbc:
                            neighbors.append(s)
                if ispbc:
                    neighbors.append(k-1+self.ncols)
            elif k%self.ncols == self.ncols-1:
                neighbors.append(k-self.ncols)
                if ispbc:
                    neighbors.append(k-self.ncols+1)
                for r in range(self.ncols):
                    s = r+self.ncols*(self.nrows-1)
                    if s != k-1 and s != k and s != k-self.ncols+1:
                        if ispbc:
                            neighbors.append(s)
                neighbors.append(k-1)
            else:
                neighbors.append(k-self.ncols)
                for r in range(self.ncols):
                    s = r+self.ncols*(self.nrows-1)
                    if s != k-1 and s != k and s != k+1:
                        if ispbc:
                            neighbors.append(s)
                    else:
                        if s == k-1 or s == k+1:
                            neighbors.append(s)
        else:
            if k%self.ncols == 0:
                neighbors.append(k-self.ncols)
                neighbors.append(k+1)
                if ispbc:
                    neighbors.append(k-1+self.ncols)
                neighbors.append(k+self.ncols)
            elif k%self.ncols == self.ncols-1:
                neighbors.append(k-self.ncols)
                if ispbc:
                    neighbors.append(k-self.ncols+1)
                neighbors.append(k-1)
                neighbors.append(k+self.ncols)
            else:
                neighbors.append(k-self.ncols)
                neighbors.append(k-1)
                neighbors.append(k+1)
                neighbors.append(k+self.ncols)
        return neighbors
