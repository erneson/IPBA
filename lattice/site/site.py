from random import random
import numpy as np

class Site:
    def __init__(self,height):
        self.height = np.float32(height+random())
        self.sigma = np.uint32(1)
        
        self.label = np.uint16(0)
        self.parent = np.uint32(0)
        
        self.status = np.uint16(0)

        self.status1 = np.uint8(0)
