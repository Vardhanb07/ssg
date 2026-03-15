import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_with_correct_props_html(self):
        test_props = {"src": "https://test.test", "alt": "test-alt"}
        test_props_html = f' src="{test_props["src"]}" alt="{test_props["alt"]}"'
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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "test-p")
        self.assertEqual(node.to_html(), "<p>test-p</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "test-p", {"class": "test"})
        self.assertEqual(node.to_html(), '<p class="test">test-p</p>')

    def test_repr(self):
        node = LeafNode("p", "test-p")
        self.assertEqual(node.__repr__(), "LeafNode(tag=p, value=test-p, props=None)")

    def test_leaf_with_no_html_tag(self):
        node = LeafNode(None, "test-text")
        self.assertEqual(node.to_html(), "test-text")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, "normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>bold text</b>normal text<i>italic text</i>normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h1",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, "normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h1><b>bold text</b>normal text<i>italic text</i>normal text</h1>",
        )


if __name__ == "__main__":
    unittest.main()
