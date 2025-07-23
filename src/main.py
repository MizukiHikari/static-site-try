from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter, split_nodes_image
from markdown_blocks import markdown_to_blocks


def main():
    md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
    blocks = markdown_to_blocks(md)
    return print(blocks)


if __name__ == "__main__":
    main()
