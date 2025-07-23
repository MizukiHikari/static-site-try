from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")

    if markdown_block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING

    elif len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    elif markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    elif markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    elif markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
