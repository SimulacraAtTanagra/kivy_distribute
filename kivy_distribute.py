
#predefine layout options for grid view based on the number of elements
#arange on gridview with maximum of 5 columns and rows
#dynamically distribute existing items

import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from kivy.graphics import Rectangle, Color, InstructionGroup
from kivy.clock import Clock

import numpy as np


def circle_points(r, n):
	circles = []
	for r, n in zip([r], [n]):
		t = np.linspace(0, 2*np.pi, n, endpoint=False)
		x = list(r * np.cos(t))
		y = list(r * np.sin(t))
		circles.extend([i for i in zip(x,y)])
	circles=[(int(circle[0]),int(circle[1])) for circle in circles]
	for ex,circle in enumerate(circles):
		this=[]
		for ix,i in enumerate(circle):
			this.append(int((i+100)/2))
		circles[ex]=tuple(this)
	return(circles)

posdict={2: [(28, 15), (8, 16)],
	3: [(1, 7), (17, 7), (27, 24)],
	4: [(17, 7), (35, 24), (19, 24), (1, 7)],
	5: [(17, 7), (35, 24), (17, 34), (19, 24), (1, 7)],
	6: [(16, 0), (9, 7), (35, 24), (17, 34), (19, 24), (1, 7)],
	7: [(23, 0), (27, 7), (5, 25), (17, 34), (15, 24), (29, 6), (9, 0)],
	8: [(16, 0),  (1, 7),  (20, 15),  (19, 24),  (17, 34),  (35, 24),  (18, 16),  (17, 7)]
	}

class CustomRow(FloatLayout):
	def __init__(self,i):
		self.id=i

class CustomGrid(FloatLayout):
	def __init__(self,num):
		pass
	#for i in range(num):
	def add_child_to_specific(self, row, col, widget):
		self.ids[row].ids[col].add_widget(widget)
	
class MyGrid(FloatLayout):
	def __init__(self,poslist,num,textlist,**kwargs):
	#must take dictionary with lists of positions for each permutation
		super(MyGrid,self).__init__(**kwargs)
		#self.rows=35
		#self.cols=36
		self.post=circle_points(100,num)
		#print(self.post)
		#self.row_force_default=True
		#self.height: self.minimum_height
		for i in range(num):
			print("adding widgets")
			self.add_widget(Cell(i,textlist[i]))
			self.canvas.add(self.children[0].ig)
		Clock.schedule_once(self.set_attributes)

	def set_attributes(self,dt):
		print("attempting to set attributes now")
		for ix,i in enumerate(self.children):
			pair=self.post[ix]
			sizes = Window.size
			first=(sizes[0]/130)*pair[0]+3
			second=(sizes[1]/130)*pair[1]+3
			i.rect.pos = (first,second)
			l = Label(text=texts[ix],
			font_size=10)
			i.add_widget(l)

class Cell(Widget):
	def __init__(self,i,text,**kwargs):
		super(Cell,self).__init__(**kwargs)

		self.ig=InstructionGroup()
		self.rect=Rectangle()
		self.text=text
		self.color = Color(0.2, 0.2, 0.2*i)
		self.ig.add(self.color)
		self.ig.add(self.rect)

class TestApp(App):
	def build(self):
		return MyGrid(posdict[size],size,texts)
		


if __name__ == '__main__':
	size=8
	texts=['this1','that1','thethird','thelast','another one','oh, another one','keep it coming','yeahhhhh']
	TestApp().run()