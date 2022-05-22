import numpy as np

class Heap:
    def __init__(self,n):
        self.n = n
        self.m = 0
        self.key = np.empty(self.n,dtype=np.float32)
        self.item = np.empty(self.n,dtype=np.int32)
    
    def _Parent(self,i):
        return (i-1)//2
    
    def _Left(self,i):
        return 2*i+1
    
    def _Right(self,i):
        return 2*i+2
    
    def _DecreaseKey(self,i,key,item):
        self.key[i] = key
        self.item[i] = item
        
        p = self._Parent(i)
        while i > 0 and self.key[p] > self.key[i]:
            self.key[i],self.key[p] = self.key[p],self.key[i]
            self.item[i],self.item[p] = self.item[p],self.item[i]
            
            i = p
            p = self._Parent(i)
    
    def _Heapify(self,i):
        l = self._Left(i)
        r = self._Right(i)
        
        if l < self.m and self.key[l] < self.key[i]:
            smallest = l
        else:
            smallest = i
        
        if r < self.m and self.key[r] < self.key[smallest]:
            smallest = r
        
        if smallest != i:
            self.key[i],self.key[smallest] = self.key[smallest],self.key[i]
            self.item[i],self.item[smallest] = self.item[smallest],self.item[i]
            
            self._Heapify(smallest)
    
    def Insert(self,key,item):
        self.m += 1
        self._DecreaseKey(self.m-1,key,item)
    
    def ExtractMin(self):
        key = self.key[0]
        item = self.item[0]
        
        self.key[0] = self.key[self.m-1]
        self.item[0] = self.item[self.m-1]
        self.m -= 1
        
        self._Heapify(0)
        
        return key,item
