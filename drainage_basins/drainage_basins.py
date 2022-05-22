from .invasion_percolation import InvasionPercolation

def SetDrainageBasins(lattice,heap):
    for k in range(lattice.n):
        InvasionPercolation(lattice,heap,k)

def ReSetDrainageBasins(nodata1,lattice):
    new_nodata = -(lattice.n+1)
    max_sigma = 0
    for k in range(lattice.n):
        if lattice.sites[k].sigma == nodata1:
            lattice.sites[k].sigma = new_nodata
        if lattice.sites[k].sigma > max_sigma:
            max_sigma = lattice.sites[k].sigma
    
    for k in range(lattice.n):
        if lattice.sites[k].status >= 0:
            pi = lattice.sites[k].sigma
            
            lattice.sites[pi].sigma = -lattice.sites[k].status
    
    nodata1 = new_nodata
    for k in range(lattice.n):
        if lattice.sites[k].sigma >= 0:
            pi = lattice.sites[k].sigma
            label = -lattice.sites[pi].sigma + max_sigma
        else:
            if lattice.sites[k].sigma == nodata1:
                label = lattice.sites[k].sigma
            else:
                label = -lattice.sites[k].sigma + max_sigma
        lattice.sites[k].label = label
    
    for k in range(lattice.n):
        lattice.sites[k].sigma = lattice.sites[k].label
    
    return new_nodata
