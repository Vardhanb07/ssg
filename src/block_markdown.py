from enum import Enum
import re


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
    if len(split_text) > 1 and split_text[0].startswith("```") and split_text[-1].endswith("```"):
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
