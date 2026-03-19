import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_inline_markdown_with_no_nested_elements(self):
        node = TextNode("plain text no inline elements", TextType.CODE_TEXT)
        old_nodes = [node]
        delimiter = ""
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes, old_nodes)

    def test_inline_markdown_with_nested_element(self):
        node = TextNode("plain text with **bold text**", TextType.PLAIN_TEXT)
        old_nodes = [node]
        delimiter = "**"
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.BOLD_TEXT)
        self.assertEqual(
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
        self.assertEqual(
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
        self.assertEqual(
            [
                TextNode("plain text with ", TextType.PLAIN_TEXT),
                TextNode("bold text 1", TextType.BOLD_TEXT),
                TextNode("plain text with ", TextType.PLAIN_TEXT),
                TextNode("bold text 2", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
