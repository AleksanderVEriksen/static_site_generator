from textnode import TextNode, TextType

def main():
	new_node = TextNode("This is some anchor text", TextType.LINKS, "https://www.boot.dev")
	print(new_node)

main()
