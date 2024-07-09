import random
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps, ImageDraw

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

def distance(node1, node2):
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def is_in_obstacle(x, y, inflated_obstacle_map):
    return inflated_obstacle_map[int(y), int(x)] == 0

def line_in_obstacle(x0, y0, x1, y1, inflated_obstacle_map):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    line_points = list(bresenham(x0, y0, x1, y1))
    for x, y in line_points:
        if inflated_obstacle_map[y, x] == 0:
            return True
    return False

def bresenham(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        yield x0, y0
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def nearest_node(tree, random_node):
    return min(tree, key=lambda node: distance(node, random_node))

def get_new_node(nearest, random_node, step_size):
    theta = math.atan2(random_node.y - nearest.y, random_node.x - nearest.x)
    new_x = nearest.x + step_size * math.cos(theta)
    new_y = nearest.y + step_size * math.sin(theta)
    new_node = Node(new_x, new_y, nearest)
    return new_node

def rewire(tree, new_node, radius, inflated_obstacle_map):
    for node in tree:
        if node != new_node.parent and node.parent is not None:
            if distance(node, new_node) < radius and not line_in_obstacle(node.x, node.y, new_node.x, new_node.y, inflated_obstacle_map):
                new_cost = distance(new_node, new_node.parent) + distance(new_node.parent, node)
                current_cost = distance(node, node.parent)
                if new_cost < current_cost:
                    node.parent = new_node

def get_path(goal_node):
    path = []
    node = goal_node
    while node is not None:
        path.append(node)
        node = node.parent
    return path[::-1]

def plot_rrt_star(tree, path=None, obstacle_map=None):
    if obstacle_map is not None:
        plt.imshow(obstacle_map, cmap='gray', origin='lower')

    for node in tree:
        if node.parent is not None:
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], 'k-', lw=0.5)

    if path:
        path_x = [node.x for node in path]
        path_y = [node.y for node in path]
        plt.plot(path_x, path_y, 'r-', lw=2)

    plt.scatter([node.x for node in tree], [node.y for node in tree], c='b')
    plt.scatter([start.x], [start.y], c='g', marker='o')
    plt.scatter([goal.x], [goal.y], c='r', marker='x')
    plt.show()

num_nodes = 500
step_size = 10
radius = 15
x_max = 1500
y_max = 900

image_path = 'Obsticle.png'
original_image = Image.open(image_path).convert('L')
obstacle_map = np.array(original_image)

inflated_obstacle_map = ImageOps.expand(original_image, border=5, fill=255)
draw = ImageDraw.Draw(inflated_obstacle_map)
for y in range(obstacle_map.shape[0]):
    for x in range(obstacle_map.shape[1]):
        if obstacle_map[y, x] == 0:
            draw.rectangle([x, y, x + 10, y + 10], fill=0)

inflated_obstacle_map = np.array(inflated_obstacle_map)

start = Node(400, 200)
goal = Node(1050, 600)
tree = [start]

while len(tree) < num_nodes:
    rand_x = random.uniform(0, x_max)
    rand_y = random.uniform(0, y_max)
    random_node = Node(rand_x, rand_y)

    nearest = nearest_node(tree, random_node)
    new_node = get_new_node(nearest, random_node, step_size)

    if not is_in_obstacle(new_node.x, new_node.y, inflated_obstacle_map) and not line_in_obstacle(nearest.x, nearest.y, new_node.x, new_node.y, inflated_obstacle_map):
        tree.append(new_node)
        rewire(tree, new_node, radius, inflated_obstacle_map)

        if distance(new_node, goal) < step_size:
            goal.parent = new_node
            tree.append(goal)
            break

path = get_path(goal) if goal in tree else None

if path:
    print("Path found:")
    for node in path:
        print(f"Node: ({node.x}, {node.y})")
else:
    print("No path found")

plot_rrt_star(tree, path, obstacle_map)
