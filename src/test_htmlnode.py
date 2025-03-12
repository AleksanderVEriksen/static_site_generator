import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link_img


class TestHtmlNode(unittest.TestCase):
	def test_HTML(self):
		mock=' href="https://www.google.com" target="_blank"'
		node = HTMLNode("a", "Yes", props={"href":"https://www.google.com","target":"_blank",})
		self.assertEqual(node.props_to_html(), mock)
	def test_HTML_props(self):
		mock =  ' href="https://www.google.com"'
		node = HTMLNode("a", "Yes",props = {"href":"https://www.google.com"})
		self.assertEqual(node.props_to_html(), mock)
	def test_HTML_no_props(self):
		node = HTMLNode("a","Yes")
		self.assertEqual(node.props_to_html(), "")
	def test_leaf_to_html_p(self):
			node = LeafNode("p", "Hello, world!")
			self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
	def test_leaf_to_html_p(self):
		node = LeafNode("", "Hello, world!")
		self.assertEqual(node.to_html(), "Hello, world!")
	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
        	parent_node.to_html(),
        	"<div><span><b>grandchild</b></span></div>",
    		)
	def test_to_html_no_children(self):
		with self.assertRaises(TypeError):
			parent_node = ParentNode("div")
	def test_to_html_None_child(self):
		with self.assertRaises(ValueError):
			parent_node = ParentNode("div", [])
			parent_node.to_html()

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")


	def test_textType(self):
		with self.assertRaises(Exception):
			node = TextNode("This is a text node", TextType.FISH)

	def test_node_delim_code(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		node2 = TextNode("This is a `bold` word for the best coding `part of my life`", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
		mock = [
    			TextNode("This is text with a ", TextType.TEXT),
    			TextNode("code block", TextType.CODE),
    			TextNode(" word", TextType.TEXT),
				TextNode("This is a ", TextType.TEXT),
    			TextNode("bold", TextType.CODE),
    			TextNode(" word for the best coding ", TextType.TEXT),
				TextNode("part of my life", TextType.CODE),
				]
		self.assertEqual(new_nodes, mock)

	def test_node_delim_bold(self):
		node = TextNode("This is **text** with a **code block** word", TextType.TEXT)
		node2 = TextNode("This is a **bold** word for the best coding **part of my life**", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
		mock = [
    			TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with a ", TextType.TEXT),
    			TextNode("code block", TextType.BOLD),
    			TextNode(" word", TextType.TEXT),
				TextNode("This is a ", TextType.TEXT),
    			TextNode("bold", TextType.BOLD),
    			TextNode(" word for the best coding ", TextType.TEXT),
				TextNode("part of my life", TextType.BOLD),
				]
		self.assertEqual(new_nodes, mock)

	def test_node_delim_ITALIC(self):
		node = TextNode("This is _text_ with a _code block_ word", TextType.TEXT)
		node2 = TextNode("This is a _bold_ word for the best coding _part of my life_", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
		mock = [
    			TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.ITALIC),
				TextNode(" with a ", TextType.TEXT),
    			TextNode("code block", TextType.ITALIC),
    			TextNode(" word", TextType.TEXT),
				TextNode("This is a ", TextType.TEXT),
    			TextNode("bold", TextType.ITALIC),
    			TextNode(" word for the best coding ", TextType.TEXT),
				TextNode("part of my life", TextType.ITALIC),
				]
		self.assertEqual(new_nodes, mock)

	def test_extract_markdown(self):
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
		actual = extract_markdown_images(text)
		self.assertEqual(actual,expected)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    	)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_links(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev)"
		matches = extract_markdown_links(text)
		self.assertListEqual([("to boot dev", "https://www.boot.dev")],matches)	

	def test_split_link(self):
		node = TextNode(
    		"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    		TextType.TEXT,
		)
		new_nodes = split_nodes_link_img([node], TextType.LINK)
		self.assertListEqual([
    	 		TextNode("This is text with a link ", TextType.TEXT),
     			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
     			TextNode(" and ", TextType.TEXT),
     			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
 					],new_nodes,
				)


	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link_img([node], TextType.IMAGE)
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode(
					"second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
				),
			],
			new_nodes,
		)



if __name__ == "__main__":
    unittest.main()

