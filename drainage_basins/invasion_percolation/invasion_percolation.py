def InvasionPercolation(lattice,heap,k):
    if lattice.sites[k].sigma == -1:
        for i in lattice.burner1:
            lattice.sites[i].status1 = -2
        lattice.burner1 = []
        heap.m = 0
        
        lattice.burner1.append(k)
        lattice.sites[k].status1 = 1
        
        t_old = k
        
        heap.Insert(lattice.sites[k].height,k)
        
        stop = False
        while heap.m > 0 and stop == False:
            _,t = heap.ExtractMin()
            
            lattice.sites[t].status1 = 2
            
            lattice.sites[t].parent = t_old
            t_old = t
            
            if lattice.sites[t].sigma >= 0:
                w = lattice.sites[t].sigma
                stop = True
            
            if lattice.sites[t].label == 1:
                w = t
                stop = True
            
            if stop == False:
                for s in lattice.GetNeighbors(t):
                    if lattice.sites[s].status1 == -2:
                        lattice.burner1.append(s)
                        lattice.sites[s].status1 = 1
                        
                        heap.Insert(lattice.sites[s].height,s)
        if stop:
            i = t
            while lattice.sites[i].parent != i:
                lattice.sites[i].sigma = w
                i = lattice.sites[i].parent
            lattice.sites[i].sigma = w
