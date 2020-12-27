# 此部分通过pygame进行迷宫展示（相当于一个界面的设计）

import pygame
from pygame.locals import *
from sys import exit
from random import randint
from GameMap import *
from MazeGenerator import *
from AStarSearch import *

# 迷宫以及按钮长宽的定义
REC_SIZE = 10
REC_WIDTH = 51 # 必须为奇数，可以调整迷宫的长宽
REC_HEIGHT = 51 # must be odd number
BUTTON_HEIGHT = 30
BUTTON_WIDTH = 120
SCREEN_WIDTH = REC_WIDTH * REC_SIZE
SCREEN_HEIGHT = REC_HEIGHT * REC_SIZE + BUTTON_HEIGHT

# 对按钮进行背景字体颜色的设计
class Button():
	def __init__(self, screen, type, x, y):
		self.screen = screen
		self.width = BUTTON_WIDTH
		self.height = BUTTON_HEIGHT
		self.button_color = (128,128,128)
		self.text_color = [(255,255,255), (255,0,0)]  # 设置字体颜色，未选中的按钮字体颜色为白色（255，255，255），选中为红色
		self.font = pygame.font.SysFont(None, BUTTON_HEIGHT*2//3)
		
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.topleft = (x, y)
		self.type = type
		self.init_msg()

	# 获取矩形框中的相关参数
	def init_msg(self):
		self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[0], self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	# 利用draw（）方法进行背景填充
	def draw(self):
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)

	# 当点击的时候应该展示的颜色
	def click(self, game):
		game.maze_type = self.type
		self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[1], self.button_color)

	# 不点击时应该展示的颜色
	def unclick(self):
		self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[0], self.button_color)

class Game():
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		self.clock = pygame.time.Clock()
		self.map = Map(REC_WIDTH, REC_HEIGHT)
		self.mode = 0
		self.maze_type = MAZE_GENERATOR_TYPE.RANDOM_PRIM
		self.buttons = []
		self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.RECURSIVE_BACKTRACKER, 0, 0))
		self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.RANDOM_PRIM, BUTTON_WIDTH + 10, 0))
		self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.RECURSIVE_DIVISION, (BUTTON_WIDTH + 10) * 2, 0))
		self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.UNION_FIND_SET, (BUTTON_WIDTH + 10) * 3, 0))
		self.buttons[0].click(self)
# 游戏过程中的界面显示
	def play(self):
		self.clock.tick(30)
		
		pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, SCREEN_WIDTH, BUTTON_HEIGHT))
		for button in self.buttons:
			button.draw()

		for y in range(self.map.height):
			for x in range(self.map.width):
				type = self.map.getType(x, y)
				if type == MAP_ENTRY_TYPE.MAP_EMPTY:
					color = (255, 255, 255)
				elif type == MAP_ENTRY_TYPE.MAP_BLOCK:
					color = (0, 0, 0)
				elif type == MAP_ENTRY_TYPE.MAP_TARGET:
					color = (255, 0, 0)
				else:
					color = (0, 0, 255)
				pygame.draw.rect(self.screen, color, pygame.Rect(REC_SIZE*x, REC_SIZE*y+BUTTON_HEIGHT, REC_SIZE, REC_SIZE))
# 生成，根据mode模式进行判断设置生成迷宫还是设置起始点或者A*寻路
	def generateMaze(self):
		if self.mode >= 4:
			self.mode = 0
		if self.mode == 0:
			generateMap(self.map, self.maze_type)
		elif self.mode == 1:
			self.source = self.map.generatePos((1,1),(1, self.map.height-2))
			self.dest = self.map.generatePos((self.map.width-2, self.map.width-2), (1, self.map.height-2))
			self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_TARGET)
			self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
		elif self.mode == 2:
			AStarSearch(self.map, self.source, self.dest)
			self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_TARGET)
			self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
		else:
			self.map.resetMap(MAP_ENTRY_TYPE.MAP_EMPTY)
		self.mode += 1


# 检测鼠标所点击的按钮位置
def check_buttons(game, mouse_x, mouse_y):
	for button in game.buttons:
		if button.rect.collidepoint(mouse_x, mouse_y):
			button.click(game)
			for tmp in game.buttons:
				if tmp != button:
					tmp.unclick()
			break

# 根据情况对以上方法进行调用
game = Game()
while True:
	game.play()
	pygame.display.update()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			game.generateMaze()
			break
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_buttons(game, mouse_x, mouse_y)
			