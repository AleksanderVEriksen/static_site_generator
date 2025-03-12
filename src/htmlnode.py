from textnode import TextNode, TextType
import re

# Bootdev --> Wsl --> powershell --> wsl.exe --Ubuntu --> bootdev login --> cd /OneDrive/workspace/static_site_generator

# public$
# python3 -m http.server 8888

class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError
	def props_to_html(self):
		if self.props is None:
			return ""
		props_string = ""
		for key, value in self.props.items():
			props_string+=(f' {key}="{value}"')
		return props_string
	def __repr__(self):
		return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
class LeafNode(HTMLNode):
	def __init__(self, tag=None, value="Some text", props=None):
		super().__init__(tag=tag, value=value, children=None, props=props)
		if value == None:
			raise ValueError("Error: Value cant be None")
	def to_html(self):
		if self.tag in (None, ""):
			return f"{self.value}"
		if self.props == None:
			return f"<{self.tag}>{self.value}</{self.tag}>"
		else:
			return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag=tag, value=None, children=children, props=props)
	def to_html(self):
		if self.tag in (None, ""):
			raise ValueError("Error: Tag cannot be None or empty")
		if self.children in (None, []):
			raise ValueError("Error: Children cannot be None or empty")
		child_string = ""
		for child in self.children:
			child_string ="".join(child.to_html())
		return f"<{self.tag}>{child_string}</{self.tag}>"
def text_node_to_html_node(text_node):
	if text_node.text_type not in TextType:
		raise Exception
	else:
		if text_node.text_type == TextType.TEXT:
			return LeafNode(value=text_node.text)

		if text_node.text_type == TextType.BOLD:
			return LeafNode(tag="b", value=text_node.text)

		if text_node.text_type == TextType.ITALIC:
			return LeafNode(tag="_", value=text_node.text)

		if text_node.text_type == TextType.CODE:
			return LeafNode(tag="`", value=text_node.text)

		if text_node.text_type == TextType.LINK:
			return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

		if text_node.text_type == TextType.IMAGE:
			return LeafNode(tag="img",value="", props={"src": text_node.url, "alt": text_node.text})
		

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        # If not a text node, add it as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Process the text node to find delimiter pairs
        result_nodes = process_text_node(old_node.text, delimiter, text_type)
        new_nodes.extend(result_nodes)
        
    return new_nodes


def process_text_node(text, delimiter, text_type):
	result_nodes = []
	# Find first delimiter
	start_idx = text.find(delimiter)
	if start_idx == -1:
		# No delimiter found, return node as is
		return [TextNode(text, TextType.TEXT)] if text else []
	
	# Find matching closing delimiter
	end_idx = text.find(delimiter, start_idx + len(delimiter))
	if end_idx == -1:
		raise Exception(f"No closing delimiter found for '{delimiter}'") 
	# Text before the first delimiter
	if start_idx > 0:
		result_nodes.append(TextNode(text[:start_idx], TextType.TEXT))

	# Text between delimiters (without the delimiters) 
	special_text = text[start_idx + len(delimiter):end_idx]
	result_nodes.append(TextNode(special_text, text_type))

	# Process remaining text after second delimiter
	remaining_text = text[end_idx + len(delimiter):]
	if remaining_text:
		result_nodes.extend(process_text_node(remaining_text, delimiter,text_type))
	return result_nodes


def extract_markdown_images(text):

	alt_text = re.findall(r"\!\[(.*?)\]",text)
	url_text = re.findall(r"\((https:\/\/.*?)\)",text)
	pairs = len(alt_text)
	tuple = []
	for x in range(pairs):
		tuple.append((alt_text[x], url_text[x]))
	return tuple

def extract_markdown_links(text):
	import re
	alt_text = re.findall(r"\[(.*?)\]",text)
	url_text = re.findall(r"\((https:\/\/.*?)\)",text)
	pairs = len(alt_text)
	tuple = []
	for x in range(pairs):
		tuple.append((alt_text[x], url_text[x]))
	return tuple


mock_node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]

# Split text with link to text nodes
def split_nodes_link_img(old_nodes, Texttype):
	if Texttype == TextType.LINK or Texttype == TextType.IMAGE:
		new_nodes = []
		for old_node in old_nodes:
			text = old_node.text
			# If not a text node, add it as is
			if old_node.text_type != TextType.TEXT:
				new_nodes.append(old_node)
				continue
			if Texttype == TextType.IMAGE:
				text = text.replace("!","")
			# Process the text node to find delimiter pairs
			result_nodes = process_link_text_node(text, Texttype)
			new_nodes.extend(result_nodes)
	else:
		raise ValueError("Text needs to be converted to type IMAGE or LINK")
	return new_nodes

def process_link_text_node(text, Texttype):
	result_nodes = []
	# Find first delimiter
	start_idx = text.find("[")
	if start_idx == -1:
		# No delimiter found, return node as is
		return [TextNode(text, TextType.TEXT)] if text else []
	
	# Find matching closing delimiter
	end_idx = text.find("]", start_idx + len("["))
	if end_idx == -1:
		raise Exception(f"No closing delimiter found for '{"["}'") 
	# Text before the first delimiter
	if start_idx > 0:
		result_nodes.append(TextNode(text[:start_idx], TextType.TEXT))

	url_start = text.find("(")
	url_end = text.find(")", url_start+len("("))
	# Text between delimiters (without the delimiters)
	
	special_text = text[start_idx + len("["):end_idx]
	url_text = text[url_start + len("("):url_end]

	result_nodes.append(TextNode(special_text, Texttype, url=url_text))

	# Process remaining text after second delimiter
	remaining_text = text[url_end + len(")"):]
	if remaining_text:
		result_nodes.extend(process_link_text_node(remaining_text, Texttype))
	return result_nodes


# Split text with image to text nodes
def split_nodes_image(old_nodes):

	return None


