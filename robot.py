"""
TODO: You can either work from this skeleton, or you can build on your solution for Toy Robot 3 exercise.
"""

# list of valid command names
import sys
import world.obstacles as obstacles
from world.use_turtle import draw_obstacles
from world.text import world


my_turtle = None
# my_obstacles = obstacles.get_obstacles()

# my_obstacles.pop()
# my_obstacles.append((0, 70))
my_obstacles = [(0, 70), (70, -10), (10, -70), (-10, 70), (-70, 10)]

if len(sys.argv) == 1:
    from world.text import world

elif len(sys.argv) == 2 and sys.argv[1] == 'turtle':
    from world.turtle import world
    my_turtle = world.use_turtle()
    draw_obstacles(my_obstacles)


valid_commands = ['off', 'help', 'replay', 'forward', 'back', 'right', 'left', 'sprint']
move_commands = valid_commands[3:]
current_direction_index = 0

#commands history
history = []


def get_robot_name():
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name

                                                                                                                    
def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """

    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    while len(command) == 0 or not valid_command(command):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)

    return command.lower()


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """

    (command_name, arg1) = split_command_input(command)

    if command_name.lower() == 'replay':
        if len(arg1.strip()) == 0:
            return True
        elif (arg1.lower().find('silent') > -1 or arg1.lower().find('reversed') > -1) and len(arg1.lower().replace('silent', '').replace('reversed','').strip()) == 0:
            return True
        else:
            range_args = arg1.replace('silent', '').replace('reversed','')
            if is_int(range_args):
                return True
            else:
                range_args = range_args.split('-')
                return is_int(range_args[0]) and is_int(range_args[1]) and len(range_args) == 2
    else:
        return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1))


def output(name, message):
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays all movement commands from history [FORWARD, BACK, RIGHT, LEFT, SPRINT]
"""

# wolrd cut from here


def get_commands_history(reverse, relativeStart, relativeEnd):
    """
    Retrieve the commands from history list, already breaking them up into (command_name, arguments) tuples
    :param reverse: if True, then reverse the list
    :param relativeStart: the start index relative to the end position of command, e.g. -5 means from index len(commands)-5; None means from beginning
    :param relativeEnd: the start index relative to the end position of command, e.g. -1 means from index len(commands)-1; None means to the end
    :return: return list of (command_name, arguments) tuples
    """

    commands_to_replay = [(name, args) for (name, args) in list(map(lambda command: split_command_input(command), history)) if name in move_commands]
    if reverse:
        commands_to_replay.reverse()

    range_start = len(commands_to_replay) + relativeStart if (relativeStart is not None and (len(commands_to_replay) + relativeStart) >= 0) else 0
    range_end = len(commands_to_replay) + relativeEnd if  (relativeEnd is not None and (len(commands_to_replay) + relativeEnd) >= 0 and relativeEnd > relativeStart) else len(commands_to_replay)
    return commands_to_replay[range_start:range_end]


def do_right_turn(robot_name, ):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    global current_direction_index

    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0

    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    global current_direction_index

    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3

    return True, ' > '+robot_name+' turned left.'


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    try:
        if world.update_position(steps, current_direction_index, my_turtle=my_turtle, my_obstacles=my_obstacles):
            
            return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
        else:
            return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'
    except Exception as error:
        return True, error        


def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    if world.update_position(-steps, current_direction_index, my_turtle=my_turtle):
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)


def do_replay(robot_name, arguments):
    """
    Replays historic commands
    :param robot_name:
    :param arguments a string containing arguments for the replay command
    :return: True, output string
    """

    silent = arguments.lower().find('silent') > -1
    reverse = arguments.lower().find('reversed') > -1
    range_args = arguments.lower().replace('silent', '').replace('reversed', '')

    range_start = None
    range_end = None

    if len(range_args.strip()) > 0:
        if is_int(range_args):
            range_start = -int(range_args)
        else:
            range_args = range_args.split('-')
            range_start = -int(range_args[0])
            range_end = -int(range_args[1])

    commands_to_replay = get_commands_history(reverse, range_start, range_end)

    for (command_name, command_arg) in commands_to_replay:
        (do_next, command_output) = call_command(command_name, command_arg, robot_name)
        if not silent:
            print(command_output)

            world.show_position(robot_name)

    return True, ' > '+robot_name+' replayed ' + str(len(commands_to_replay)) + ' commands' + (' in reverse' if reverse else '') + (' silently.' if silent else '.')


def call_command(command_name, command_arg, robot_name):
    do_next = False
    output = None
    
    if command_name == 'help':
        return do_help()
    elif command_name == 'forward':
        return do_forward(robot_name, int(command_arg))
    
    elif command_name == 'back':
        return do_back(robot_name, int(command_arg))
    
    elif command_name == 'right':
        return do_right_turn(robot_name)
    
    elif command_name == 'left':
        return do_left_turn(robot_name)
    
    elif command_name == 'sprint':  
        return do_sprint(robot_name, int(command_arg))
    
    elif command_name == 'replay':
        return do_replay(robot_name, command_arg)
    return False, None


def handle_command(robot_name, command):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """
    (command_name, arg) = split_command_input(command)

    if command_name == 'off':
        return False
    else:
        (do_next, command_output) = call_command(command_name, arg, robot_name)

    print(command_output)

    world.show_position(robot_name)
    add_to_history(command)

    return do_next


def add_to_history(command):
    """
    Adds the command to the history list of commands
    :param command:
    :return:
    """
    history.append(command)


def print_obstacles(obs):
    position_0_15 = []
    position_50_60 = []
    position_n20_n30 = []

    for ob in obs:
        x, y = ob

        if 0 <= x <= 15 and 0 <= y <= 15:
            position_0_15.append(ob[0])
            position_0_15.append(ob[1])

        if 50 <= x <= 60 and 50 <= y <= 60:
            position_50_60.append(ob[0])
            position_50_60.append(ob[1])

        if -30 <= x <= -20 and -30 <= y <= -20:
            position_n20_n30.append(ob[0])
            position_n20_n30.append(ob[1])

#     print('''There are some obstacles:
# - At position 1,1 (to 5,5)''')
    
    # print('''There are some obstacles:
    # - At position 0,15 (to 4,19)
    # - At position 50,60 (to 54,64)
    # - At position -20,-30 (to -16, -26)''')

    # print(f'- At position 0,15 (to {min(position_0_15)},{max(position_0_15)})')
    # print(f'- At position 50,60 (to {min(position_0_15)},{max(position_50_60)})')
    # print(f'- At position -20,-30 (to {min(position_0_15)},{max(position_n20_n30)})')


def robot_start():
    """This is the entry point for starting my robot"""

    global position_x, position_y, current_direction_index, history, my_turtle

    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")
    
    # print('obstacles: ', my_obstacles)
    print_obstacles(my_obstacles)
    print(my_obstacles)

    command = get_command(robot_name)
    while handle_command(robot_name, command):
        command = get_command(robot_name)

    output(robot_name, "Shutting down..")

    my_turtle = None
    current_direction_index = 0
    history = []



if __name__ == "__main__":
    robot_start()
