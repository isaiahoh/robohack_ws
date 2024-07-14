"""
    Workflow: 
        - Get map from simulation 
        - Use art gallery to get optimal starting positions
        - Use two-pass over map
        - Use DARP to partition map
        - Use Kruskal to generate global plans
"""
from darp import DARP
# For now, generate random graph
from graph_gen import generate_connected_zero_mass, place_enemies_in_map
from art_gallery import place_agents
from two_pass import analyze_connected_regions
import numpy as np
import matplotlib.pyplot as plt

# Helper functions
def find_ones_indices(grid):
    indices = []
    rows = len(grid)
    
    for i in range(rows):
        cols = len(grid[i])
        for j in range(cols):
            if grid[i][j] == 1:
                indices.append((i, j))
    
    return indices

def flatten_tuple(t, rows, cols):
    flattened = ()
    return t[0] * rows + t[1]


ocup_grid = generate_connected_zero_mass(rows=16, cols=16, zero_fraction=0.7)
enemy_map = place_enemies_in_map(ocup_grid)

# Get optimal starting positions
NUM_AGENTS = int(4)

init_pos = place_agents(ocup_grid, num_agents=4, fov_radius=4)
for pos in init_pos:
    print(ocup_grid[pos[0],pos[1]])
print(len(init_pos))

# Two-pass
# if analyze_connected_regions(ocup_grid, init_pos) == 1:
#     print("Agent is surrounded.")
#     exit()

size = 1 / 4
portions = [size] * 4

for count,pos in enumerate(init_pos):
    x = pos[0]
    y = pos[1]
    ocup_grid[x][y] = 125+count
plt.imshow(ocup_grid)
plt.colorbar()
plt.show()

# Initialize DARP
darp_instance = DARP(nx=16, ny=16, notEqualPortions=False, given_initial_positions=init_pos, given_portions=portions, 
                        obstacles_positions=ocup_grid, visualization=True,
                        MaxIter=80000, CCvariation=0.01,
                        randomLevel=0.0001, dcells=2, importance=False)

# Divide areas based on robots initial positions
DARP_success , iterations = darp_instance.divideRegions()
print(DARP_success)

