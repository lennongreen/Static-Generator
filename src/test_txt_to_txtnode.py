import unittest
from text_to_textnode import *


class TestTextToTextNode(unittest.TestCase):
    def test_eq(self):
        node = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        assert len(node) == len(expected)
        for i in range(len(node)):
            self.assertEqual(node[i].text, expected[i].text)
            self.assertEqual(node[i].text_type, expected[i].text_type)

    def test_text_only(self):
        node = text_to_textnodes("This should only be text")
        assert len(node) == 1
        self.assertEqual(node[0].text, "This should only be text")
        self.assertEqual(node[0].text_type, TextType.TEXT)

    def test_single_format(self):
        node = text_to_textnodes("Here is my text and **oh man** that was bolded")
        expected = [
            TextNode("Here is my text and ", TextType.TEXT),
            TextNode("oh man", TextType.BOLD),
            TextNode(" that was bolded", TextType.TEXT)
        ]

        assert len(node) == len(expected)
        for i in range(len(node)):
            self.assertEqual(node[i].text, expected[i].text)
            self.assertEqual(node[i].text_type, expected[i].text_type)
        
    def test_multiple_format(self):
        node = text_to_textnodes("Here is my text and **oh man** that was bolded now I hope it *doesn't*...Italisize")
        expected = [
            TextNode("Here is my text and ", TextType.TEXT),
            TextNode("oh man", TextType.BOLD),
            TextNode(" that was bolded now I hope it ", TextType.TEXT),
            TextNode("doesn't", TextType.ITALIC),
            TextNode("...Italisize", TextType.TEXT)
        ]

        assert len(node) == len(expected)
        for i in range(len(node)):
            self.assertEqual(node[i].text, expected[i].text)
            self.assertEqual(node[i].text_type, expected[i].text_type)

    def test_invalid_markdown(self):
        # missing closing
        with self.assertRaises(Exception):
            node = text_to_textnodes("This is [a link without closing")

        # missing attribute
        with self.assertRaises(Exception):
            node = text_to_textnodes("This is text with a link [to boot dev]")

    # Markdown Blocks

    def test_eq(self):
        markdown = """
            # Heading

            Paragraph 1


            * List item 1
            * List item 2

            Final paragraph
        """
        expected = [
            "# Heading",
            "Paragraph 1",
            "* List item 1\n* List item 2",
            "Final paragraph"
        ]

        result = markdown_to_block(markdown)
        self.assertEqual(result, expected)

    # test block_types

    def test_heading(self):
        test_string1 = "### This is a heading"
        test_string2 = "# This is a heading"
        test_string3 = "###### This is a heading"
        expected = "heading"
        self.assertEqual(block_to_block_type(test_string1), expected)
        self.assertEqual(block_to_block_type(test_string2), expected)
        self.assertEqual(block_to_block_type(test_string3), expected)

    def test_paragraph(self):
        test_string = "This is a paragraph"
        expected = "paragraph"
        self.assertEqual(block_to_block_type(test_string), expected)

    def test_code(self):
        test_string = "```This is code```"
        expected = "code"
        self.assertEqual(block_to_block_type(test_string), expected)

    def test_quote(self):
        test_string = "> This is a quote"
        expected = "quote"
        self.assertEqual(block_to_block_type(test_string), expected)

    def test_unordered_list(self):
        test_string1 = "* First Item\n* Second Item\n* Third Item"
        test_string2 = "- First Item\n- Second Item\n- Third Item"
        expected = "unordered_list"
        self.assertEqual(block_to_block_type(test_string1), expected)
        self.assertEqual(block_to_block_type(test_string2), expected)

    def test_ordered_list(self):
        test_string = "1. First Item\n2. Second Item\n3. Third Item\n4. Fourth Item\n5. Fifth Item"
        expected = "ordered_list"
        self.assertEqual(block_to_block_type(test_string), expected)

    # special type cases
    def test_code_empty(self):
        test_string = "``````"
        expected = "code"
        self.assertEqual(block_to_block_type(test_string), expected)

    def test_quote_empty(self):
        test_string = "> "
        expected = "quote"
        self.assertEqual(block_to_block_type(test_string), expected)

    def test_single_unordered(self):
        test_string = "- First Item"
        expected = "unordered_list"
        self.assertEqual(block_to_block_type(test_string), expected)
    
    def test_mix_symbol_undordered(self):
        test_string = "* First Item\n- Second Item"
        expected = "unordered_list"
        self.assertEqual(block_to_block_type(test_string), expected)

    def test_wrong_start_ordered(self):
        test_string = "2. First Item\n3. Second Item\n4. Third Item\n5. Fourth Item\n6. Fifth Item"
        expected = "paragraph"
        self.assertEqual(block_to_block_type(test_string), expected)
    



if __name__ == "__main__":
    unittest.main()