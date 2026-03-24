import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_with_headings(self):
        headings = [
            "# heading1",
            "## heading2",
            "### heading3",
            "#### heading4",
            "##### heading5",
            "###### heading6",
        ]
        for heading in headings:
            self.assertEqual(BlockType.HEADING, block_to_block_type(heading))

    def test_block_to_block_type_with_incorrect_headings(self):
        incorrect_headings = [
            "#heading1",
            "##heading2",
            "###heading3",
            "####heading4",
            "#####heading5",
            "######heading6",
        ]
        for incorrect_heading in incorrect_headings:
            self.assertNotEqual(
                BlockType.HEADING, block_to_block_type(incorrect_heading)
            )

    def test_block_to_block_type_with_code(self):
        code = """```
        code
        ```"""
        self.assertEqual(BlockType.CODE, block_to_block_type(code))

    def test_block_to_block_type_with_quote(self):
        quotes = ["> quote1", ">quote2"]
        for quote in quotes:
            self.assertEqual(BlockType.QUOTE, block_to_block_type(quote))

    def test_block_to_block_type_with_multiline_quote(self):
        quote = """> quote1
        > quote2
        > quote3
        > quote4"""
        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote))

    def test_block_to_block_type_with_incorrect_quotes(self):
        incorrect_quotes = ["quote1"]
        for incorrect_quote in incorrect_quotes:
            self.assertNotEqual(BlockType.QUOTE, block_to_block_type(incorrect_quote))

    def test_block_to_block_type_unordered_list(self):
        unordered_list = "- list"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered_list))

    def test_block_to_block_type_with_multiline_unordered_list(self):
        unordered_list = """- 1
        - 2
        - 3
        - 4
        - 5"""
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered_list))

    def test_block_to_block_type_incorrect_unordered_list(self):
        incorrect_list = "-list"
        self.assertNotEqual(
            BlockType.UNORDERED_LIST, block_to_block_type(incorrect_list)
        )

    def test_block_to_block_type_with_multiline_ordered_list(self):
        ordered_list = """1. 1
        2. 2
        3. 2"""
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(ordered_list))

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = """
# heading1

# heading2
"""
        title = extract_title(md)
        self.assertEqual(title, "heading1")

    def test_extract_title_with_no_title(self):
        md = """
## heading1

## heading2
"""
        self.assertRaises(ValueError, extract_title, md)


if __name__ == "__main__":
    unittest.main()
