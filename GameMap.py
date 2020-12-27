# 这部分用来生成展示迷宫

from random import randint   # random（）方法用来随机生成0到1范围内的实数，但是不能进行直接访问，所以导入randint模块
from enum import Enum  # enum模块是系统内置模块，使用import进行导入

class MAP_ENTRY_TYPE(Enum):
	MAP_EMPTY = 0,  # 空标记为0
	MAP_BLOCK = 1,  # 障碍物标记为1
	MAP_TARGET = 2,  # 目标标记为2
	MAP_PATH = 3,    # 可走路径标记为3

class WALL_DIRECTION(Enum):  # 使用枚举标记方向
	WALL_LEFT = 0,
	WALL_UP = 1,
	WALL_RIGHT = 2,
	WALL_DOWN = 3,
	
map_entry_types = {0:MAP_ENTRY_TYPE.MAP_EMPTY, 1:MAP_ENTRY_TYPE.MAP_BLOCK, 2:MAP_ENTRY_TYPE.MAP_TARGET, 3:MAP_ENTRY_TYPE.MAP_PATH}

class Map():
	def __init__(self, width, height): #定义了一个方法传入参数，self代表实例本身
		self.width = width
		self.height = height
		self.map = [[0 for x in range(self.width)] for y in range(self.height)] # 利用range函数来随机生成0到self.width之间的值
	
	def generatePos(self, rangeX, rangeY):
		x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1])) # randint（）用来创建整数列表，从randint(rangeX[0]开始，rangeX[1]结束，默认步长为1
		while self.map[y][x] == 1:
			x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
		return (x , y)
	
	def resetMap(self, value):  # 重新生成地图
		for y in range(self.height):
			for x in range(self.width):
				self.setMap(x, y, value)
	
	def setMap(self, x, y, value): # 设置地图，需要判断此时的位置为通路还是障碍物或者目标等
		if value == MAP_ENTRY_TYPE.MAP_EMPTY:
			self.map[y][x] = 0
		elif value == MAP_ENTRY_TYPE.MAP_BLOCK:
			self.map[y][x] = 1
		elif value == MAP_ENTRY_TYPE.MAP_TARGET:
			self.map[y][x] = 2
		else:
			self.map[y][x] = 3
	
	def isVisited(self, x, y):  #以下方法为判断此时的位置是否已被访问或是否有效是否可移动等，return 1的时候代表满足
		return self.map[y][x] != 1

	def isMovable(self, x, y):
		return self.map[y][x] != 1
	
	def isValid(self, x, y):
		if x < 0 or x >= self.width or y < 0 or y >= self.height:  #边界不能超过获取到的长，宽
			return False
		return True
	
	def getType(self, x, y):  # 获取类型
		return map_entry_types[self.map[y][x]]

	def showMap(self):  #将地图进行展示
		for row in self.map:
			s = ''
			for entry in row:
				if entry == 0:
					s += ' 0'
				elif entry == 1:
					s += ' #'
				else:
					s += ' X'
			print(s)
		