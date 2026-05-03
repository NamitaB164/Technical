import trimesh

mesh = trimesh.load('c:\\Users\\lenovo\\Downloads\\image_smpl(1).obj')
print("Bounds:", mesh.bounds)
print("Center:", mesh.centroid)
print("Extents:", mesh.extents)
