import turtle
import os
from playsound import playsound

win = turtle.Screen()
win.title = ("Pong by Brendan.")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

scorea = 0
scoreb = 0

paddlea = turtle.Turtle()
paddlea.speed(0)
paddlea.shape("square")
paddlea.color("white")
paddlea.shapesize(stretch_wid=5, stretch_len=1)
paddlea.penup()
paddlea.goto(-350, 0)

paddleb = turtle.Turtle()
paddleb.speed(0)
paddleb.shape("square")
paddleb.color("white")
paddleb.shapesize(stretch_wid=5, stretch_len=1)
paddleb.penup()
paddleb.goto(+350, 0)

ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1
ball.dy = -1

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0   Player B: 0", align="center", font = ("Courier", 24, "normal"))



def paddlea_up():
    y = paddlea.ycor()
    y += 20
    paddlea.sety(y)

def paddlea_down():
    y = paddlea.ycor()
    y -= 20
    paddlea.sety(y)

def paddleb_up():
    y = paddleb.ycor()
    y += 20
    paddleb.sety(y)

def paddleb_down():
    y = paddleb.ycor()
    y -= 20
    paddleb.sety(y)

win.listen()
win.onkeypress(paddlea_up, "w")
win.onkeypress(paddlea_down, "s")
win.onkeypress(paddleb_up, "Up")
win.onkeypress(paddleb_down, "Down")


while True:
    win.update()
    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)

    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        playsound("Ping Pong/bounce.wav")

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        playsound("Ping Pong/bounce.wav")

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        scorea += 1
        pen.clear()
        pen.write("Player A: {}   Player B: {}".format(scorea, scoreb), align="center", font=("Courier", 24, "normal"))


    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        scoreb += 1
        pen.clear()
        pen.write("Player A: {}   Player B: {}".format(scorea, scoreb), align="center", font=("Courier", 24, "normal"))

    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddleb.ycor() + 40 and ball.ycor() > paddleb.ycor() - 40):
        ball.setx(340)
        ball.dx *= -1
        playsound("Ping Pong/bounce.wav")

    if (ball.xcor() < -340 and ball.xcor() > - 350) and (ball.ycor() < paddlea.ycor() + 40 and ball.ycor() > paddlea.ycor() - 40):
        ball.setx(-340)
        ball.dx *= -1
        playsound("Ping Pong/bounce.wav")
