import turtle


def draw_obstacles(obstacles: list) -> None:
    obstacles_turtle = turtle.Turtle()
    obstacles_turtle.hideturtle()
    obstacles_turtle.penup()

    for obs_xy in obstacles:
        obstacles_turtle.penup()
        obstacles_turtle.goto(obs_xy)

        obstacles_turtle.pendown()
        
        for i in range(4):
            obstacles_turtle.forward(4)
            obstacles_turtle.right(90)


def use_turtle():
    screen = turtle.getscreen()
    screen.setup(width=480, height=768)

    turtle_robot = turtle.Turtle()
    # turtle_robot.shape('turtle')
    turtle_robot.setheading(90)

    constrained_turtle = turtle.Turtle()
    constrained_turtle.hideturtle()
    constrained_turtle.penup()
    constrained_turtle.setheading(90)
    constrained_turtle.forward(200)
    constrained_turtle.right(90)
    constrained_turtle.forward(100)
    constrained_turtle.pendown()
    constrained_turtle.pencolor('red')
    constrained_turtle.pensize(3)

    for i in range(2):
        constrained_turtle.right(90)
        constrained_turtle.forward(400)
        constrained_turtle.right(90)
        constrained_turtle.forward(200)

    return turtle_robot