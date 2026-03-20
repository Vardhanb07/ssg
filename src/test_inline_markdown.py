import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
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
        text = "This is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_markdown_image_extraction_with_no_images(self):
        text = "This text only contains links [to youtube](https://www.youtube.com/@bootdotdev)"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [])

    def test_markdown_image_extraction_against_links(self):
        text = "This text contains image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and link [to boot dev](https://www.boot.dev)"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_markdown_link_extraction(self):
        text = "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_markdown_link_extraction_with_no_links(self):
        text = "This text only contains images ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [])

    def test_markdown_link_extraction_against_images(self):
        text = "This text contains image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and link [to boot dev](https://www.boot.dev)"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [("to boot dev", "https://www.boot.dev")])

    def test_split_markdown_images(self):
        text = "This text contains image ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        old_nodes = [TextNode(text, TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_images(old_nodes)
        self.assertListEqual(
            [
                TextNode("This text contains image ", TextType.PLAIN_TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"
                ),
            ],
            new_nodes,
        )

    def test_split_markdown_images_with_multiple_images(self):
        text = "This is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        old_nodes = [TextNode(text, TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_images(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.PLAIN_TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "obi wan", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
            ],
            new_nodes,
        )

    def test_split_markdown_images_with_multiple_old_nodes(self):
        old_nodes = [
            TextNode(
                "This is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.PLAIN_TEXT,
            ),
            TextNode(
                "This is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.PLAIN_TEXT,
            ),
        ]
        new_nodes = split_nodes_images(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.PLAIN_TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "obi wan", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode("This is a text with a ", TextType.PLAIN_TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "obi wan", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
            ],
            new_nodes,
        )

    def test_split_markdown_images_against_links(self):
        text = "This text contains image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and link [to boot dev](https://www.boot.dev)"
        old_nodes = [TextNode(text, TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_images(old_nodes)
        self.assertListEqual(
            [
                TextNode("This text contains image ", TextType.PLAIN_TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(
                    " and link [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT
                ),
            ],
            new_nodes,
        )

    def test_split_markdown_links(self):
        text = "This text only contains links [to youtube](https://www.youtube.com/@bootdotdev)"
        old_nodes = [TextNode(text, TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_links(old_nodes)
        self.assertListEqual(
            [
                TextNode("This text only contains links ", TextType.PLAIN_TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK_TEXT,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_markdown_links_with_multiple_links(self):
        text = "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        old_nodes = [TextNode(text, TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_links(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK_TEXT,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_markdown_links_with_multiple_old_nodes(self):
        old_nodes = [
            TextNode(
                "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.PLAIN_TEXT,
            ),
            TextNode(
                "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.PLAIN_TEXT,
            ),
        ]
        new_nodes = split_nodes_links(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK_TEXT,
                    "https://www.youtube.com/@bootdotdev",
                ),
                TextNode("This is a text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK_TEXT,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_markdown_links_against_images(self):
        text = "This text contains image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and link [to boot dev](https://www.boot.dev)"
        old_nodes = [TextNode(text, TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_links(old_nodes)
        self.assertListEqual(
            [
                TextNode(
                    "This text contains image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and link ",
                    TextType.PLAIN_TEXT,
                ),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
