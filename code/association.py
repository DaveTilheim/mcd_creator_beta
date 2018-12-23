from entity import *
import os

association_font = Fontstring(size=20, italic=True, bold=True, window=window.get_canva())

class FocusAssociation(Drawblock):

	def __init__(self,  window, x, y, size=10, focus=0):
		Drawblock.__init__(self, x=x, y=y, width=size*2, height=size*2, speed=1, color=(255,153,51), fill=focus, window=window)


class Association(Drawblock):
	LIST = list()
	focus = None
	number = 0
	focus_view = True
	def __init__(self, window, x, y, focus=0):
		
		Association.number += 1
		self.print_name = Printstring(main_font=association_font, string=f"association{Association.number}", 
			color=(200,50,100), x=x, y=y)
		Drawblock.__init__(self, x=x, y=y,
			width=self.print_name.string.get_width(), height=self.print_name.string.get_width(), speed=1, color=(0,0,0), fill=FILL, window=window)
		self.focus = FocusAssociation(window, self.xbegin+self.print_name.string.get_width()//2, self.ybegin+self.print_name.string.get_width()//2,focus=focus)
		self.print_name.x -= self.width//2
		self.print_name.y -= self.print_name.string.get_height()//2
		self.hit_box = Block(x=self.xbegin-self.width//2, y=self.ybegin-self.height//2, width=self.width, height=self.height)
		self.bg = Drawblock(x=x,y=y,color=(220,220,220),window=window,width=self.width, height=self.height)
		if not focus:
			Association.focus = self
		Association.LIST.append(self)
		self.list_point = list()
		self.id = str(Association.number)+"a"

	def cursor_collide(self, cursor):
		if self.hit_box.cursor_collide(cursor):
			return True
		return False

	def set_position(self, x, y):
		Drawblock.set_position(self, x, y)
		Drawblock.set_position(self.bg, x, y)
		self.hit_box.set_position(x-self.width//2, y-self.height//2)
		self.print_name.x = x - self.width//2
		self.print_name.y = y - self.print_name.string.get_height()//2
		self.focus.set_position(self.xbegin+self.print_name.string.get_width()//2, self.ybegin+self.print_name.string.get_width()//2)
		for p in self.list_point:
			p.x = x
			p.y = y


	def print(self):
		self.bg.draw("circle")
		self.draw("circle")
		if Association.focus_view:
			self.focus.draw("circle")
		self.print_name.write()

	def set_name(self, new_name):
		self.print_name << new_name
		self.set_ajustement()

	def set_ajustement(self):
		self.set_dimension(width=self.print_name.string.get_width())
		self.bg.set_dimension(width=self.width)
		self.hit_box.set_dimension(width=self.width, height=self.height)
		self.hit_box.set_position(self.xbegin-self.width//2, self.ybegin-self.height//2)
		self.focus.set_position(self.xbegin+self.print_name.string.get_width()//2, self.ybegin+self.print_name.string.get_width()//2)
		for p in self.list_point:
			p.x = self.xbegin
			p.y = self.ybegin

	def add_point(self, point):
		if len(Link.LIST):
			link = Link.LIST[len(Link.LIST)-1]
			for l in Link.LIST:
				if l != link:
					if link.p1.parent == l.p2.parent and link.p2.parent == l.p1.parent:
						link.rect = True
						try:
							self.list_point.remove(l.p1)
							l.p2.parent.list_point.remove(l.p2)
							Link.LIST.remove(l)
						except:pass
		self.list_point.append(point)
		self.set_ajustement()

	def __str__(self):
		return f"{self.xbegin} {self.ybegin}\n{self.print_name.get_text()}\n"



def set_info(type_focus):

	if not type(type_focus.last_focus):return None
	cmd = str()
	
	split_cmd = list()
	while cmd != "end":
		os.system("clear")
		print("\n[commands]\nchanged the name of the current element: 'name' <new_name>")
		print("change the name of a proprety of the current entity: 'n°proprety' <new_name>")
		print("delete a proprety of the current entity: 'del' <n°proprety>")
		print("create a link between the current element and an association or an entity: 'link' <association/entity>")
		print("destroy a link between the current element and an association or an entity: 'delink' <association/entity>")
		print("quit the application: 'end'\n")
		cmd = input("[cmd]> ")
		split_cmd = cmd.split()
		if len(split_cmd):
			if split_cmd[0] == "name":
				if len(split_cmd) == 2:
					type(type_focus.last_focus).focus.set_name(split_cmd[1])
			elif split_cmd[0] == "link":
				if len(split_cmd) == 2:
					linked = None
					find = False
					if type(type_focus.last_focus) == Entity:
						for a in Association.LIST:
							if split_cmd[1] == a.print_name.get_text():
								linked = a
								find = True
								break
						if find:
							link = Link(type_focus.last_focus.foot.xbegin+type_focus.last_focus.foot.width//2, 
								type_focus.last_focus.foot.ybegin+type_focus.last_focus.foot.height//2, 
								type_focus.last_focus.foot.window, type_focus.last_focus, True)
							link.p2.x = linked.xbegin
							link.p2.y = linked.ybegin
							link.p2.parent = linked
							linked.add_point(link.p2)
					else:
						for e in Entity.LIST:
							if split_cmd[1].upper() == e.head.print_name.get_text():
								linked = e
								find = True
								break
						if find:
							link = Link(type_focus.last_focus.xbegin, 
								type_focus.last_focus.ybegin, 
								type_focus.last_focus.window, type_focus.last_focus, True)
							link.p2.x = linked.foot.xbegin+linked.foot.width//2
							link.p2.y = linked.foot.ybegin+linked.foot.height//2
							link.p2.parent = linked
							linked.add_point(link.p2)

			elif split_cmd[0] == "delink":
				if len(split_cmd) == 2:
					linked = None
					find = False
					if type(type_focus.last_focus) == Entity:
						for a in Association.LIST:
							if split_cmd[1] == a.print_name.get_text():
								linked = a
								find = True
								break
						if find:
							for l in Link.LIST:
								if l.p1.parent == type_focus.last_focus and l.p2.parent == linked:
									type_focus.last_focus.list_point.remove(l.p1)
									linked.list_point.remove(l.p2)
									Link.LIST.remove(l)
								elif l.p2.parent == type_focus.last_focus and l.p1.parent == linked:
									type_focus.last_focus.list_point.remove(l.p2)
									linked.list_point.remove(l.p1)
									Link.LIST.remove(l)
					else:
						for a in Entity.LIST:
							if split_cmd[1].upper() == a.head.print_name.get_text():
								linked = a
								find = True
								break
						if find:
							for l in Link.LIST:
								if l.p1.parent == type_focus.last_focus and l.p2.parent == linked:
									type_focus.last_focus.list_point.remove(l.p1)
									linked.list_point.remove(l.p2)
									Link.LIST.remove(l)
								elif l.p2.parent == type_focus.last_focus and l.p1.parent == linked:
									type_focus.last_focus.list_point.remove(l.p2)
									linked.list_point.remove(l.p1)
									Link.LIST.remove(l)

			elif type(type_focus.last_focus) == Entity:
				if split_cmd[0] == "del":
					if len(split_cmd) == 2:
						try:
							idp = int(split_cmd[1])
							Entity.focus.del_property(idp)
						except:
							print("\athe id must be an integer")

				elif split_cmd[0] != "end":
					if len(split_cmd) == 2:
						try:
							idp = int(split_cmd[0])
							Entity.focus.set_property(idp, split_cmd[1])
						except:
							print("\athe id must be an integer")

	print("\nexit ...\n")
	fini = True


def save_mcd(filename="mcd_save.txt"):
	file = open(filename, "w")
	file.write(f"{len(Entity.LIST)}\n")
	i = 1
	for e in Entity.LIST:
		e.id = str(i)+"e"
		file.write(str(e)+" "+str(i)+"e"+"\n")
		i+=1
	file.write(f"{len(Association.LIST)}\n")
	i = 1
	for a in Association.LIST:
		a.id = str(i)+"a"
		file.write(str(i)+"a"+" "+str(a)+"\n")
		i+=1
	for l in Link.LIST:
		file.write(str(l))
	file.write("c "+str(len(Cardinalite.LIST))+"\n")
	for c in Cardinalite.LIST:
		file.write(str(c)+"\n")
	file.close()


def open_mcd(filename="mcd_save.txt"):
	file = open(filename, "r")
	content = file.read().split()
	file.close()

	n_entity = int()
	n_association = int()

	n_entity = int(content[0])
	del content[0]
	for i in range(0, n_entity, 1):
		x_h = int(content[0])
		y_h = int(content[1])
		w_h = int(content[2])
		h_h = int(content[3])
		x_f = int(content[4])
		y_f = int(content[5])
		w_f = int(content[6])
		h_f = int(content[7])
		name = content[8]
		idname = content[9]
		list_p = list()
		while content[10][0].isalpha() == True:
			list_p.append(content[10])
			del content[10]
		ide = content[10]
		del content[:11]

		e = Entity(window.get_canva(), x_h, y_h, 3)
		e.head.print_name << name
		e.foot.idEntity << idname
		for p in list_p:
			e.foot.property.append(Printstring(main_font=property_font, string=p, 
			color=(0,0,0), x=e.head.print_name.x+FILL, y=e.head.yend+(len(e.foot.property)+1)*e.head.print_name.string.get_height()))
		for p in e.foot.property:
			e.text_list.append(p)
		e.ajust_dimension()

	n_association = int(content[0])
	del content[0]
	for i in range(0, n_association, 1):
		ida = content[0]
		x_a = int(content[1])
		y_a = int(content[2])
		name = content[3]
		del content[:4]

		a = Association(window.get_canva(), x_a, y_a, focus=3)
		a.print_name << name
		a.set_ajustement()

	while content[0] != "c":
		x_1 = int(content[0])
		x_2 = int(content[1])
		p_1 = content[2]
		y_1 = int(content[3])
		y_2 = int(content[4])
		p_2 = content[5]
		rect = content[6]
		del content[:7]
		for e in Entity.LIST:
			if e.id == p_1:
				p_1 = e
				break
			elif e.id == p_2:
				p_2 = e
				break
		for a in Association.LIST:
			if a.id == p_1:
				p_1 = a
				break
			elif a.id == p_2:
				p_2 = a
				break
		l = Link(x_1, y_1, window.get_canva(), p_1, True, x_2, y_2, p_2)
		if rect == "True":
			l.rect = True
	del content[0]
	n_card = int(content[0])
	del content[0]
	while len(content):
		x = int(content[0])
		y = int(content[1])
		txt = content[2]
		c = Cardinalite(x, y, txt)
		c.set_position(x, y)
		del content[:3]








