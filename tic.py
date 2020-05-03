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
		self.no_boarder = True
		self.width = 7
		self.font_family = 'Helvetica'
		self.divs = 3
		self.start_pattern = '*'
		size = self.size.w	
		self.font_size = size/2/self.divs
		#draw lines on board
		for i in range(1,self.divs):
			pos = i*size/self.divs - size/2
			line1 = self.draw_line(0,pos,size,0)
			line2 = self.draw_line(pos,0,0,size)
		if self.no_boarder:
			self.stroke_color = 'clear'
		#initialize pieces
		self.pieces = [[None for _ in range(self.divs)] for _ in range(self.divs)]
		self.pieces_inv = [[None for _ in range(self.divs)] for _ in range(self.divs)]
		self.available = []
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
				self.pieces[j][i] = piece
				self.pieces_inv[i][j] = piece
				self.available.append(piece)

class Tic(Scene):
	
	def setup(self):
		#build board
		self.color = 'white'
		self.background_color = '#7052ff'
		margin = 20
		available_size = min(self.size.w,self.size.h)
		size = available_size - 2*margin
		square = ui.Path.rect(0,0,size,size)
		center = (self.size.w/2,self.size.h/2)
		self.board = Board(square,fill_color='clear',stroke_color=self.color,parent=self,position=center)
		#initialize game variables
		self.players = ['X','O']
		self.current_player = choice(self.players)
		self.game_state = LabelNode("",font=(self.board.font_family,2.25*self.board.font_size),position=center,parent=self)
		
	def touch_began(self, touch):
		#listen for touch events on pieces
		#if any of the pieces are touched, replace them with a the current piece
		#adjust touch location for new coordinate system
		x = touch.location.x - self.size.w/2
		y = touch.location.y - self.size.h/2
		if self.game_state.text == "":
			for div in self.board.pieces:
				for piece in div:
					if piece.is_touched(x,y) and piece in self.board.available:
						click = sound.play_effect('ui:click5',pitch=0.5)
						self.pick(piece)
						result = self.check_state()
						if result:
							self.game_state.text = result
						else:
							self.take_turn()		
								
	def pick(self,piece):
		piece.text = self.current_player
		self.board.available.remove(piece)
		#switch current player
		current_player_index = (self.players.index(self.current_player) + 1) % len(self.players)
		self.current_player = self.players[current_player_index]
						
	def check_state(self):
		#check horizontal and vertical
		for div in range(self.board.divs):
			winner = self.board.pieces[div][0]
			row = self.board.pieces[div]
			if self.all_equal(row) and self.is_valid(winner):
				return f'{winner.text} WINS'
			winner = self.board.pieces_inv[div][0]
			col = self.board.pieces_inv[div]
			if self.all_equal(col) and self.is_valid(winner):
				return f'{winner.text} WINS'
				
		#check diagonals
		winner = self.board.pieces[0][0]
		diagonal = [self.board.pieces[i][i] for i in range(self.board.divs)]
		if self.all_equal(diagonal) and self.is_valid(winner):
			return f'{winner.text} WINS'
		winner = self.board.pieces[self.board.divs-1][0]
		diagonal = [self.board.pieces[self.board.divs-1-i][i] for i in range(self.board.divs)]
		if self.all_equal(diagonal) and self.is_valid(winner):
			return f'{winner.text} WINS'
			
		#check for tie
		if len(self.board.available) <= 0:
			return 'TIE'
			
		#else return nothing
		return ''
		
	def is_valid(self,winner):
		#check if the winner is valid
		return winner != None and winner.text != self.board.start_pattern
		
	def all_equal(self,list):
		#determine if the elements in the list all have the same text
		first = list[0]
		for i in range(1,len(list)):
			if list[i].text != first.text:
				return False
		return True
		
	def take_turn(self):
		piece = choice(self.board.available)
		self.pick(piece)
		result = self.check_state()
		if result:
			self.game_state.text = result
					
run(Tic())
