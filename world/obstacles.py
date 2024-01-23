import random


def get_obstacles():
    num_of_obstacles = 10
    obstacles = []

    for _ in range(1, num_of_obstacles + 1):
        x = random.randint(-100, 100)
        y = random.randint(-50, 50)
        obstacles.append((x, y))
        
    return obstacles


def is_position_blocked(x, y,direction=None, my_turtle=None, obstacles=None):
    is_blocked = False

    if isinstance(obstacles, list) and my_turtle:
        current_pos = my_turtle.pos()
        print('current pos: ', my_turtle.pos())
        print('new pos: ', (x, y))

        x_negative = []
        x_positive = []

        if direction == 'forward':
            # updating y values, so check y values
            if current_pos[0] >= 0:
                print('get all positive x')
                x_positive = [x for x in obstacles if x[0] >= 0]
                print(x_positive)

                x_values = [n[1] for n in x_positive if n[0] == current_pos[0]]
                print(x_values)

                if len(x_values) and min(x_values) and y >= min(x_values):
                    is_blocked = True

            else:
                x_negative = [x for x in obstacles if x[0] < 0]
                print('get all negative x')
                print(x_negative)

                x_values = [n[1] for n in x_negative if n[0] == current_pos[0]]
                print(min(x_values))

                if len(x_values) and min(x_values) and y >= min(x_values):
                    is_blocked = True

        if direction == 'right':
            print('direction is: ', direction)


    return is_blocked
