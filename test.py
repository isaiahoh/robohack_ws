import numpy as np
from art_gallery import place_agents
from two_pass import analyze_connected_regions
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Example usage
    occupancy_map = np.array([
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ])

    num_agents = 3
    fov_radius = 2

    agent_positions = place_agents(occupancy_map, num_agents, fov_radius)
    print("Agent positions:", agent_positions)
    for agent_pos in agent_positions:
        print(analyze_connected_regions(occupancy_map, agent_pos))
    occupancy_map = occupancy_map * 255
    for count,pos in enumerate(agent_positions):
        x = pos[0]
        y = pos[1]
        occupancy_map[x][y] = 125+count
    plt.imshow(occupancy_map)
    plt.colorbar()
    plt.show()
    