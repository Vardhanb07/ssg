import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        nodes = []
        split_text = node.text.split(delimiter)
        delimiter_in_text = node.text.count(delimiter)
        if delimiter_in_text % 2 != 0:
            raise ValueError("invalid markdown, closing delimiter not found")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                nodes.append(TextNode(split_text[i], TextType.PLAIN_TEXT))
            else:
                nodes.append(TextNode(split_text[i], text_type))
        new_nodes.extend(nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)