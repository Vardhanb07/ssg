import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


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


if __name__ == "__main__":
    unittest.main()
