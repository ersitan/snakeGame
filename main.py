from parts import Snake, screen


snake = Snake()

while not snake.is_crashed():
    screen.onkey(key="Left", fun=snake.turn_left)
    screen.onkey(key="Right", fun=snake.turn_right)
    snake.move_snake()
    snake.check_walls()
    snake.is_food_eaten()
    screen.update()

screen.exitonclick()
