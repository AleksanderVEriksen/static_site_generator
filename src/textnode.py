from enum import Enum



class TextType(Enum):

	TEXT = "text"     # For normal text
	BOLD = "bold"     # For bold text
	ITALIC = "Italic" # For italic text
	CODE = "Code"     # For code text
	LINK = "Link"   # For links
	IMAGE = "Image"  # For images


class TextNode:
	
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = TextType(text_type)
		self.url = url

	def __eq__(self, other):
		
		if not isinstance(other, TextNode):
			return False
		return (self.text == other.text and
			self.text_type == other.text_type and
			self.url == other.url
			)
	
	def __repr__(self):

		return (f"TextNode({self.text},{self.text_type.value},{self.url})")
