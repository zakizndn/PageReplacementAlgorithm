from queue import Queue

# Runs the least recently used algorithm
def run_lru(rs, mnf):
    faults = 0
    pagenums = set(rs)
    frames = mnf*[-1]
    page_data = {}

    for t,r in enumerate(rs):
        if not(r in frames):
            if -1 in frames:
                frames[ frames.index(-1) ] = r
            else:
                victim_page = min(page_data, key = page_data.get)
                frames[ frames.index(victim_page) ] = r
                del page_data[victim_page]
            faults += 1
        page_data[r] = t

    return faults

# Runs the most recently used algorithm
def run_mru(rs, mnf): # This algorithm replaces the most recently accessed page from memory.
    faults = 0
    l = []
    i = 0

    while(1): # Adding pages to memory initially till its capacity
        if(rs[i] not in l): # Check if page is present and if not present, add it to memory.
            l.append(rs[i])
            i += 1
            faults += 1 # Increment faults because page is not in memory.
            if(len(l) == mnf):
                break
        else:
            i += 1
            continue

    for i in range(mnf,len(rs)): # After memory is full, we replace the page in memory with coming page in queue.
        if rs[i] not in l:
            faults += 1
            l.pop(-1) # We remove recently ued page from memory using pop.
            l.append(rs[i])
        else:
            l.remove(rs[i]) # If page is found already in memory, there is no fault.
            
            l.append(rs[i]) # We update the list such that the most recently accessed page gets to the last position in list.
    l.clear()

    return faults

# Runs the least frequently used algorithm
def run_lfu(rs, mnf): # This algorithm replaces the page that has least frequency of occurrence in list.
    l = []
    faults = 0
    temp = []
    i = 0

    while(1): # Adding pages to memory initially till its capacity
        if(rs[i] not in l): # Check if page is present and if not present, add it to memory.
            l.append(rs[i])
            i += 1
            faults += 1 # Increment faults because page is not in memory.
            if(len(l) == mnf):
                break
        else:
            i += 1
            continue

    for i in range(mnf,len(rs)): # After memory is full, we replace the least frequency pages with coming page.
        if rs[i] in l:
            continue
        else:
            faults += 1
            temp = []
            for j in l: # Finding the least frequency page in memory.
                temp.append(rs[:i].count(j)) # Obtain frequencies of every page and store them in temp list.
            index = temp.index(min(temp)) # Obtain least frequency using min() and get index of it.
        
            l.pop(index) # Using that index, we remove the page from list
            l.append(rs[i]) # We append new page to that list.
    
    return faults

# Runs the least frequently used algorithm
def run_fifo(rs, mnf):
    n = len(rs)
    s = set()
    indexes = Queue()
    faults = 0
    
    for i in range(n):
        if (len(s) < mnf):
            if (rs[i] not in s):
                s.add(rs[i])
                faults += 1
                indexes.put(rs[i])
        else:
            if (rs[i] not in s):
                val = indexes.queue[0]
                indexes.get()
                s.remove(val)
                s.add(rs[i])
                indexes.put(rs[i])
                faults += 1

    return faults


def test_all_funcs(rs, mnf):
    print('\n'+(80*'*'))
    print('Reference string: ',rs)
    print('Maximum number of frames in memory: ', mnf)
    print('Number of page faults from FIFO: ',run_fifo(rs, mnf))
    print('Number of page faults from LFU: ',run_lfu(rs, mnf))
    print('Number of page faults from LRU: ',run_lru(rs, mnf))
    print('Number of page faults from MRU: ',run_mru(rs, mnf))
    print((80*'*')+'\n')

rs = [0, 2, 1, 6, 4, 0, 1, 0, 3, 1, 2, 1]
mnf = 4
test_all_funcs(rs, mnf)

rs = [9, 6, 4, 2, 0, 3, 1, 9, 3, 4, 5, 6, 2, 7, 8]
mnf = 3
test_all_funcs(rs, mnf)
