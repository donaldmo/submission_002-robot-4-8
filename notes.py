import sys


if len(sys.argv) == 1:
    from world.text import world 
    print("Importing text module")

elif len(sys.argv) == 2 and sys.argv[1] == 'turtle':
    from world.turtle import world
    print("Importing turtle module")

else:
    print("Invalid command-line arguments")