import numpy as np
import random
import csv
import os

L = 200
vmax = 5
p = 0.3
density = 0.3
steps = 2000

num_cars = int(density * L)
positions = random.sample(range(L), num_cars)
velocities = {pos: 0 for pos in positions}

def distance_to_next(pos, positions):
    sorted_pos = sorted(positions)
    idx = sorted_pos.index(pos)
    next_pos = sorted_pos[(idx+1) % len(sorted_pos)]
    return (next_pos - pos - 1) % L

avalanche_sizes = []
current_avalanche = 0

for step in range(steps):
    new_positions = []
    new_velocities = {}
    jam_size = 0

    for pos in positions:
        v = velocities[pos]

        v = min(v + 1, vmax)
        d = distance_to_next(pos, positions)
        v = min(v, d)

        if random.random() < p:
            v = max(v - 1, 0)

        if v == 0:
            jam_size += 1

        new_pos = (pos + v) % L
        new_positions.append(new_pos)
        new_velocities[new_pos] = v

    if jam_size > 0:
        current_avalanche += jam_size
    elif current_avalanche > 0:
        avalanche_sizes.append(current_avalanche)
        current_avalanche = 0

    positions = new_positions
    velocities = new_velocities

os.makedirs("data", exist_ok=True)
with open("data/avalanche_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["size"])
    for s in avalanche_sizes:
        writer.writerow([s])

print("Simulation complete")
