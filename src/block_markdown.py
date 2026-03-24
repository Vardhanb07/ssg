from enum import Enum
import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block == "":
            continue
        result.append(block.strip())
    return result


class BlockType(Enum):
    PARAGRAPH = "PARAGRAH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"


def block_to_block_type(block):
    split_text = block.split("\n")
    if len(split_text) == 1 and re.match(r"#{0,6} ", split_text[0]):
        return BlockType.HEADING
    if (
        len(split_text) > 1
        and split_text[0].startswith("```")
        and split_text[-1].endswith("```")
    ):
        return BlockType.CODE
    is_quote = True
    is_unordered_list = True
    is_ordered_list = True
    for idx, text in enumerate(split_text):
        is_quote = is_quote and text.strip().startswith(">")
        is_unordered_list = is_unordered_list and text.strip().startswith("- ")
        is_ordered_list = is_ordered_list and text.strip().startswith(f"{idx + 1}. ")
    if is_quote:
        return BlockType.QUOTE
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError("Block type not supported")


def text_to_html_nodes(block):
    text_nodes = text_to_textnodes(block)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def paragraph_to_html_node(block):
    block = block.replace("\n", " ")
    children = text_to_html_nodes(block)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for c in block:
        if c == "#":
            level += 1
        else:
            break
    max_heading_level = 6
    if level > max_heading_level:
        raise ValueError(f"invalid heading level: {level}")
    tag = f"h{level}"
    text = block[level + 1 :]
    children = text_to_html_nodes(text)
    return ParentNode(tag, children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    block = block[4:-3]
    raw_text_node = TextNode(block, TextType.PLAIN_TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise TypeError("invalid quote block")
        new_lines.append(line.replace(">", "").strip())
    text = " ".join(new_lines)
    children = text_to_html_nodes(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    list_items = block.split("\n")
    children = []
    for item in list_items:
        text = item[2:].strip()
        children.append(ParentNode("li", text_to_html_nodes(text)))
    return ParentNode("ul", children)


def ordered_list_to_html_node(block):
    list_items = block.split("\n")
    children = []
    for item in list_items:
        text = item.split(".", 1)[1].strip()
        children.append(ParentNode("li", text_to_html_nodes(text)))
    return ParentNode("ol", children)
