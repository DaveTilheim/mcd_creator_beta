from izi_pygame import *
import os
from math import cos
from math import sin
from random import randint
from random import seed

FILL = 2


window = Window(wtitle="MCD", wwidth=1400, wheight=800)
entity_font = Fontstring(size=20, bold=1, window=window.get_canva())
property_font = Fontstring(size=20, window=window.get_canva())
cardinalite_font = Fontstring(size=20, bold=True, window=window.get_canva())
id_font = Fontstring(size=20, window=window.get_canva(), underline=True)
cursor = Block(width=1, height=1)


class HeadEntity(Drawblock):
	number = 0
	def __init__(self, window, name="ENTITY", x=0, y=0, text_list=None):
		seed(10)
		self.name = name.upper()+str(HeadEntity.number+1)
		Drawblock.__init__(self, x=x, y=y, color=(100,100,100), fill=FILL, window=window, speed=1)
		self.print_name = Printstring(main_font=entity_font, string=self.name, color=(0,0,0), x=self.xbegin, y=self.ybegin)
		self.set_dimension(self.print_name.string.get_width(), self.print_name.string.get_height())
		HeadEntity.number+=1
		text_list.append(self.print_name)
		
	
	def set_position(self, x, y):
		Drawblock.set_position(self, x, y)
		self.print_name.x = self.xbegin
		self.print_name.y = self.ybegin

	def print(self):
		self.draw()
		self.print_name.write()

	def __str__(self):
		return f"{self.xbegin} {self.ybegin} {self.width} {self.height}\n"


class FootEntity(Drawblock):

	def __init__(self, window, x, y, width, height, head, text_list):
		Drawblock.__init__(self, x=x, y=y, width=width, height=height, color=(100,100,100), fill=FILL, window=window, speed=1)
		self.idEntity = Printstring(main_font=id_font, string="id"+head.print_name.get_text().lower(), color=(0,0,150), 
			x=head.print_name.x+FILL, y=head.yend+FILL)
		text_list.append(self.idEntity)
		self.property = list()
		head.set_dimension(height=head.height)
		self.set_dimension(height=self.height+FILL*3)
		

	def add_property(self, head, text_list):
		self.property.append(Printstring(main_font=property_font, string=f"property{len(self.property)+1}", 
			color=(0,0,0), x=head.print_name.x+FILL, y=head.yend+(len(self.property)+1)*head.print_name.string.get_height()))
		text_list.append(self.property[len(self.property)-1])
		self.set_dimension(self.width, (len(self.property)+1)*head.print_name.string.get_height())

	def set_position(self, x, y):
		Drawblock.set_position(self, x, y)
		i = 1
		self.idEntity.x = self.xbegin+FILL
		self.idEntity.y = self.ybegin
		for p in self.property:
			p.x = self.xbegin+FILL
			p.y = self.ybegin+i*p.string.get_height()
			i+=1

	def print(self):
		self.draw()

		self.idEntity.write()
		for p in self.property:
			p.write()

	def __str__(self):
		info = f"{self.xbegin} {self.ybegin} {self.width} {self.height}\n"
		return info

class FocusEntity(Drawblock):

	def __init__(self,  window, x, y, width=10, height=10, focus=0):
		Drawblock.__init__(self, x=x, y=y, width=width, height=height, speed=0, color=(255,153,51), fill=focus, window=window)


class Entity:
	LIST = list()
	focus = None
	focus_view = True
	def __init__(self, window, x=0, y=0, focus=0):
		self.text_list = list()
		self.head = HeadEntity(window, x=x, y=y, text_list=self.text_list)
		self.foot = FootEntity(window, self.head.xbegin, self.head.yend, self.head.width, self.head.height, self.head, self.text_list)
		self.focus = FocusEntity(window, self.foot.xend, self.foot.yend-5, focus=focus)
		self.bg = Drawblock(x=x,y=y,color=(220,220,220),window=window,width=self.head.width, height=self.head.height+self.foot.height)
		Entity.LIST.append(self)
		if not focus:
			Entity.focus = self
		self.list_point = list()
		self.id = str(HeadEntity.number)+"e"


	def print(self):
		global focus_view
		self.bg.draw()
		self.head.print()
		self.foot.print()
		if Entity.focus_view:
			self.focus.draw()

	def set_name(self, new_name):
		self.head.print_name << new_name.upper()
		self.foot.idEntity << self.foot.idEntity.get_text()[0:2]+new_name.lower()
		self.ajust_dimension()

	def set_property(self, idp, new_name):
		self.foot.property[idp-1] << new_name
		self.ajust_dimension()

	def del_property(self, idp):
		del self.foot.property[idp-1]
		self.ajust_dimension()

	def add_property(self):
		self.foot.add_property(self.head, self.text_list)
		self.focus.set_position(self.foot.xend, self.foot.yend)
		self.ajust_dimension()

	def set_position(self, x, y):
		self.head.set_position(x-self.head.width//2, y-(self.head.height+self.foot.height)//2)
		self.foot.set_position(x-self.head.width//2, self.head.yend)
		self.focus.set_position(self.foot.xend, self.foot.yend)
		Drawblock.set_position(self.bg,self.head.xbegin,self.head.ybegin)
		for p in self.list_point:
			p.x = x
			p.y = y

	def change_position(self, x, y):
		self.head.set_position(x, y)
		self.foot.set_position(x, self.head.yend)
		self.focus.set_position(self.foot.xend, self.foot.yend)
		Drawblock.set_position(self.bg,self.head.xbegin,self.head.ybegin)
		for p in self.list_point:
			p.x = x+self.head.width//2
			p.y = y+(self.head.height+self.foot.height)//2

	def cursor_collide(self, cursor):
		if self.head.cursor_collide(cursor) or self.foot.cursor_collide(cursor):
			return True
		return False

	#no use
	def focus_cursor_collide(self, cursor):
		if self.focus.cursor_collide(cursor):
			return True
		return False

	def ajust_dimension(self):
		maxi = self.text_list[0].string.get_width()
		for t in self.text_list:
			if maxi < t.string.get_width():
				maxi = t.string.get_width()
		self.head.set_dimension(width=maxi+FILL)
		self.foot.set_dimension(width=maxi+FILL, height=(len(self.foot.property)+1)*self.head.print_name.string.get_height())
		self.focus.set_position(self.foot.xend, self.foot.yend)
		self.bg.set_dimension(width=self.head.width, height=self.head.height+self.foot.height)
		for p in self.list_point:
			p.x = self.foot.xbegin + self.foot.width//2
			p.y = self.foot.ybegin + self.foot.height//2

	def add_point(self, point):
		if len(Link.LIST):
			link = Link.LIST[len(Link.LIST)-1]
			"""link.cardinalite.x = (point.x + self.foot.width)
												link.cardinalite.y = (point.y + self.foot.height)"""
			for l in Link.LIST:
				if link.p1.parent == l.p2.parent and link.p2.parent == l.p1.parent:
					link.rect = True
					try:
						self.list_point.remove(l.p1)
						l.p2.parent.list_point.remove(l.p2)
						Link.LIST.remove(l)
					except:pass
		self.list_point.append(point)
		self.ajust_dimension()

	def __str__(self):
		info = str(self.head)+str(self.foot)
		for t in self.text_list:
			info += f"{t.get_text()}\n"
		return info
		

class Point:

	def __init__(self, x, y, parent):
		self.x = x
		self.y = y
		self.parent = parent
		if parent:
			self.parent.add_point(self)



class Link:
	LIST = list()
	focus = None
	def __init__(self, x, y, window, parent, no_focus=False, x2=None, y2=None, parent2=None):
		self.p1 = Point(x, y, parent)
		self.p2 = Point(x2, y2, parent2)
		"""self.cardinalite = Printstring(main_font=cardinalite_font, string="0 , N", color=(150,0,200), x=-100,y=-100)
								if type(parent) == Entity:
									self.cardinalite.x = (self.p1.x + parent.foot.width)
									self.cardinalite.y = (self.p1.y + parent.foot.height)"""
		self.rect = False
		self.window = window
		Link.LIST.append(self)
		if not no_focus:
			Link.focus = self
		self.parent = parent
		

	def update_drawing(self, x, y):
		self.p2.x = x
		self.p2.y = y
		pygame.draw.aaline(self.window, (0,100,100), (self.p1.x, self.p1.y), (x, y), 1)

	def draw(self):
		if self != Link.focus:
			if self.rect:
				if self.p2.x < self.p1.x:
					if self.p2.y > self.p1.y:
						pygame.draw.rect(self.window, (0,100,100), (self.p2.x, self.p1.y, abs(self.p2.x-self.p1.x), abs(self.p2.y-self.p1.y)), FILL)
					else:
						pygame.draw.rect(self.window, (0,100,100), (self.p2.x, self.p2.y, abs(self.p2.x-self.p1.x), abs(self.p2.y-self.p1.y)), FILL)
				elif self.p2.x > self.p1.x:
					if self.p2.y > self.p1.y:
						pygame.draw.rect(self.window, (0,100,100), (self.p1.x, self.p1.y, abs(self.p2.x-self.p1.x), abs(self.p2.y-self.p1.y)), FILL)
					else:
						pygame.draw.rect(self.window, (0,100,100), (self.p1.x, self.p2.y, abs(self.p2.x-self.p1.x), abs(self.p2.y-self.p1.y)), FILL)
			else:
				pygame.draw.aaline(self.window, (0,100,100), (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), 1)
				#self.cardinalite.write()

	def __str__(self):
		return f"{self.p1.x} {self.p1.y} {self.p1.parent.id} {self.p2.x} {self.p2.y} {self.p2.parent.id} {self.rect}\n"


class Cardinalite(Block):
	number = 0
	focus = None
	LIST = list()
	def __init__(self, x, y, txt="0,N"):
		self.text = Printstring(main_font=cardinalite_font, string=txt, color=(0,150,150), x=x, y=y)
		Block.__init__(self, x=x-self.text.string.get_width()//2, y=y-self.text.string.get_height()//2, 
			width=self.text.string.get_width(), height=self.text.string.get_height(), speed=0)
		self.text.x = self.xbegin
		self.text.y = self.ybegin
		Cardinalite.number += 1
		self.id = str(Cardinalite.number)+"c"
		Cardinalite.LIST.append(self)
		Cardinalite.focus = self

	def print(self):
		self.text.write()

	def set_position(self, x, y, mouse=False):
		if not mouse:
			Block.set_position(self, x,y)
		else:
			Block.set_position(self, x-self.width//2,y-self.height//2)
		self.text.x = self.xbegin
		self.text.y = self.ybegin

	def change_position(self, x, y):
		Block.set_position(self, x,y)
		self.text.x = self.xbegin
		self.text.y = self.ybegin

	def __str__(self):
		return f"{self.xbegin} {self.ybegin} {self.text.get_text()}\n"




