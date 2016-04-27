global sprites
global screen
global bullets
global enemies

class myRect(pygame.Rect)
	attributes of pygame.Rect
	rect
	type

	__init__(left, top, width, height, type)
	
class Castle
	rect 
	state
	explosion
	active
	
	__init__()
	draw() :   draw castle
	rebuild()
	destroy()
	
class Level
	obstacle_rects = []
	mapr
	
	__init__(level)
	hitTile(pos) : xử lí trên dữ liệu khi đạn bắn vào tile
	updateObstacleRects(): obstacle_rects bao gồm những tile bắn được
	
class Tank
	rect
	direction
	health
	paralised
	paused
	shileded
	speed
	max_active_bullets
	level
	state
	
	__init__(level, side)
	rotate(direction)
	
class Enemy(Tank):
	attributes from Tank
	type
	

	__init__(level, type, position)
	
class Player(Tank):
	attributes from Tank
	player_rect : chứa rect mới vừa di chuyển
	
	__init(level, type, position)
	move(direction)
	
	
AttackStategy: 
	while not enemyTanks.empty():
		enemyTank = find the nearest enemy with the castle()
		while not canFire(enemyTank) moveTo(enemyTank)
		fire()

getDistTanks(tank1, tank2): return manhattan distance		
getDistCastle_Tank(tank) : return the manhattan distance
findNearestTarget(list of tanks) : return the nearest tank
moveTo(playerTank, enemyTank): return the direction(1,2,3,4)
canFire(playerTank, enemyTank): return True of False
aStar(playerTank, enemyTank, ...) : return the list path direction(1,2,3,4)
	- define the structure of node
		tank
		dir		
		G
		H
	- create valid child nodes
		makeMoveNode()
	- save the parent
