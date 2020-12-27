# 这部分A*算法自动寻路

from random import randint
from GameMap import *

# 使用F=G+H来预估下一步应该怎么走，H表示待检测结点到目标节点B的估计移动开销，G代表的是从初始位置Start沿着已生成的路径到指定待检测节点的移动开销，
# 估价函数F为他们的取值求和，选择F值最小的节点确定为要移动的节点（当F值相同时我们可以选择跟着open列表中最近添加的方块走）。寻路过程中将待检测节点放
# 入open list，已检测过的节点放入close list。最终close列表中存放的就是最短路径。
class SearchEntry():
	def __init__(self, x, y, g_cost, f_cost=0, pre_entry=None):
		self.x = x
		self.y = y
		# cost move form start entry to this entry
		self.g_cost = g_cost
		self.f_cost = f_cost
		self.pre_entry = pre_entry
	# 获取当前位置
	def getPos(self):
		return (self.x, self.y)


def AStarSearch(map, source, dest):
	def getNewPosition(map, locatioin, offset):
		x,y = (location.x + offset[0], location.y + offset[1])
		# 如果此节点无效或不可移动的点返回none
		if not map.isValid(x, y) or not map.isMovable(x, y):
			return None
		return (x, y)

		# 获取可移动的节点
	def getPositions(map, location):
		# use four ways to move，分别代表上下左右
		offsets = [(-1,0), (0, -1), (1, 0), (0, 1)]
		#offsets = [(-1,0), (0, -1), (1, 0), (0, 1), (-1,-1), (1, -1), (-1, 1), (1, 1)]
		poslist = []
		for offset in offsets:
			pos = getNewPosition(map, location, offset)
			if pos is not None:			
				poslist.append(pos)
		return poslist
	
	# 计算曼哈顿距离
	def calHeuristic(pos, dest):
		return abs(dest.x - pos[0]) + abs(dest.y - pos[1])

	# 计算消耗
	def getMoveCost(location, pos):
		if location.x != pos[0] and location.y != pos[1]:
			return 1.4
		else:
			return 1

	# 判断节点是否在open集或close集中
	def isInList(list, pos):
		if pos in list:
			return list[pos]
		return None
	
	# 添加节点的邻节点
	def addAdjacentPositions(map, location, dest, openlist, closedlist):
		poslist = getPositions(map, location)
		for pos in poslist:
			# 如果该节点已经在close列表中，什么都不做
			if isInList(closedlist, pos) is None:
				findEntry = isInList(openlist, pos)
				h_cost = calHeuristic(pos, dest)
				g_cost = location.g_cost + getMoveCost(location, pos)
				if findEntry is None :
					# 如果该节点不在open表中，将它添加到open表
					openlist[pos] = SearchEntry(pos[0], pos[1], g_cost, g_cost+h_cost, location)
				elif findEntry.g_cost > g_cost:
					# 如果此位置在open表中并且代价大于当前位置，那么更新代价和以前的节点位置
					findEntry.g_cost = g_cost
					findEntry.f_cost = g_cost + h_cost
					findEntry.pre_entry = location
	
	# 寻找open表中代价最小的节点，如果open表为空返回none
	def getFastPosition(openlist):
		fast = None
		for entry in openlist.values():
			if fast is None:
				fast = entry
			elif fast.f_cost > entry.f_cost:
				fast = entry
		return fast

	openlist = {}
	closedlist = {}
	location = SearchEntry(source[0], source[1], 0.0)
	dest = SearchEntry(dest[0], dest[1], 0.0)
	openlist[source] = location
	while True:
		location = getFastPosition(openlist)
		if location is None:
			# 没有找到有效路径
			print("can't find valid path")
			break;
		
		if location.x == dest.x and location.y == dest.y:
			break
		
		closedlist[location.getPos()] = location
		openlist.pop(location.getPos())
		addAdjacentPositions(map, location, dest, openlist, closedlist)
		
	# 在地图中标记找到的路径
	while location is not None:
		map.setMap(location.x, location.y, MAP_ENTRY_TYPE.MAP_PATH)
		location = location.pre_entry	
# 调用相关函数进行运行
def run():
	WIDTH = 10
	HEIGHT = 10
	BLOCK_NUM = 15
	map = Map(WIDTH, HEIGHT)
	map.createBlock(BLOCK_NUM)
	map.showMap()

	source = map.generatePos((0,WIDTH//3),(0,HEIGHT//3))
	dest = map.generatePos((WIDTH//2,WIDTH-1),(HEIGHT//2,HEIGHT-1))
	print("source:", source)
	print("dest:", dest)
	AStarSearch(map, source, dest)
	map.showMap()

if __name__ == "__main__":
	run()


