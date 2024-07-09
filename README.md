![Untitled design (4)](https://github.com/devanys/RRT-path-planning/assets/145944367/91f73607-73dc-4d68-8bcb-f466e43e8cff)
### Implementation of Rapidly-exploring Random Tree (RRT)

RRT (Rapidly-exploring Random Tree) is an algorithm used for path planning in robotics and related fields. It efficiently searches high-dimensional spaces and is particularly useful in complex environments.

1. **Initialization:**
 - Start with an initial node (start) as the first node of the tree
 - Define the search space (e.g., the workspace boundaries of the robot).

2. **Tree Expansion:**
 - Random Sampling: Randomly sample a point (random_node) within the search space.
 - Nearest Neighbor: Find the nearest node in the tree (nearest_node) to the sampled point.
 - New Node Creation: Create a new node (new_node) by moving from the nearest_node towards the random_node by a fixed step size.
 - Obstacle Checking: Ensure the new_node and the path to it are not within any obstacles.
 - Add Node: If the new_node is valid (not in an obstacle), add it to the tree, connecting it to the nearest_node.

3. **Iterate:**
 - Repeat the tree expansion steps until the tree has grown sufficiently, or the goal has been reached.
 - Optionally, the goal can be checked at each iteration to see if the path has been found.

4. **Path Extraction:**
 - Once the tree reaches the goal region or a termination condition is met, extract the path by tracing back from the goal node to the start node using the parent pointers.

### References
- Jinshan Song, Satyandra K. Gupta, and Thomas A. Wettergren **"MRRT: Multiple Rapidly-Exploring Random Trees for Fast Online Replanning in Dynamic Environments"** 2023, DOI: 10.48550/arXiv.2104.11059
- James J. Kuffner and Steven M. LaValle **"RRT-Connect: An Efficient Approach to Single-Query Path Planning"** 2000, DOI: 10.1109/ICRA.2000.844730   
- Mathlab's youtube **"Autonomus Navigation"**, https://youtube.com/playlist?list=PLn8PRpmsu08rLRGrnF-S6TyGrmcA2X7kg&si=od9l4Bdib7LTQfav 
