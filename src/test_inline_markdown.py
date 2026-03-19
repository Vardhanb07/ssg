import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_inline_markdown_with_no_nested_elements(self):
        node = TextNode("plain text no inline elements", TextType.CODE_TEXT)
        old_nodes = [node]
        delimiter = ""
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.PLAIN_TEXT)
        self.assertListEqual(new_nodes, old_nodes)

    def test_inline_markdown_with_nested_element(self):
        node = TextNode("plain text with **bold text**", TextType.PLAIN_TEXT)
        old_nodes = [node]
        delimiter = "**"
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("plain text with ", TextType.PLAIN_TEXT),
                TextNode("bold text", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_inline_markdown_with_incomplete_nested_element(self):
        node = TextNode("plain text with **bold text", TextType.PLAIN_TEXT)
        old_nodes = [node]
        delimiter = "**"
        self.assertEqual(node.text.count(delimiter), 1)
        self.assertRaises(
            ValueError, split_nodes_delimiter, old_nodes, delimiter, TextType.BOLD_TEXT
        )

    def test_inline_markdown_with_multiple_nested_elements(self):
        node = TextNode(
            "plain text with **bold text 1** and **bold text 2**", TextType.PLAIN_TEXT
        )
        old_nodes = [node]
        delimiter = "**"
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("plain text with ", TextType.PLAIN_TEXT),
                TextNode("bold text 1", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("bold text 2", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_inline_markdown_with_multiple_nodes(self):
        old_nodes = [
            TextNode("plain text with **bold text 1**", TextType.PLAIN_TEXT),
            TextNode("plain text with **bold text 2**", TextType.PLAIN_TEXT),
        ]
        delimiter = "**"
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("plain text with ", TextType.PLAIN_TEXT),
                TextNode("bold text 1", TextType.BOLD_TEXT),
                TextNode("plain text with ", TextType.PLAIN_TEXT),
                TextNode("bold text 2", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_markdown_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_markdown_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
