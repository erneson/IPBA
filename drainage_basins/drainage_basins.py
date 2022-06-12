from .invasion_percolation import InvasionPercolation

def SetDrainageBasins(lattice,heap):
    for k in range(lattice.n):
        InvasionPercolation(lattice,heap,k)
