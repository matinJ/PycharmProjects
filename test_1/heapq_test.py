import math
import random
import heapq
from cStringIO import StringIO

def show_tree(tree,total_width=36, fill=' '):
    output = StringIO()
    last_row = -1
    for i ,n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i+2,2)))
        else:
            row = 0
        if row !=last_row:
            output.write('\n')
        columns = 2**row
        col_width = int(math.floor((total_width*1.0)/columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print output.getvalue()
    print '_'*total_width
    print
    return
heap = []
data = random.sample(range(1,8),7)
print 'data:', data
show_tree(data)

for i in data:
    print 'add %3d:' %i
    heapq.heappush(heap, i)
    show_tree(heap)
