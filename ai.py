import random
import time
import multiprocessing
import math
import pygame
import sys
from Queue import Queue

class Node():
	def __init__(self, top, left, dir, parent):
		self.left = left
		self.top = top
		self.dir = dir
		self.parent = parent				
					
class ai_agent():
	mapinfo = []
	map = []
	checked = []
	
	def __init__(self):
		self.mapinfo = []

	# rect:					[left, top, width, height]
	# rect_type:			0:empty 1:brick 2:steel 3:water 4:grass 5:froze
	# castle_rect:			[12*16, 24*16, 32, 32]
	# mapinfo[0]: 			bullets [rect, direction, speed]]
	# mapinfo[1]: 			enemies [rect, direction, speed, type]]
	# enemy_type:			0:TYPE_BASIC 1:TYPE_FAST 2:TYPE_POWER 3:TYPE_ARMOR
	# mapinfo[2]: 			tile 	[rect, type] (empty don't be stored to mapinfo[2])
	# mapinfo[3]: 			player 	[rect, direction, speed, Is_shielded]]
	# shoot:				0:none 1:shoot
	# move_dir:				0:Up 1:Right 2:Down 3:Left 4:None
	# keep_action:			0:The tank work only when you Update_Strategy. 	1:the tank keep do previous action until new Update_Strategy.

	# def Get_mapInfo:		fetch the map infomation
	# def Update_Strategy	Update your strategy

	
	#  0:bullet   1:enemy    2: tile    3: player
	
	def mapInit(self):
		#Empty board
		for i in range(26):
			self.map.append([])	
			
		for i in range(26):
			for j in range(26):
				self.map[i].append('.')	
	
	#update the current map into 2-dimentional array
	def mapUpdate(self):	
	
		for i in range(26):
			for j in range(26):
				self.map[i][j] = '.'
			
		#Add tiles
		for tile in self.mapinfo[2]:			
			if tile[1] == 1:   #BRICK
				self.map[tile[0][1]/16][tile[0][0]/16] = '#'
			if tile[1] == 4:   #GRASS
				self.map[tile[0][1]/16][tile[0][0]/16] = '.'
			if tile[1] == 2:   #STEEL 
				self.map[tile[0][1]/16][tile[0][0]/16] = '#'
			if tile[1] == 3: 
				self.map[tile[0][1]/16][tile[0][0]/16] = '~'
			
		#Add enemy tanks
		for tank in self.mapinfo[1]:
			self.map[tank[0][1]/16][tank[0][0]/16] = 'e'
			self.map[tank[0][1]/16+1][tank[0][0]/16] = 'e'
			self.map[tank[0][1]/16][tank[0][0]/16+1] = 'e'
			self.map[tank[0][1]/16+1][tank[0][0]/16+1] = 'e'
			
		var = 0
		#Add player tank
		for tank in self.mapinfo[3]:
			self.map[(tank[0][1]+var)/16][(tank[0][0]+var)/16] = 'p'
			self.map[(tank[0][1]+var)/16+1][(tank[0][0]+var)/16] = 'p'
			self.map[(tank[0][1]+var)/16][(tank[0][0]+var)/16+1] = 'p'
			self.map[(tank[0][1]+var)/16+1][(tank[0][0]+var)/16+1] = 'p'
			
		#Add bullets
		for bullet in self.mapinfo[0]:		
			if bullet[0][1]/16 >= 0 and bullet[0][0]/16 >= 0 and bullet[0][1]/16 < 26 and bullet[0][0]/16 < 26:
				self.map[bullet[0][1]/16][bullet[0][0]/16] = 'b'
				
			"""
			if bullet[0][1]/16+1 < 26 and bullet[0][0]/16 >= 0:
				self.map[bullet[0][1]/16+1][bullet[0][0]/16] = 'b'
			if bullet[0][0]/16+1 < 26 and bullet[0][1]/16 >= 0:
				self.map[bullet[0][1]/16][bullet[0][0]/16+1] = 'b'
			if bullet[0][0]/16+1 < 26 and bullet[0][1] < 26:
				self.map[bullet[0][1]/16+1][bullet[0][0]/16+1] = 'b'
			"""
				
	def isThreatened(self, playerNode):
		x = playerNode.top
		y = playerNode.left
		
	
		x = x - 1
		cnt = 3
		while x >= 0 and self.map[x][y] <> '#' and cnt > 0:
			if self.map[x][y] == 'e' or self.map[x][y] == 'b':
				return 0
			x = x - 1
			cnt -= 1
			
		x = playerNode.top
		y = playerNode.left
		y = y + 1
		cnt = 3
		while y < 26 and self.map[x][y] <> '#' and cnt > 0:
			if self.map[x][y] == 'e' or self.map[x][y] == 'b':
				return 1
			y = y + 1
			cnt -= 1
			
		x = playerNode.top
		y = playerNode.left
		x = x + 1
		cnt = 3
		while x < 26 and self.map[x][y] <> '#' and cnt > 0:
			if self.map[x][y] == 'e' or self.map[x][y] == 'b':
				return 2
			x = x + 1
			cnt -= 1
			
		x = playerNode.top
		y = playerNode.left
		y = y - 1
		cnt = 3
		while y >= 0 and self.map[x][y] <> '#' and cnt > 0:
			if self.map[x][y] == 'e' or self.map[x][y] == 'b':
				return 3
			y = y - 1
			cnt -= 1
			
		return 4
		
	#check if the tank can fire in current position
	def canFire(self, playerNode):
		x = playerNode.top
		y = playerNode.left
		
		
		if playerNode.dir == 0:
			x = x - 1
			while x >= 0 and self.map[x][y] <> '#':
				if self.map[x][y] == 'e':
					return True
				x = x - 1
				
		if playerNode.dir == 1:
			y = y + 1
			while y < 26 and self.map[x][y] <> '#':
				if self.map[x][y] == 'e':
					return True
				y = y + 1
				
		if playerNode.dir == 2:
			x = x + 1
			while x < 26 and self.map[x][y] <> '#':
				if self.map[x][y] == 'e':
					return True
				x = x + 1
				
		if playerNode.dir == 3:
			y = y - 1
			while y >= 0 and self.map[x][y] <> '#':
				if self.map[x][y] == 'e':
					return True
				y = y - 1
				
		return False
		
	#change for getting an appropriate strategy
	def isTarget(self, current, goal):
		return current.top == goal.top and current.left == goal.left
	
	#check if node is a valid node
	def isValid(self, node):
		if node.top < 0: 
			return False
		if node.top > 24:
			return False
		if node.left < 0: 
			return False
		if node.left > 24: 
			return False
			
		brick = ['#', '~']
	
		if self.map[node.top][node.left] in brick:
			return False
		if self.map[node.top + 1][node.left] in brick:
			return False
		if self.map[node.top][node.left + 1] in brick:
			return False
		if self.map[node.top + 1][node.left + 1] in brick:
			return False
			
		return True
	
	#return a list of appropriate children nodes
	def children(self, current):
	
		res = []
	
		#move_up
		child = Node(current.top - 1, current.left, 0, current)
		if self.isValid(child): 
			res.append(child)
			
		#move_right
		child = Node(current.top, current.left + 1, 1, current)
		if self.isValid(child): 
			res.append(child)
			
		#move_down
		child = Node(current.top + 1, current.left, 2, current)
		if self.isValid(child): 
			res.append(child)
			
		#move_left
		child = Node(current.top, current.left - 1, 3, current)
		if self.isValid(child): 
			res.append(child)
			
		return res
		
	def BFS_Init(self):
	
		self.checked = []
		for i in range(26):			
			self.checked.append([])	
		
		for i in range(26):
			for j in range(26):
				self.checked[i].append(0)
		
	def BFS(self, start, goal):
		
		q = Queue()
		
		for i in range(26):
			for j in range(26):
				self.checked[i][j] = 0
		
		q.put(start)
		self.checked[start.top][start.left] = 1
		
		while q:
			current = q.get()
			
			#print "current"
			#print current.top
			#print current.left
			#print ""
			
			
			if self.isTarget(current, goal):
				path = []
				while current.parent <> -1:
					path.append(current)
					current = current.parent
				#path.append(current)
				return path
			
			for node in self.children(current):   
				if self.checked[node.top][node.left] == 0:
					self.checked[node.top][node.left] = 1					
					q.put(node)
		raise ValueError("Not found enemy")
		
	def nextPos(self, playerNode):
		if playerNode.dir == 0:
			playerNode.top = (self.mapinfo[3][0][0][1] - 2)/16
			playerNode.left = (self.mapinfo[3][0][0][0])/16
		if playerNode.dir == 1:
			playerNode.top = (self.mapinfo[3][0][0][1])/16
			playerNode.left = (self.mapinfo[3][0][0][0] + 2)/16
		if playerNode.dir == 2:
			playerNode.top = (self.mapinfo[3][0][0][1] + 2)/16
			playerNode.left = (self.mapinfo[3][0][0][0])/16
		if playerNode.dir == 3:
			playerNode.top = (self.mapinfo[3][0][0][1])/16
			playerNode.left = (self.mapinfo[3][0][0][0] - 2)/16
			
		return playerNode
		
		
	def operations (self,p_mapinfo,c_control):	
		sys.stdout = open('output.txt', 'w')
		moveDir = ["Move up", "Move right", "Move down", "Move left", "Standby"]
	
		self.mapInit()
		self.BFS_Init()
		lastMove = 0
		while True:
		#-----your ai operation,This code is a random strategy,please design your ai !!-----------------------			
			self.Get_mapInfo(p_mapinfo)
			
			self.mapUpdate()
			
			#print self.mapinfo[1]
			print self.mapinfo[0]
			"""
			for i in range(26):
				for j in range(26): 
					sys.stdout.write(self.map[i][j])
				print ""
				
			print "++++++++++++++++++++++++++++++++++++"
			"""	
			
			
			
			move_dir = 4
			shoot = 0
			
			if len(self.mapinfo[1]) > 0:
				
				player = Node(self.mapinfo[3][0][0][1]/16, self.mapinfo[3][0][0][0]/16, self.mapinfo[3][0][2], -1)
				enemy = Node(self.mapinfo[1][0][0][1]/16, self.mapinfo[1][0][0][0]/16, self.mapinfo[1][0][2], -1)
				
				#print "enemy"
				#print enemy.top
				#print enemy.left
				#print ""
				
				path = self.BFS(player, enemy)
				
				move_dir = path[-1].dir				
				#sys.stdout.write("(%d, %d, %d)" % (path[-1].top, path[-1].left, path[-1].dir))
				#print "Movedir %d" % move_dir
				
				px = (self.mapinfo[3][0][0][1])/16
				py = (self.mapinfo[3][0][0][0])/16
				XTop, XLeft = self.mapinfo[3][0][0][1], self.mapinfo[3][0][0][0]
				bounderTop = px*16
				bounderLeft = py*16
				
				currentDir = self.mapinfo[3][0][1]
				
				#LEFT OR RIGHT
				if (currentDir == 1 or currentDir == 3):
					if (XTop - bounderTop > 3):
						move_dir = 0
						
				#UP OR DOWN
				if (currentDir == 0 or currentDir == 2):
					if (XLeft - bounderLeft > 3):
						move_dir = 3
				"""
				#TURN LEFT OR RIGHT
				if (move_dir == 1 or move_dir == 3) and (lastMove == 0 or lastMove == 2) : 
					var = self.mapinfo[3][0][0][1] % 2
					var = 1
					print "top: %d var: %d " % (self.mapinfo[3][0][0][1], var)
					#print var
					if (self.mapinfo[3][0][0][1] - var)%16 <> 0:											
						move_dir = lastMove						
				#TURN UP OR DOWN
				elif (move_dir == 0 or move_dir == 2) and (lastMove == 1 or lastMove == 3) : 
					var = self.mapinfo[3][0][0][0] % 2
					var = 1
					print "left: %d var: %d " % (self.mapinfo[3][0][0][0], var)
					#print var
					if (self.mapinfo[3][0][0][0] - var)%16 <> 0:											
						move_dir = lastMove
					
				"""	
				
				for i in range(26):
					for j in range(26): 
						sys.stdout.write(self.map[i][j])
					print ""
				
				print "++++++++++++++++++++++++++++++++++++"
				"""
				print "path"
				#path = path[::-1]
				
				while path:
					tmp = path.pop()
					sys.stdout.write("(%d, %d, %d)" % (tmp.top, tmp.left, tmp.dir))
					
				print "endpath"
				
				"""
				
				player.dir = move_dir
				if self.canFire(player):	
					shoot = 1
					print "Enemy found"
				else: 
					shoot = 0	
					
				player = self.nextPos(player)
				tmp = self.isThreatened(player)
				if tmp <> 4:
					move_dir = 4
					shoot = 1
				
			#lastMove = move_dir
			#print move_dir
				
			print moveDir[move_dir]			
			#print lastMove
			
			
			
			#keep_action = 0
			keep_action = 0
			#-----------
			self.Update_Strategy(c_control,shoot,move_dir,keep_action)
		#------------------------------------------------------------------------------------------------------

	def Get_mapInfo(self,p_mapinfo):
		if p_mapinfo.empty()!=True:
			try:
				self.mapinfo = p_mapinfo.get(False)
			except Queue.Empty:
				skip_this=True

	def Update_Strategy(self,c_control,shoot,move_dir,keep_action):
		if c_control.empty() ==True:
			c_control.put([shoot,move_dir,keep_action])
			return True
		else:
			return False

