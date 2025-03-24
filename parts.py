import random
import time
from turtle import Turtle, Screen

screen = Screen()
screen.bgcolor("black")
screen.setup(800, 600)
screen.title("Snake Game")
screen.tracer(0)
screen.listen()


class Food:
    def __init__(self):
        self.food = Turtle("circle")
        self.food.color("blue")
        self.food.teleport(
            x=random.randrange(int(-screen.window_width() / 2) + 20, int(screen.window_width() / 2) - 20, 20),
            y=random.randrange(int(-screen.window_height() / 2) + 20, int(screen.window_height() / 2) - 20, 20))

    def get_food_position(self):
        return round(self.food.xcor()), round(self.food.ycor())

    def delete_old_food(self):
        self.food.hideturtle()
        self.food.clear()


class Snake:
    def __init__(self):
        self.parts = []
        self.length = 3
        self.init_snake()
        self.head = self.parts[0].get_part()
        self.should_move = True
        self.food = Food()
        self.score = Parts(x_pos=300, y_pos=280)
        self.score.get_part().hideturtle()
        self.update_score()

    def update_score(self):
        self.score.get_part().clear()
        self.score.get_part().write(f"Score: {self.length - 3}")

    def create_food(self):
        self.food.delete_old_food()
        self.food = Food()
        if self.food.get_food_position() in [(x.get_part().xcor(), x.get_part().ycor()) for x in self.parts]:
            self.create_food()

    def is_food_eaten(self):
        x_pos, y_pos = self.head.xcor(), self.head.ycor()
        food_pos = self.food.get_food_position()
        if food_pos == (round(x_pos), round(y_pos)):
            self.create_food()
            self.length += 1
            snake_segment = Parts(self.parts[-1].get_part().xcor(), self.parts[-1].get_part().ycor())
            color = "lime" if self.length % 3 else "green"
            snake_segment.get_part().color(color)
            self.parts.append(snake_segment)
            self.update_score()

    def init_snake(self):
        x, y = 0, 0
        for _ in range(self.length):
            part = Parts(x, y)
            part.get_part().color("green")
            self.parts.append(part)
            x -= 20

    def move_snake(self):
        for i in range(len(self.parts) - 1):
            self.parts[len(self.parts) - 1 - i].get_part().goto(self.parts[len(self.parts) - i - 2].get_part().xcor(),
                                                                self.parts[len(self.parts) - i - 2].get_part().ycor())

        self.head.forward(20)

        time.sleep(.1)

    def turn_left(self):
        self.head.setheading(self.head.heading() + 90)

    def turn_right(self):
        self.head.setheading(self.head.heading() - 90)

    def is_crashed(self):
        hit_self = len([x for x in self.parts[1:] if (round(x.get_part().xcor()), round(x.get_part().ycor())) == (
            round(self.head.xcor()), round(self.head.ycor()))]) > 0

        hit_walls = self.head.xcor() < - screen.window_width() / 2 + 20 or self.parts[
            0].get_part().xcor() > screen.window_width() / 2 - 20 or self.parts[
                        0].get_part().ycor() < - screen.window_height() / 2 + 20 or self.parts[
                        0].get_part().ycor() > screen.window_height() / 2 - 20
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


class Parts:
    def __init__(self, x_pos=0, y_pos=0):
        self.part = Turtle("square")
        self.part.color("white")
        self.part.speed("slowest")
        self.part.penup()
        self.part.setx(x_pos)
        self.part.sety(y_pos)

    def get_part(self):
        return self.part
