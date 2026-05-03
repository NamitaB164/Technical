
import numpy as np
from scipy.spatial import KDTree


garments = [
    {"id": 1,  "chest": 90,  "waist": 75,  "hip": 95},
    {"id": 2,  "chest": 92,  "waist": 77,  "hip": 97},
    {"id": 3,  "chest": 94,  "waist": 79,  "hip": 99},
    {"id": 4,  "chest": 96,  "waist": 80,  "hip": 100},  
    {"id": 5,  "chest": 98,  "waist": 82,  "hip": 102},
    {"id": 6,  "chest": 100, "waist": 84,  "hip": 104},
    {"id": 7,  "chest": 88,  "waist": 73,  "hip": 93},   
    {"id": 8,  "chest": 95,  "waist": 80,  "hip": 100},  
    {"id": 9,  "chest": 97,  "waist": 81,  "hip": 101},
    {"id": 10, "chest": 102, "waist": 86,  "hip": 106},
]


user_chest = 96
user_waist = 80
user_hip   = 100

CHEST_WEIGHT = 2  
WAIST_WEIGHT = 1
HIP_WEIGHT   = 1

def apply_weights(chest, waist, hip):
    return [chest * CHEST_WEIGHT, waist * WAIST_WEIGHT, hip * HIP_WEIGHT]

points = []
for g in garments:
    weighted_point = apply_weights(g["chest"], g["waist"], g["hip"])
    points.append(weighted_point)

points = np.array(points)  

tree = KDTree(points)      


user_point = apply_weights(user_chest, user_waist, user_hip)

distances, indices = tree.query(user_point, k=5)

print("KD-Tree found these candidates (before penalty check):")
for i, idx in enumerate(indices):
    g = garments[idx]
    print(f"  Garment ID {g['id']} — chest:{g['chest']} waist:{g['waist']} hip:{g['hip']}  (distance: {distances[i]:.2f})")

def get_penalty(garment_size, user_size):
    diff = garment_size - user_size
    if diff <= -2:
        return float('inf') 
    if diff < 0:
        return abs(diff) * 10   
    else:
        return abs(diff) * 1   

def get_total_penalty(garment):
    chest_penalty = get_penalty(garment["chest"], user_chest)
    waist_penalty = get_penalty(garment["waist"], user_waist)
    hip_penalty   = get_penalty(garment["hip"],   user_hip)
    return (chest_penalty * CHEST_WEIGHT) + (waist_penalty * WAIST_WEIGHT) + (hip_penalty * HIP_WEIGHT)


candidates = []
for idx in indices:
    garment = garments[idx]
    penalty = get_total_penalty(garment)
    candidates.append({"id": garment["id"], "penalty": penalty})


candidates.sort(key=lambda x: x["penalty"])



worst_penalty = max(c["penalty"] for c in candidates)

for c in candidates:
    if worst_penalty == 0:
        c["fit_score"] = 100
    else:
        c["fit_score"] = round(100 - (c["penalty"] / worst_penalty * 100))


print("\nTOP 3 BEST FITTING GARMENTS:")

for i in range(3):
    g = candidates[i]
    print(f"Rank {i+1}: Garment ID = {g['id']}  |  Fit Score = {g['fit_score']}/100")
