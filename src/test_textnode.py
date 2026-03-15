import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, node.text)

    def test_text_node_to_bold_node(self):
        node = TextNode("bold text", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, node.text)

    def test_text_node_to_italic_node(self):
        node = TextNode("italic text", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, node.text)

    def test_text_node_to_code_node(self):
        node = TextNode("code text", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, node.text)

    def test_text_node_to_link_node(self):
        url = "https://url.com/"
        node = TextNode("link text", TextType.LINK_TEXT, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": url})
        self.assertEqual(html_node.value, node.text)

    def test_text_node_to_image_node(self):
        node = TextNode("alt text", TextType.IMAGE_TEXT, "https://url.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": node.text})

    def test_unsupported_text_node_to_html_node_conversion(self):
        node = TextNode("alt", "unsupported")
        self.assertRaises(Exception, text_node_to_html_node, node)


if __name__ == "__main__":
    unittest.main()
