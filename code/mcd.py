from association import *
from threading import Thread

BGC = (255,255,255)
fini = False
temps = pygame.time.Clock()

icard = 1
card_txt = ["0,N", "0,1", "1,N", "1,1"]
save_font = Fontstring(size=30, bold=True, window=window.get_canva())
save = Printstring(main_font=save_font, x=10, y=10, color=(255,0,0))
save << "not saved"
cptr = 0
grab_entity = False
grab_association = False
grab_link = False
grab_cardinalite = False
gravity = False
class Focus:
	last_focus = None
	def __init__(self):pass
foc = Focus()
th_set_info = Thread(target=lambda:set_info(foc))
launched = False


LEFT = 1
RIGHT = 3

SAVED = (0,200,0)
UNSAVED = (200,0,0)

LIM = 50

while not fini:
	mx,  my = pygame.mouse.get_pos()
	cursor.set_position(mx,my)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			fini = True
		elif event.type == KEYUP:
			if event.key == K_UP:
				for e in Entity.LIST:
					e.change_position(x=e.head.xbegin,y=e.head.ybegin-LIM)
				for a in Association.LIST:
					a.set_position(x=a.xbegin,y=a.ybegin-LIM)
				for c in Cardinalite.LIST:
					c.change_position(x=c.xbegin,y=c.ybegin-LIM)
			elif event.key == K_DOWN:
				for e in Entity.LIST:
					e.change_position(x=e.head.xbegin,y=e.head.ybegin+LIM)
				for a in Association.LIST:
					a.set_position(x=a.xbegin,y=a.ybegin+LIM)
				for c in Cardinalite.LIST:
					c.change_position(x=c.xbegin,y=c.ybegin+LIM)
			elif event.key == K_RIGHT:
				for e in Entity.LIST:
					e.change_position(x=e.head.xbegin+LIM,y=e.head.ybegin)
				for a in Association.LIST:
					a.set_position(x=a.xbegin+LIM,y=a.ybegin)
				for c in Cardinalite.LIST:
					c.change_position(x=c.xbegin+LIM,y=c.ybegin)
			elif event.key == K_LEFT:
				for e in Entity.LIST:
					e.change_position(x=e.head.xbegin-LIM,y=e.head.ybegin)
				for a in Association.LIST:
					a.set_position(x=a.xbegin-LIM,y=a.ybegin)
				for c in Cardinalite.LIST:
					c.change_position(x=c.xbegin-LIM,y=c.ybegin)

			elif event.key == K_v:
				Entity.focus_view = not Entity.focus_view
				Association.focus_view = not Association.focus_view

			elif event.key == K_e:
				if save.color == SAVED:
					save << "not saved"
					save.color = UNSAVED
					save.refresh()
				if Entity.focus:
					Entity.focus.focus.fill = 3
				if Association.focus:
					Association.focus.focus.fill = 3
				Focus.last_focus = Entity(window.get_canva(), mx, my)
				if not launched:
					th_set_info.start()
					launched = True

			elif event.key == K_a:
				if save.color == SAVED:
					save << "not saved"
					save.color = UNSAVED
					save.refresh()
				if Association.focus:
					Association.focus.focus.fill = 3
				if Entity.focus:
					Entity.focus.focus.fill = 3
				Focus.last_focus = Association(window.get_canva(), mx, my)
				if not launched:
					th_set_info.start()
					launched = True

			elif event.key == K_c:
				if save.color == SAVED:
					save << "not saved"
					save.color = UNSAVED
					save.refresh()
				Cardinalite(mx, my)
			elif event.key == K_SPACE:
				if type(Focus.last_focus) == Cardinalite:
					Focus.last_focus.text << card_txt[icard]
					icard = (icard+1)%4

			elif event.key == K_p:
				if Entity.focus:
					Entity.focus.add_property()

			elif event.key == K_RETURN and not launched:
				open_mcd("mcd_save.txt")

			elif event.key == K_BACKSPACE:#delete
				if Focus.last_focus:
					if type(Focus.last_focus) != Cardinalite:
						for p in Focus.last_focus.list_point:
							for l in Link.LIST:
								if l.p1 == p:
									l.p2.parent.list_point.remove(l.p2)
									Link.LIST.remove(l)
								elif l.p2 == p:
									l.p1.parent.list_point.remove(l.p1)
									Link.LIST.remove(l)
					type(Focus.last_focus).LIST.remove(Focus.last_focus)
					Focus.last_focus = None

			elif event.key == K_s and launched:
				save_mcd()
				save << "saved"
				save.color = SAVED
				save.refresh()

			elif event.key == K_g:
				gravity = not gravity
						

		elif event.type == MOUSEBUTTONDOWN:
			if event.button == LEFT:
				for e in Entity.LIST:
					if e.cursor_collide(cursor):
						if not launched:
							th_set_info.start()
							launched = True
						if Entity.focus:
							Entity.focus.focus.fill = 3
						Entity.focus = e
						Entity.focus.focus.fill = 0
						grab_entity = True
						Focus.last_focus = Entity.focus
						break
				for a in Association.LIST:
					if a.cursor_collide(cursor):
						if not launched:
							th_set_info.start()
							launched = True
						if Association.focus:
							Association.focus.focus.fill = 3
						Association.focus = a
						Association.focus.focus.fill = 0
						grab_association = True
						Focus.last_focus = Association.focus
						break
				for c in Cardinalite.LIST:
					if c.cursor_collide(cursor):
						grab_cardinalite = True
						Cardinalite.focus = c
						if Focus.last_focus:
							Focus.last_focus.focus.fill = 3
						Focus.last_focus = Cardinalite.focus

			elif event.button == RIGHT and not grab_link:
				for e in Entity.LIST:
					if e.cursor_collide(cursor):
						Link(mx, my, window.get_canva(), parent=e)
						grab_link = True
						if Association.focus:
							Association.focus.focus.fill = 3
						if Entity.focus:
							Entity.focus.focus.fill = 3
						Entity.focus = e
						Entity.focus.focus.fill = 0
						Focus.last_focus = Entity.focus
						break
				if not grab_link:
					for a in Association.LIST:
						if a.cursor_collide(cursor):
							Link(mx, my, window.get_canva(), parent=a)
							grab_link = True
							if Entity.focus:
								Entity.focus.focus.fill = 3
							if Association.focus:
								Association.focus.focus.fill = 3
							Association.focus = a
							Association.focus.focus.fill = 0
							Focus.last_focus = Association.focus
							break

		elif event.type == MOUSEBUTTONUP:
			grab_entity = False
			grab_association = False
			grab_cardinalite = False
			if grab_link:
				collide = False
				for e in Entity.LIST:
					if e != Focus.last_focus:
						if e.cursor_collide(cursor):
							collide = True
							Link.focus.p2.parent = e
							e.add_point(Link.focus.p2)
							break
				if not collide:
					for a in Association.LIST:
						if a != Focus.last_focus:
							if a.cursor_collide(cursor):
								collide = True
								Link.focus.p2.parent = a
								a.add_point(Link.focus.p2)
								break
				if not collide:
					Link.LIST.remove(Link.focus)
				else:
					Link.focus = 0
				grab_link = False

	if grab_entity:
		Entity.focus.set_position(mx, my)
		if Association.focus:
				Association.focus.focus.fill = 3
	if grab_association:
		Association.focus.set_position(mx, my)
		if Entity.focus:
				Entity.focus.focus.fill = 3
	if grab_cardinalite:
		Cardinalite.focus.set_position(mx, my, True)

	if gravity:
		for e in Entity.LIST:
			BGC = (50,50,50)
			e.head.print_name << "!!!!"
			e.set_position(mx+randint(-20,20), my+randint(-20,20))
			for p in e.foot.property:
				p << "!!!!"
		if len(Entity.LIST) and cptr == 12:

			cptr = -1
			del Entity.LIST[len(Entity.LIST)-1]
		elif not len(Entity.LIST):
			gravity = not gravity
			BGC = (255,255,255)
		for a in Association.LIST:
			a.print_name << "   O_O"
		cptr += 1


	temps.tick(60)

	window.fill(BGC)
	if grab_link:
		Link.focus.update_drawing(mx, my)
	for l in Link.LIST:
		l.draw()
	for e in Entity.LIST:
		e.print()
	for a in Association.LIST:
		a.print()
	for c in Cardinalite.LIST:
		c.print()
	save.write()
	pygame.display.flip()

if launched:
	th_set_info.join()

