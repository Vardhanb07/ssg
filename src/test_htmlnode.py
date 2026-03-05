import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_with_correct_props_html(self):
        test_props = {"src": "https://test.test", "alt": "test-alt"}
        test_props_html = f'src="{test_props["src"]}" alt="{test_props["alt"]}"'
        node = HTMLNode(tag="img", props=test_props)
        self.assertEqual(node.props_to_html(), test_props_html)

    def test_with_incorrect_props_html(self):
        test_props = {"src": "https://test.test", "alt": "test-alt"}
        test_props_html = f'src="{test_props["src"]}"alt="{test_props["alt"]}"'
        node = HTMLNode(tag="img", props=test_props)
        self.assertNotEqual(node.props_to_html(), test_props_html)

    def test_repr(self):
        node = HTMLNode(
            tag="img",
            value=None,
            children=None,
            props={"src": "http://test.test"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag=img, value=None, children=None, props={'src': 'http://test.test'})",
        )


if __name__ == "__main__":
    unittest.main()
