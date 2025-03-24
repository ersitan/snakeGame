import random
import time
from turtle import Turtle, Screen

screen = Screen()
screen.bgcolor("black")
screen.setup(800, 600)
screen.title("Snake Game")
screen.tracer(0)
screen.listen()


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("blue")
        self.teleport(x=random.randrange(int(-screen.window_width() / 2) + 20, int(screen.window_width() / 2) - 20, 20),
            y=random.randrange(int(-screen.window_height() / 2) + 20, int(screen.window_height() / 2) - 20, 20))

    def get_food_position(self):
        return round(self.xcor()), round(self.ycor())

    def delete_old_food(self):
        self.hideturtle()
        self.clear()


class Snake:
    def __init__(self):
        self.parts = []
        self.length = 3
        self.init_snake()
        self.head = self.parts[0]
        self.should_move = True
        self.food = Food()
        self.score = Parts(x_pos=300, y_pos=280)
        self.score.hideturtle()
        self.update_score()

    def init_snake(self):
        x, y = 0, 0
        for _ in range(self.length):
            part = Parts(x, y)
            part.color("green")
            self.parts.append(part)
            x -= 20

    def update_score(self):
        self.score.clear()
        self.score.write(f"Score: {self.length - 3}")

    def create_food(self):
        self.food.delete_old_food()
        self.food = Food()
        if self.food.get_food_position() in [(x.xcor(), x.ycor()) for x in self.parts]:
            self.create_food()

    def is_food_eaten(self):
        x_pos, y_pos = self.head.xcor(), self.head.ycor()
        food_pos = self.food.get_food_position()
        if food_pos == (round(x_pos), round(y_pos)):
            self.create_food()
            self.length += 1
            snake_segment = Parts(self.parts[-1].xcor(), self.parts[-1].ycor())
            color = "lime" if self.length % 3 else "green"
            snake_segment.color(color)
            self.parts.append(snake_segment)
            self.update_score()

    def move_snake(self):
        for i in range(len(self.parts) - 1):
            self.parts[len(self.parts) - 1 - i].goto(self.parts[len(self.parts) - i - 2].xcor(),
                                                                self.parts[len(self.parts) - i - 2].ycor())

        self.head.forward(20)

        time.sleep(.1)

    def turn_left(self):
        self.head.setheading(self.head.heading() + 90)

    def turn_right(self):
        self.head.setheading(self.head.heading() - 90)

    def is_crashed(self):
        hit_self = len([x for x in self.parts[1:] if (round(x.xcor()), round(x.ycor())) == (
            round(self.head.xcor()), round(self.head.ycor()))]) > 0

        hit_walls = self.head.xcor() < - screen.window_width() / 2 + 20 or self.parts[
            0].xcor() > screen.window_width() / 2 - 20 or self.parts[
                        0].ycor() < - screen.window_height() / 2 + 20 or self.parts[
                        0].ycor() > screen.window_height() / 2 - 20
        return hit_self

    def check_walls(self):
        if self.head.xcor() < - screen.window_width() / 2:
            self.head.setx(screen.window_width() / 2)
        elif self.head.xcor() > screen.window_width() / 2:
            self.head.setx(-screen.window_width() / 2)
        elif self.head.ycor() > screen.window_height() / 2:
            self.head.sety(-screen.window_height() / 2)
        elif self.head.ycor() < - screen.window_height() / 2:
            self.head.sety(screen.window_height() / 2)


class Parts(Turtle):
    def __init__(self, x_pos=0, y_pos=0):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.speed("slowest")
        self.penup()
        self.setx(x_pos)
        self.sety(y_pos)
