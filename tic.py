#setup board
#setup players
#setup AI move algorithm

from scene import *

class Board (ShapeNode):
	def __init__(self,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.width = 7
		size = self.size.w
		for i in range(1,3):
			pos = i*size/3 - size/2
			line1 = self.draw_line(0,pos,size,0)
			line2 = self.draw_line(pos,0,0,size)
		
	def draw_line(self,x,y,dx,dy):
		line = ui.Path()
		line.line_width = self.width
		line.move_to(0,0)
		line.line_to(dx,dy)
		line.close()
		line_node = ShapeNode(line,stroke_color=self.stroke_color,parent=self,position=(x,y))
		return line_node

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
		
run(Tic())
