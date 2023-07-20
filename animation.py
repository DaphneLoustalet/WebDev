# Animations for pending user (like Duo)
from turtle import *
import turtle as tur

for color in ('red', 'orange', 'yellow', 'green', 'blue', 'purple'):
    tur.speed(10)
    for i in range(1):
        tur.color(color)
        tur.begin_fill()
        tur.circle(100)
        tur.end_fill()
    tur.hideturtle()
