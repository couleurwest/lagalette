import threading
from turtle import Screen, Turtle


def loop1_10():
    screen = Screen()
    turtle = Turtle()
    turtle.hideturtle()
    turtle.speed(0)
    screen.mainloop()


threading.Thread(target=loop1_10).start()
