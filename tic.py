#setup board
#setup players
#setup AI move algorithm

from scene import *
import sound
from random import choice
import math

class Spot(LabelNode):
	def __init__(self,*args,index=None,**kwargs):
		LabelNode.__init__(self,*args,**kwargs)
		self.i = index[0]
		self.j = index[1]
		self.taken = False
		
	def is_touched(self,x,y):
		#if the spot is not taken, determine if a spot has been touched
		if not self.taken:
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
		#initialize spots and moves
		self.moves = [[self.start_pattern for _ in range(self.divs)] for _ in range(self.divs)]
		self.moves_inv = [[self.start_pattern for _ in range(self.divs)] for _ in range(self.divs)]
		self.spots = []
		self.update()
		
	def draw_line(self,x,y,dx,dy):
		#draw line and return ShapeNode
		line = ui.Path()
		line.line_width = self.width
		line.move_to(0,0)
		line.line_to(dx,dy)
		line.close()
		line_node = ShapeNode(line,stroke_color=self.stroke_color,parent=self,position=(x,y))
		return line_node
		
	def update(self):
		#initialize board if there are no available spots
		#otherwise update the board with the current moves
		if len(self.spots) <= 0:
			size = self.size.w
			for j in range(self.divs):
				for i in range(self.divs):
					x = 1/self.divs*i*size - size/2 + size/2/self.divs
					y = -1/self.divs*j*size + size/2 - size/2/self.divs
					spot = Spot(self.start_pattern,index=(j,i),font=(self.font_family,self.font_size),position=(x,y),parent=self)
					self.spots.append(spot)
		else:
			for spot in self.spots:
				if self.moves[spot.i][spot.j] != spot.text:
					spot.text = self.moves[spot.i][spot.j]
					spot.taken = True

class Tic(Scene):
	
	def setup(self):
		#build board
		self.color = 'white'
		self.background_color = '#7052ff'
		margin = 20
		center = (self.size.w/2,self.size.h/2)
		available_size = min(self.size.w,self.size.h)
		size = available_size - 2*margin
		self.square = ui.Path.rect(0,0,size,size)
		self.board = Board(self.square,fill_color='clear',stroke_color=self.color,parent=self,position=center)
		#initialize game variables
		self.AI_level = 2
		self.players = ['X','O']
		self.player = choice(self.players)
		self.current_player = self.player
		self.game_state = LabelNode("",font=(self.board.font_family,2.25*self.board.font_size),position=center,parent=self)
		
	def touch_began(self, touch):
		#listen for touch events on pieces
		#if any of the pieces are touched, replace them with a the current piece
		#adjust touch location for new coordinate system
		x = touch.location.x - self.size.w/2
		y = touch.location.y - self.size.h/2
		if self.game_state.text == "":
			for spot in self.board.spots:
				if spot.is_touched(x,y):
					click = sound.play_effect('ui:click5',pitch=0.5)
					self.pick((spot.i,spot.j))
					self.board.update()
					result = self.update_state()
					if not result:
						self.take_turn()		
								
	def pick(self,index):
		self.board.moves[index[0]][index[1]] = self.current_player
		self.board.moves_inv[index[1]][index[0]] = self.current_player
		#switch current player
		current_player_index = (self.players.index(self.current_player) + 1) % len(self.players)
		self.current_player = self.players[current_player_index]
		
	def unpick(self,index):
		self.board.moves[index[0]][index[1]] = self.board.start_pattern
		self.board.moves_inv[index[1]][index[0]] = self.board.start_pattern
		#switch current player back
		current_player_index = (self.players.index(self.current_player) + 1) % len(self.players)
		self.current_player = self.players[current_player_index]
		
	def update_state(self):
		result = self.check_winner()
		if result:
			if result != 'TIE':
				self.game_state.text = f'{result} WINS'
			else:
				self.game_state.text = result
		return result
						
	def check_winner(self):
		#check horizontal and vertical
		for div in range(self.board.divs):
			winner = self.board.moves[div][0]
			row = self.board.moves[div]
			if self.all_equal(row) and self.is_valid(winner):
				return winner
			winner = self.board.moves_inv[div][0]
			col = self.board.moves_inv[div]
			if self.all_equal(col) and self.is_valid(winner):
				return winner
				
		#check diagonals
		winner = self.board.moves[0][0]
		diagonal = [self.board.moves[i][i] for i in range(self.board.divs)]
		if self.all_equal(diagonal) and self.is_valid(winner):
			return winner
		winner = self.board.moves[self.board.divs-1][0]
		diagonal = [self.board.moves[self.board.divs-1-i][i] for i in range(self.board.divs)]
		if self.all_equal(diagonal) and self.is_valid(winner):
			return winner
			
		#check if the game is a tie or ongoing
		for div in self.board.moves:
			for move in div:
				if move == self.board.start_pattern:
					return None
		return 'TIE'
		
	def is_valid(self,winner):
		#check if the winner is valid
		return winner != None and winner != self.board.start_pattern
		
	def all_equal(self,list):
		#determine if the elements in the list all have the same value
		value = list[0]
		for i in range(1,len(list)):
			if list[i] != value:
				return False
		return True
		
	def take_turn(self):
		selection = None
		if self.AI_level == 0:
			#skip AI turn
			return
		elif self.AI_level == 1:
			#find random pick
			while selection == None:
				pick = choice(self.board.spots)
				if not pick.taken:
					selection = (pick.i,pick.j)
		else:
			#find best pick
			maxEval = -math.inf
			for i, div in enumerate(self.board.moves):
				for j, move in enumerate(div):
					if move == self.board.start_pattern:
						self.pick((i,j))
						eval = self.minimax()
						self.unpick((i,j))
						if eval > maxEval:
							maxEval = eval
							selection = (i,j)
			
		self.pick(selection)
		self.board.update()
		self.update_state()
			
	def minimax(self,maximizingPlayer=False):
		#base case
		result = self.check_winner()
		if result:
			return self.calc_score(result)
		
		#maximizing players turn
		if maximizingPlayer:
			maxEval = -math.inf
			for i, div in enumerate(self.board.moves):
				for j, move in enumerate(div):
					if move == self.board.start_pattern:
						self.pick((i,j))
						eval = self.minimax(False)
						self.unpick((i,j))
						maxEval = max(maxEval,eval)
			return maxEval
						
		#minimizing players turn
		else:
			minEval = math.inf
			for i, div in enumerate(self.board.moves):
				for j, move in enumerate(div):
					if move == self.board.start_pattern:
						self.pick((i,j))
						eval = self.minimax(True)
						self.unpick((i,j))
						minEval = min(minEval,eval)
			return minEval
		
	def calc_score(self,result):
		if result == self.player:
			return -1
		elif result == 'TIE':
			return 0
		else:
			return 1
					
run(Tic())
