import random


def get_obstacles():
    num_of_obstacles = 10
    obstacles = []

    for _ in range(1, num_of_obstacles + 1):
        x = random.randint(-100, 100)
        y = random.randint(-50, 50)
        obstacles.append((x, y))
        
    return obstacles


def is_position_blocked(x, y, my_turtle=None, obstacles=None):
    is_blocked = False

    if isinstance(obstacles, list) and my_turtle:

        if (x, y) in obstacles:
            is_blocked = True

    return is_blocked
