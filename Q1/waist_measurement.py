import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math


file_name = r'C:\Users\lenovo\Desktop\Technical\Q1\image_smpl.obj'

mesh = trimesh.load(file_name)

# target height
h = 0.191
v = mesh.vertices
f = mesh.faces


# list of lines
lines = []

# loop over all faces
for i in range(len(f)):
    face = f[i]
    # get z of vertices
    z1 = v[face[0]][1]
    z2 = v[face[1]][1]
    z3 = v[face[2]][1]
    
    # check if face crosses h
    if (z1 < h and z2 < h and z3 < h):
        continue
    if (z1 > h and z2 > h and z3 > h):
        continue
        
    pts = []
    
    # edge 1
    if (z1 <= h and z2 >= h) or (z2 <= h and z1 >= h):
        if z1 == z2:
            t = 0.5
        else:
            t = (h - z1) / (z2 - z1)
        # get point
        x = v[face[0]][0] + t * (v[face[1]][0] - v[face[0]][0])
        y = v[face[0]][1] + t * (v[face[1]][1] - v[face[0]][1])
        z = v[face[0]][2] + t * (v[face[1]][2] - v[face[0]][2])
        pts.append([x, y, z])
        
    # edge 2
    if (z2 <= h and z3 >= h) or (z3 <= h and z2 >= h):
        if z2 == z3:
            t = 0.5
        else:
            t = (h - z2) / (z3 - z2)
        # get point
        x = v[face[1]][0] + t * (v[face[2]][0] - v[face[1]][0])
        y = v[face[1]][1] + t * (v[face[2]][1] - v[face[1]][1])
        z = v[face[1]][2] + t * (v[face[2]][2] - v[face[1]][2])
        pts.append([x, y, z])
        
    # edge 3
    if (z3 <= h and z1 >= h) or (z1 <= h and z3 >= h):
        if z3 == z1:
            t = 0.5
        else:
            t = (h - z3) / (z1 - z3)
        # get point
        x = v[face[2]][0] + t * (v[face[0]][0] - v[face[2]][0])
        y = v[face[2]][1] + t * (v[face[0]][1] - v[face[2]][1])
        z = v[face[2]][2] + t * (v[face[0]][2] - v[face[2]][2])
        pts.append([x, y, z])
        
    if len(pts) == 2:
        lines.append([pts[0], pts[1]])

print("lines", len(lines))

# round off  points
rounded = []
for i in range(len(lines)):
    pt1 = lines[i][0]
    pt2 = lines[i][1]
    
    r_pt1 = [round(pt1[0], 3), round(pt1[1], 3), round(pt1[2], 3)]
    r_pt2 = [round(pt2[0], 3), round(pt2[1], 3), round(pt2[2], 3)]
    
    rounded.append([r_pt1, r_pt2])


my_dict = {}
my_dict2 = {}
current_number = 0
edges = []

for i in range(len(rounded)):
    t1 = (rounded[i][0][0], rounded[i][0][1], rounded[i][0][2])
    t2 = (rounded[i][1][0], rounded[i][1][1], rounded[i][1][2])
    
    if t1 not in my_dict:
        my_dict[t1] = current_number
        my_dict2[current_number] = lines[i][0]
        current_number = current_number + 1
        
    if t2 not in my_dict:
        my_dict[t2] = current_number
        my_dict2[current_number] = lines[i][1]
        current_number = current_number + 1
        
    edges.append((my_dict[t1], my_dict[t2]))

# graph
graph = {}
for i in range(len(edges)):
    u = edges[i][0]
    v_node = edges[i][1]
    if u not in graph:
        graph[u] = []
    if v_node not in graph:
        graph[v_node] = []
    graph[u].append(v_node)
    graph[v_node].append(u)

visited = []
loops = []

for i in range(current_number):
    if i not in visited:
        curr = i
        my_loop = []
        last = -1
        
        while True:
            if curr in visited:
                break
            visited.append(curr)
            my_loop.append(my_dict2[curr])
            
            n = graph[curr]
            next_node = -1
            for j in range(len(n)):
                if n[j] != last:
                    next_node = n[j]
                    break
            
            if next_node == -1:
                break
                
            last = curr
            curr = next_node
            
        if len(my_loop) > 2:
            loops.append(my_loop)

print("loops", len(loops))

#  biggest loop
biggest_size = 0
biggest_loop = []
for i in range(len(loops)):
    if len(loops[i]) > biggest_size:
        biggest_size = len(loops[i])
        biggest_loop = loops[i]

# calc length
total_length = 0
for i in range(len(biggest_loop)):
    p1 = biggest_loop[i]
    if i == len(biggest_loop) - 1:
        p2 = biggest_loop[0]
    else:
        p2 = biggest_loop[i + 1]
        
    dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
    total_length = total_length + dist

print("Circumference:", total_length)


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# plot 
loop_xs = []
loop_ys = []
loop_zs = []
for i in range(len(biggest_loop)):
    loop_xs.append(biggest_loop[i][0])
    loop_ys.append(biggest_loop[i][1])
    loop_zs.append(biggest_loop[i][2])
    
loop_xs.append(biggest_loop[0][0])
loop_ys.append(biggest_loop[0][1])
loop_zs.append(biggest_loop[0][2])

ax.plot(loop_xs, loop_ys, loop_zs, color='black', linewidth=3)

plt.savefig('visualization.png')
