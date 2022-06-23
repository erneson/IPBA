import numpy as np

def InvasionPercolation(lattice,heap,k,pbc):
    if lattice.sites[k].sigma == 1:
        for i in lattice.burner1:
            lattice.sites[i].status1 = np.uint8(0)
        lattice.burner1 = []
        heap.m = 0
        
        lattice.burner1.append(np.uint32(k))
        lattice.sites[k].status1 = np.uint8(1)
        
        t_old = k
        
        heap.Insert(lattice.sites[k].height,k)
        
        stop = False
        while heap.m > 0 and stop == False:
            _,t = heap.ExtractMin()
            
            lattice.sites[t].status1 = np.uint8(2)
            
            lattice.sites[t].parent = np.uint32(t_old)
            t_old = t
            
            if lattice.sites[t].sigma >= 2:
                w = int(lattice.sites[t].sigma)-2
                stop = True
            
            if lattice.sites[t].label > 0:
                w = t
                stop = True
            
            if stop == False:
                for s in lattice.GetNeighbors(t,pbc):
                    if lattice.sites[s].status1 == 0:
                        lattice.burner1.append(np.uint32(s))
                        lattice.sites[s].status1 = np.uint8(1)
                        
                        heap.Insert(lattice.sites[s].height,s)
        if stop:
            i = t
            while lattice.sites[i].parent != i:
                lattice.sites[i].sigma = np.uint32(w+2)
                lattice.sites[i].status = lattice.sites[w].label
                
                i = lattice.sites[i].parent
            
            lattice.sites[i].sigma = np.uint32(w+2)
            lattice.sites[i].status = lattice.sites[w].label
