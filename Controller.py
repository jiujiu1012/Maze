from turtle import Turtle
import turtle
import pygame
from pygame.locals import *
from sys import exit
from random import randint
from GameMap import *
from MazeGenerator import *

class Controller(Turtle):
  def __init__(self, go_up, go_down, go_left, go_right):
    # 父类初始化
    Turtle.__init__(self)
    # 初始值设置
    self.go_up = go_up
    self.go_down = go_down
    self.go_left = go_left
    self.go_right = go_right
    # 绘制控制器
    self.hideturtle()
    self.speed(0)
    self.draw_btn('上', -15, 165)
    self.draw_btn('下', -15, -135)
    self.draw_btn('左', -165, 15)
    self.draw_btn('右', 135, 15)
    # 绑定点击事件
    screen = self.getscreen()
    screen.onclick(self.handlescreenclick)

  #此处与绘制迷宫内一格墙的方法雷同，不做解释
  def draw_btn(self, name, x, y):
    self.penup()
    self.goto(x, y)
    self.begin_fill()
    self.fillcolor('#ffffff')
    for i in range(4):
      self.forward(30)
      self.right(90)
    self.end_fill()
    self.color('#000000')
    self.goto(x + 7, y - 20)
    self.write(name, font = ('SimHei', 12, 'bold'))

  #当点击事件发生时利用abs函数进行比较判断
  def handlescreenclick(self, x, y):
    if y > 0 and abs(x) < y:
      self.go_up()
    if y < 0 and abs(x) < -y:
      self.go_down()
    if x < 0 and abs(y) < -x:
      self.go_left()
    if x > 0 and abs(y) < x:
      self.go_right()