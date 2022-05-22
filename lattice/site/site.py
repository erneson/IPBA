from random import random

class Site:
    def __init__(self,height):
        self.height = height+random()
        self.sigma = -2
        
        self.status = -2
        self.label = -2
        self.parent = -2
        
        self.status1 = -2
