from .invasion_percolation import InvasionPercolation

def SetDrainageBasins(lattice,heap,ispbc):
    for k in range(lattice.n):
        InvasionPercolation(lattice,heap,k,ispbc)
