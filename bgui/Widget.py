from bgl import *

# Widget options
BGUI_NONE = 0
BGUI_CENTERX = 1
BGUI_CENTERY = 2
BGUI_NORMALIZED = 4

BGUI_DEFAULT = BGUI_NORMALIZED
BGUI_CENTERED = BGUI_CENTERX | BGUI_CENTERY

class Widget:
	"""The base widget class"""

	def __init__(self, parent, name, size=[0, 0], pos=[0, 0],
			options=BGUI_DEFAULT):
		"""The Widget constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""

		self.name = name
		self.options = options
		self.on_click = None

		# Setup the parent
		parent._attach_widget(self)
		self.parent = parent

		# A dictionary to store children widgets
		self.children = {}

		# Setup the widget's position
		self.position = [None]*4
		self._update_position(size, pos)


	def _update_position(self, size, pos):
		self._base_size = size[:]
		self._base_pos = pos[:]

		if self.options & BGUI_NORMALIZED:
			pos[0] *= self.parent.size[0]
			pos[1] *= self.parent.size[1]

			size[0] *= self.parent.size[0]
			size[1] *= self.parent.size[1]

		if self.options & BGUI_CENTERX:
			pos[0] = self.parent.size[0]/2 - size[0]/2

		if self.options & BGUI_CENTERY:
			pos[1] = self.parent.size[1]/2 - size[1]/2

		x = pos[0] + self.parent.position[0]
		y = pos[1] + self.parent.position[1]
		width = size[0]
		height = size[1]
		self.size = [width, height]
		# The "friendly" position
		self.position = [x, y]
		
		# OpenGL starts at the bottom left and goes counter clockwise
		self.gl_position = [
					[x, y],
					[x+width, y],
					[x+width, y+height],
					[x, y+height]
				]
				
	def _on_click(self, pos):
		"""Runs the on_click callback"""

		if self.on_click:
			self.on_click(self)
			
		# Run any children on_click methods
		for widget in [self.children[i] for i in self.children]:
			if (widget.gl_position[0][0] <= pos[0] <= widget.gl_position[1][0]) and \
				(widget.gl_position[0][1] <= pos[1] <= widget.gl_position[2][1]):
					widget._on_click(pos)			

	def _attach_widget(self, widget):
		"""Attaches a widget to this widget"""

		if not isinstance(widget, Widget):
			raise TypeError("Expected a Widget object")

		if widget in self.children:
			raise ValueError("%s is already attached to this widget" %s (widget.name))

		self.children[widget.name] = widget

	def _draw(self):
		"""Draws the widget and the widget's children"""

		# This base class has nothing to draw, so just draw the children

		for child in self.children:
			self.children[child]._draw()