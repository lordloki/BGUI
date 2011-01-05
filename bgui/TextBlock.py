from .Widget import *
from .Label import *

class TextBlock(Widget):
	"""Widget for displaying blocks of text"""
	
	def __init__(self, parent, name, text="", font=None, pt_size=30, color=None, aspect=None,
					size=[1, 1], pos=[0, 0], sub_theme='', overflow=BGUI_OVERFLOW_HIDDEN, options=BGUI_DEFAULT):
		"""The Label constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		text -- the text to display (this can be changed later via the text property)
		font -- the font to use
		pt_size -- the point size of the text to draw
		aspect -- constrain the widget size to a specified aspect ratio
		size -- a tuple containing the width and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""
		
		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)
		
		self.overflow = overflow
		self._font = font
		self._pt_size = pt_size
		self._color = color
		self._lines = []
		
		self.text = text
		
	@property
	def text(self):
		"""The text to display"""
		return self._text
		
	@text.setter
	def text(self, value):
		
		# Get rid of any old lines
		for line in self._lines:
			self._remove_widget(line)
		
		self._lines = []
		self._text = value
	
		# If the string is empty, then we are done
		if not value: return
	
		lines = value.split('\n')
		for i, v in enumerate(lines):
			lines[i] = v.split()
			
		cur_line = 0
		line = Label(self, "tmp", "Ay", self._font, self._pt_size, self._color)
		self._remove_widget(line)
		char_height = line.size[1]
	
		if self.options & BGUI_NORMALIZED:
			char_height /= self.size[1]
		
		for words in lines:
			line = Label(self, "lines_"+str(cur_line), "", self._font, self._pt_size, self._color, pos=[0, 1-(cur_line+1)*char_height])
			
			while words:
				# Try to add a word			
				if line.text:
					line.text += " " + words[0]
				else:
					line.text = words[0]
				
				# The line is too big, remove the word and create a new line
				if line.size[0] > self.size[0]:
					line.text = line.text[0:-(len(words[0])+1)]
					self._lines.append(line)
					cur_line += 1
					line = Label(self, "lines_"+str(cur_line), "", self._font, self._pt_size, self._color, pos=[0, 1-(cur_line+1)*char_height])
				else:
					# The word fit, so remove it from the words list
					words.remove(words[0])
					
			# Add what's left
			self._lines.append(line)
			cur_line += 1
			
		if self.overflow:
			line_height = char_height* (self.size[1] if self.options & BGUI_NORMALIZED else 1)
		
			while self.size[1] < len(self._lines)*line_height:
				if self.overflow == BGUI_OVERFLOW_HIDDEN:
					self._remove_widget(self._lines[-1])
					self._lines = self._lines[:-1]
					
				elif self.overflow == BGUI_OVERFLOW_REPLACE:
					self._remove_widget(self._lines[0])
					self._lines = self._lines[1:]
					for line in self._lines:
						if line.options & BGUI_NORMALIZED:
							line._update_position(line.size, [0, line._base_pos[1]+char_height])
						else:
							line._update_position(line.size, [0, line._base_pos[1]+(char_height*self.system.size[1])])
				
				elif self.overflow == BGUI_OVERFLOW_CALLBACK:
					if self.on_overflow:
						self.on_overflow(self)
						
		