from .invasion_percolation import InvasionPercolation

def SetDrainageBasins(lattice,heap,pbc):
    for k in range(lattice.n):
        InvasionPercolation(lattice,heap,k,pbc)
