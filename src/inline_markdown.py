import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    text_node = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    text_node = split_nodes_delimiter(text_node, "_", TextType.ITALIC)
    text_node = split_nodes_delimiter(text_node, "`", TextType.CODE)
    text_node = split_nodes_image(text_node)
    text_node = split_nodes_link(text_node)
    return text_node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        word_parts = old_node.text.split(delimiter)
        if len(word_parts) % 2 == 0:
            raise ValueError("Invalid markdown syntax: unmatched delimiter")

        for i in range(len(word_parts)):
            if word_parts[i] == "":
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(word_parts[i], TextType.TEXT))

            else:
                split_nodes.append(TextNode(word_parts[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        image_list = extract_markdown_images(original_text)

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        for image in image_list:
            image_alt, image_link = image
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        original_text = old_node.text
        link_list = extract_markdown_links(original_text)

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        for link in link_list:
            link_alt, link_url = link
            sections = original_text.split(f"[{link_alt}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes
