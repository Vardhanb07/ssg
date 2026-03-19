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


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)
        text_without_images = re.split(r"!\[.*?\]\(.*?\)", text)
        nodes = []
        offset = 0
        for i in range(len(text_without_images)):
            if text_without_images[i] != "":
                nodes.append(TextNode(text_without_images[i], TextType.PLAIN_TEXT))
            if offset + len(text_without_images[i]) < len(text):
                if text[offset + len(text_without_images[i])] == "!":
                    if len(images) > 0:
                        alt_text, link = images[0]
                        nodes.append(TextNode(alt_text, TextType.IMAGE_TEXT, link))
                        images.pop(0)
            offset += len(text_without_images[i])
            while offset < len(text) and text[offset] != ")":
                offset += 1
            offset += 1
        new_nodes.extend(nodes)
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)
        text_without_links = re.split(r"(?<!!)\[.*?\]\(.*?\)", text)
        nodes = []
        offset = 0
        for i in range(len(text_without_links)):
            if text_without_links[i] != "":
                nodes.append(TextNode(text_without_links[i], TextType.PLAIN_TEXT))
            if offset + len(text_without_links[i]) < len(text):
                if text[offset + len(text_without_links[i])] == "[":
                    if len(links) > 0:
                        inline_text, link = links[0]
                        nodes.append(TextNode(inline_text, TextType.LINK_TEXT, link))
                        links.pop(0)
            offset += len(text_without_links[i])
            while offset < len(text) and text[offset] != ")":
                offset += 1
            offset += 1
        new_nodes.extend(nodes)
    return new_nodes
