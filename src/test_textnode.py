import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_when_both_are_equal(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_eq_when_both_nodes_have_different_text_types(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a anchor node", TextType.BOLD_TEXT, "https://url.url")
        self.assertNotEqual(node1, node2)

    def test_eq_when_both_nodes_have_different_text(self):
        node1 = TextNode("text 1", TextType.BOLD_TEXT)
        node2 = TextNode("text 2", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("test", TextType.BOLD_TEXT)
        self.assertEqual(
            node.__repr__(), "TextNode(text=test, text_type=bold, url=None)"
        )


if __name__ == "__main__":
    unittest.main()
