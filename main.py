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

# Helper function
def find_ones_indices(grid):
    indices = []
    rows = len(grid)
    
    for i in range(rows):
        cols = len(grid[i])
        for j in range(cols):
            if grid[i][j] == 1:
                indices.append((i, j))
    
    return indices

ocup_grid = generate_connected_zero_mass(rows=20, cols=40, zero_fraction=0.6)
enemy_map = place_enemies_in_map(ocup_grid)

# Get optimal starting positions
init_pos = place_agents(ocup_grid, num_agents=5, fov_radius=5)

# Two-pass
# if analyze_connected_regions(ocup_grid, init_pos) == 1:
#     print("Agent is surrounded.")
#     exit()

# Initialize DARP
darp_instance = DARP(nx=40, ny=20, notEqualPortions=False, given_initial_positions=init_pos, given_portions=[], obstacles_positions=find_ones_indices(ocup_grid), visualization=False,
                        MaxIter=80000, CCvariation=0.01,
                        randomLevel=0.0001, dcells=2, importance=False)

# Divide areas based on robots initial positions
DARP_success , iterations = darp_instance.divideRegions()
print(DARP_success)

