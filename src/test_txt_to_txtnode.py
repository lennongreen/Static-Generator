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

if __name__ == "__main__":
    unittest.main()