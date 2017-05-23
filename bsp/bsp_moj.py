# -*- coding: UTF-8 -*-

import random
import time
from itertools import chain

class leaf():

	MIN_LEAF_SIZE = 80
	MAX_DEPTH = 5
	def __init__(self, origin, width, height, depth = 1):
		self.x, self.y = origin
		self.height = height
		self.width = width
		self.l = None
		self.r = None
		self.depth = depth
		self.room  = room((self.x, self.y), self.width, self.height)
		self.split_orientation = None #0 for vertical, 1 for horizontal split, None for not split
	
	def __iter__(self):
		if self.l:
			yield from self.l
		yield self
		if self.r:
			yield from self.r
		#yield from self.leaves()
	
	def split(self):
		#split the leaf in two, unless the size of the leaf is too small
		h_less = self.height <= self.MIN_LEAF_SIZE
		w_less = self.width <= self.MIN_LEAF_SIZE
		if  h_less and w_less:
			return
		elif w_less:
			self.split_h()
		elif h_less:
			self.split_v()
		elif random.choice((0,1)) == 0:
			self.split_v()
		else: 
			self.split_h()
		return
	
	def split_v(self):
		#spliting vertically, on x-axis
		if self.depth > self.MAX_DEPTH:
			return
		
		movx = int(random.uniform(0.45*self.width, 0.55*self.width))
		if self.width-movx < self.MIN_LEAF_SIZE:
			return
			
		self.split_orientation = 0	
		self.l = leaf((self.x, self.y), movx, self.height, self.depth+1)
		self.r = leaf((self.x+movx, self.y), self.width-movx, self.height, self.depth+1)
		self.l.split()
		self.r.split()
		#print("uspesno deljenje vertikalno")
	
	def split_h(self):
		#splitting horizontally, on y-axis. L is above, R is below.
		if self.depth > self.MAX_DEPTH:
			return
		
		movy = int(random.uniform(0.45*self.height, 0.55*self.height))
		if self.height-movy < self.MIN_LEAF_SIZE:
			return
			
		self.split_orientation = 1
		self.l = leaf((self.x, self.y), self.width, movy, self.depth+1)
		self.r = leaf((self.x, self.y+movy), self.width, self.height-movy, self.depth+1)
		self.l.split()
		self.r.split()
		#print("uspesno deljenje horizontalno")
	
	def packit(self):
		#packs the leaf data
		return (self.x, self.y, self.width, self.height)
		
	def leaves(self):
		#returns the leaf rooms in order
		if self.l is None and self.r is None:
			return [self.packit()]
		elif self.l is None:
			return self.r.leaves()
		elif self.r is None:
			return self.l.leaves()
		else:
			return self.l.leaves() + self.r.leaves()

class room:
	#generates a room inside a leaf
	MIN_ROOM_SIZE = 40
	def __init__(self, origin, width, height):
		self.x, self.y = origin
		self.width = width
		self.height = height
		
		#move the origin
		movx = int(random.triangular(1, 0.4*self.width, 0.05*self.width))
		movy = int(random.triangular(1, 0.4*self.height, 0.05*self.height))
		self.x += movx
		self.y += movy
		
		#reduce size
		#movwidth = int(random.uniform(movx, self.width-movx))
		#movheight = int(random.uniform(movy, self.height-movy))
		movwidth = int(random.triangular(movx, self.width-movx, 
										movx+0.05*(self.width-movx)))
		movheight = int(random.triangular(movy, self.height-movy, 
										movy+0.05*(self.height-movy)))
		self.width -= movwidth
		self.height -=  movheight
		
		if self.width < self.MIN_ROOM_SIZE:
			self.width = self.MIN_ROOM_SIZE
		if self.height < self.MIN_ROOM_SIZE:
			self.height = self.MIN_ROOM_SIZE
		
	
	def packit(self):
		#packs the room data
		return (self.x, self.y, self.width, self.height)
		
		
class dungeon:
	def __init__(self, width, height, seed=None):
		if seed is None:
			self.seed = int(round(time.time()))
		else:
			self.seed = None
		random.seed(self.seed)
		self.tree = leaf((0,0), width, height)
		#print("Uspesna init")
		#self.tree.MIN_LEAF_SIZE = width/
		self.tree.split()
	
	def __iter__(self):
		i = self.tree.__iter__()
		return i
		