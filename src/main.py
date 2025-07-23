from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    obj = TextNode("Hello, World!", TextType.BOLD, "http://example.com")
    print(obj)


if __name__ == "__main__":
    main()
