from turtle import Turtle
import turtle

class Player(Turtle):
  def __init__(self, map, start_m, start_n, end_m, end_n):
    # 父类初始化
    Turtle.__init__(self)
    #初始的横纵坐标
    self.m = start_m
    self.n = start_n
    #终点的横纵坐标
    self.end_m = end_m
    self.end_n = end_n
    #迷宫地图
    self.map = map
    self.hideturtle()
    self.speed(0)
    self.penup()
    # 玩家移到对应的位置
    self.goto(self.n * 20 - 120, 120 - self.m * 20)
    # 生成玩家
    self.shape('turtle')
    self.color('yellow')
    #玩家初始方向
    self.setheading(270)
    self.showturtle()

#当玩家到达终点时，显示'you win!'
  def reach_exit(self, m, n):
    if m == self.end_m and n == self.end_n:
      # 走出迷宫，显示'you win!'
      text = turtle.Turtle()
      text.hideturtle()
      text.penup()
      text.goto(-125, -10)
      text.color('blue')
      text.write('you win!', font = ('SimHei', 48, 'bold'))

  #定义玩家可移动的位置，即只允许在迷宫内的通道里移动
  def canmove(self, m, n):
    #遇到0允许移动
    return self.map[m][n] == 0

  #玩家移动时位置发生的变化
  def move(self, m, n):
    self.m = m
    self.n = n
    self.goto(self.n * 20 - 120, 120 - self.m * 20)
    self.reach_exit(m, n)

  #向上移动
  def go_up(self):
    if self.canmove(self.m - 1, self.n):
      self.setheading(90)
      self.move(self.m - 1, self.n)

  #向下移动
  def go_down(self):
    if self.canmove(self.m + 1, self.n):
      self.setheading(270)
      self.move(self.m + 1, self.n)

  #向左移动
  def go_left(self):
    if self.canmove(self.m, self.n - 1):
      self.setheading(180)
      self.move(self.m, self.n - 1)

  #向右移动
  def go_right(self):
    if self.canmove(self.m, self.n + 1):
      self.setheading(0)
      self.move(self.m, self.n + 1)