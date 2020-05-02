#setup board
#setup players
#setup AI move algorithm

from scene import *
from random import choice
import sound

class Piece(LabelNode):
	def __init__(self,*args,**kwargs):
		LabelNode.__init__(self,*args,**kwargs)
		
	def is_touched(self,x,y):
		#determine if a piece has been touched
		bound = self.font[1] / 2
		left_bound = self.position.x - bound
		right_bound = self.position.x + bound
		upper_bound = self.position.y + bound
		bottom_bound = self.position.y - bound
		if left_bound <= x and x <= right_bound and bottom_bound <= y and y <= upper_bound:
			return True
		return False

class Board (ShapeNode):
	def __init__(self,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.width = 7
		self.font_family = 'Helvetica'
		self.divs = 4
		self.start_pattern = '*'
		size = self.size.w	
		self.font_size = size/2/self.divs
		#draw lines on board
		for i in range(1,self.divs):
			pos = i*size/self.divs - size/2
			line1 = self.draw_line(0,pos,size,0)
			line2 = self.draw_line(pos,0,0,size)
		#initialize pieces
		self.pieces = [[None for _ in range(self.divs)] for _ in range(self.divs)]
		self.place_pieces()
		
	def draw_line(self,x,y,dx,dy):
		#draw line and return ShapeNode
		line = ui.Path()
		line.line_width = self.width
		line.move_to(0,0)
		line.line_to(dx,dy)
		line.close()
		line_node = ShapeNode(line,stroke_color=self.stroke_color,parent=self,position=(x,y))
		return line_node
		
	def place_pieces(self):
		#update board with current plays
		size = self.size.w
		for j in range(len(self.pieces)):
			for i in range(len(self.pieces)):
				x = 1/self.divs*i*size - size/2 + size/2/self.divs
				y = 1/self.divs*j*size - size/2 + size/2/self.divs
				piece = Piece(self.start_pattern,font=(self.font_family,self.font_size),position=(x,y),parent=self)
				self.pieces[i][j] = piece

class Tic(Scene):
	
	def setup(self):
		#build board
		self.color = 'white'
		self.background_color = '#7052ff'
		margin = 20
		available_size = min(self.size.w,self.size.h)
		size = available_size - 2*margin
		square = ui.Path.rect(0,0,size,size)
		self.board = Board(square,fill_color='clear',stroke_color=self.color,parent=self,position=(self.size.w/2,self.size.h/2))
		#initialize game variables
		self.players = ['X','O']
		self.current_player = choice(self.players)
		self.move_count = self.board.divs**2
		
	def touch_began(self, touch):
		#listen for touch events on pieces
		#if any of the pieces are touched, replace them with a the current piece
		#adjust touch location for new coordinate system
		x = touch.location.x - self.size.w/2
		y = touch.location.y - self.size.h/2
		if self.move_count > 0:
			for div in self.board.pieces:
				for piece in div:
					if piece.is_touched(x,y):
						click = sound.play_effect('ui:click5',pitch=0.5)
						piece.text = self.current_player
						#switch current player
						current_player_index = (self.players.index(self.current_player) + 1) % len(self.players)
						self.current_player = self.players[current_player_index]
						self.move_count -= 1
					
run(Tic())
