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

        if direction == 'forward':
            # get positive y values
            
            # y_positive = [x[1] for x in obstacles is x >= 0]
            y_positive = []

            for i in obstacles:
                if i[1] >= 0 and i[0] >= 0 and current_pos[0] == i[0]:
                    y_positive.append(i[1])
            
            if len(y_positive) and y >= min(y_positive):
                is_blocked = True


        # if (x, y) in obstacles:
        #     is_blocked = True

    return is_blocked
