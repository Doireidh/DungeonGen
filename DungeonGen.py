# -*- coding: UTF-8 -*-

import sys, pygame, random, noise, os
from bsp.bsp_moj import dungeon, leaf 
from pygame.locals import *
from itertools import cycle

clear = lambda: os.system('cls')

#colors
WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)
YELLOW = pygame.Color(255,255,0)
RED = pygame.Color(255,0,0)
ROOM_COL = WHITE
CORR_COL = WHITE

def generate_dungeon():
	seed = None
	dung = dungeon(WIDTH, HEIGHT, seed)

	for x in dung:
		print(" "*x.depth + str(x.room.packit()))
		if x.l is None and x.r is None:
			#leaf
			nROOM_COL = ROOM_COL #// pygame.Color(x.depth,x.depth,x.depth,0)
			pygame.draw.rect(surface, nROOM_COL, x.room.packit())
			#pygame.draw.rect(surface, RED, x.packit(), 2)
		else:
			#this is a branch, connect leaves
			#pygame.draw.rect(surface, RED, x.room.packit(), 1)
			pass
	connect_rooms(dung.tree)
	connect_secret_rooms(dung.tree.l, dung.tree.r, dung.tree.split_orientation)
	return dung
			
def connect_rooms(node):
	left = node.l
	right = node.r
	CORR_WIDTH = 10
	
	if left.l is not None:
		connect_rooms(left)
	if right.l is not None:
		connect_rooms(right)
	
	px, py, kx, ky, pos = draw_corr(left, right, CORR_WIDTH)
	
	#korekcija nevidljive sobe za grane
	if pos == 0:
		node.room.x = int(px)
		node.room.y = int(ky)
	else:
		node.room.x = int(kx)
		node.room.y = int(py)
	node.room.width = 0
	node.room.height = 0

def draw_corr(left, right, CORR_WIDTH = 10, nCORR_COL = CORR_COL):
	px = left.room.x + left.room.width/2
	py = left.room.y + left.room.height/2
	kx = right.room.x + right.room.width/2
	ky = right.room.y + right.room.height/2
	
	code = determine_pos((left.room.x+left.room.width/2
							, left.room.y+left.room.height/2),
						(right.room.x+right.room.width/2,
							right.room.y+right.room.height/2))
	
	print(" "*(left.depth-1) + str(left.room.packit()))
	print(" "*(right.depth-1) + str(right.room.packit()))
	
	pos = random.choice((0,1))
	
	#nCORR_COL = CORR_COL #// pygame.Color(left.depth,left.depth,left.depth,0)
	
	if code == 10: 
		#bottom right
		if pos == 0:
			#down, then right
			pygame.draw.rect(surface, nCORR_COL, (px, py, CORR_WIDTH, ky-py+CORR_WIDTH))
			pygame.draw.rect(surface, nCORR_COL, (px, ky, kx-px+CORR_WIDTH, CORR_WIDTH))
		else:
			#right, then down
			pygame.draw.rect(surface, nCORR_COL, (px, py, kx-px+CORR_WIDTH, CORR_WIDTH))
			pygame.draw.rect(surface, nCORR_COL, (kx, py, CORR_WIDTH, ky-py+CORR_WIDTH))
	elif code == 9:
		#top right
		if pos == 0:
			pygame.draw.rect(surface, nCORR_COL, (px, py, CORR_WIDTH, ky-py+CORR_WIDTH))
			pygame.draw.rect(surface, nCORR_COL, (px, ky, kx-px+CORR_WIDTH, CORR_WIDTH))
		else:
			pygame.draw.rect(surface, nCORR_COL, (px, py, kx-px+CORR_WIDTH, CORR_WIDTH))
			pygame.draw.rect(surface, nCORR_COL, (kx, py, CORR_WIDTH, ky-py+CORR_WIDTH))
	elif code == 6:
		#bottom left
		if pos == 0:
			pygame.draw.rect(surface, nCORR_COL, (px, py, CORR_WIDTH, ky-py+CORR_WIDTH))
			pygame.draw.rect(surface, nCORR_COL, (px, ky, kx-px+CORR_WIDTH, CORR_WIDTH))
			#pygame.draw.rect(surface, CORR_COL, (px, ky, CORR_WIDTH, CORR_WIDTH))
		else:
			pygame.draw.rect(surface, nCORR_COL, (px, py, kx-px+CORR_WIDTH, CORR_WIDTH))
			pygame.draw.rect(surface, nCORR_COL, (kx, py, CORR_WIDTH, ky-py+CORR_WIDTH))
	return px, py, kx, ky, pos
	
def determine_pos(a, b):
	ax,ay = a
	bx,by = b
	#using a modification of Cohen-Sutherland clipping algorithm
	code = 0	#0000
	top = 1		#0001
	bottom = 2	#0010
	left = 4	#0100
	right = 8	#1000
	
	if ax >= bx:
		code = code | left
	else:
		code = code | right
	
	if ay >= by:
		code = code | top
	else:
		code = code | bottom
	print("kod je", code)
	return code
	
def connect_secret_rooms(left, right, split_orientation):
	SEC_CORR_WIDTH = 10
	SEC_CORR_COL = CORR_COL
	
	#split_orientation is 0 if vertical, 1 if horizontal
	l_list = find_left_candidates(left, split_orientation)
	r_list = find_right_candidates(right, split_orientation)
		
	halfl = int(len(l_list)/2)
	halfr = int(len(r_list)/2)
	
	# for l_list[1,2,3,4] and r_list[1,2,3,4,5,6,7,8,9]
	# result is [(1,1), (2,2), (4,9), (3,8)]. The order is not important, grouping is.
	cand_list = list(zip(l_list[:halfl], r_list[:halfr]))
	cand_list.extend(zip(reversed(l_list[halfl:]), reversed(r_list[halfr:])))
	for room1, room2 in cand_list:
		if random.randint(0,100) < 75:
			draw_corr(room1, room2, SEC_CORR_WIDTH, SEC_CORR_COL)
		else:
			#draw_corr(room1, room2, SEC_CORR_WIDTH, GREEN)
			pass
		
def find_left_candidates(left, so):
	cand_list = []
	if left.l is None:
		if left.depth > 2:
			cand_list.append(left)
	elif left.split_orientation == 1:
		if so == 1:
			cand_list.extend(find_left_candidates(left.r, 1))
		else:
			cand_list.extend(find_left_candidates(left.l, 0))
			cand_list.extend(find_left_candidates(left.r, 0))
	else:
		if so == 1:
			cand_list.extend(find_left_candidates(left.l, 1))
			cand_list.extend(find_left_candidates(left.r, 1))
		else:
			cand_list.extend(find_left_candidates(left.r, 0))
	return cand_list
	
def find_right_candidates(right, so):
	cand_list = []
	if right.l is None:
		if right.depth > 2:
			cand_list.append(right)
	elif right.split_orientation == 1:
		if so == 1:
			cand_list.extend(find_right_candidates(right.l, 1))
		else:
			cand_list.extend(find_right_candidates(right.l, 0))
			cand_list.extend(find_right_candidates(right.r, 0))
	else:
		if so == 1:
			cand_list.extend(find_right_candidates(right.l, 1))
			cand_list.extend(find_right_candidates(right.r, 1))
		else:
			cand_list.extend(find_right_candidates(right.l, 0))
	return cand_list

pygame.init()

#font initialization for mouse coords
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)

WIDTH = 800
HEIGHT = 600
surface = pygame.display.set_mode((WIDTH, HEIGHT), 0)
pygame.display.set_caption('Pygame dungeon generator!')


#draw edges
surface.fill(BLACK)

#function defined above
dung = generate_dungeon()
seedsurf = myfont.render(str(dung.seed), False, RED, BLACK)
surface.blit(seedsurf, (0, HEIGHT-20))

while True:
	#mouse coords
	textsurface = myfont.render(str(pygame.mouse.get_pos()), False, RED, BLACK)
	surface.blit(textsurface, (0,0))
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP_ENTER:
				clear()
				surface.fill(BLACK)
				dung = generate_dungeon()
				seedsurf = myfont.render(str(dung.seed), False, RED, BLACK)
				surface.blit(seedsurf, (0, HEIGHT-20))
			elif event.key == pygame.K_F12:
				with open("screenshot_count.txt", "r+") as f:
					num = f.read()
					pygame.image.save(surface, "screenshots/{}.png".format(num))
					print("screenshot saved to screenshot/{}.png".format(num))
					nnum = int(num)+1
					f.seek(0)
					f.write(str(nnum))
				f.closed
			elif event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit(0)
	pygame.display.update()
            