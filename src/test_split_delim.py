import unittest
from .split_delim import *
from .textnode import *

class TestMarkDown(unittest.TestCase):

    def test_eq(self):
        node = split_nodes_delimiter([TextNode("Hello *world*", TextType.TEXT)], "*", TextType.ITALIC)
        node2 = split_nodes_delimiter([TextNode("Hello *world*", TextType.TEXT)], "*", TextType.ITALIC)
        assert len(node) == len(node2)
        assert node[0].text == node2[0].text
        assert node[0].text_type == node2[0].text_type

    def test_no_delim(self):
        node = split_nodes_delimiter([TextNode("Hello world", TextType.TEXT)], "*", TextType.ITALIC)
        assert len(node) == 1
        assert node[0].text == "Hello world"
        assert node[0].text_type == TextType.TEXT

    def test_paired_delim(self):
        node = split_nodes_delimiter([TextNode("Hello *world*", TextType.TEXT)], "*", TextType.ITALIC)
        assert len(node) == 2
        assert node[0].text == "Hello "
        assert node[1].text == "world"
        assert node[0].text_type == TextType.TEXT
        assert node[1].text_type == TextType.ITALIC

    def test_unpaired_delim(self):
        with self.assertRaises(Exception):
            node = split_nodes_delimiter([TextNode("Hello **world", TextType.TEXT)], "**", TextType.BOLD)

    def test_multiple_pairs(self):
        node = split_nodes_delimiter([TextNode("Hello *world* and hello *sky*", TextType.TEXT)], "*", TextType.ITALIC)
        assert len(node) == 4
        assert node[0].text == "Hello "
        assert node[1].text == "world"
        assert node[2].text == " and hello "
        assert node[3].text == "sky"
        assert node[0].text_type == TextType.TEXT
        assert node[1].text_type == TextType.ITALIC
        assert node[2].text_type == TextType.TEXT
        assert node[3].text_type == TextType.ITALIC

    def test_empty_delim(self):
        with self.assertRaises(Exception):
            node = split_nodes_delimiter([TextNode("Hello ** world", TextType.TEXT)], "*", TextType.ITALIC)

    def test_start_with_delim(self):
        node = split_nodes_delimiter([TextNode("*Hello* world", TextType.TEXT)], "*", TextType.ITALIC)
        assert len(node) == 2
        assert node[0].text == "Hello"
        assert node[0].text_type == TextType.ITALIC
        assert node[1].text == " world"
        assert node[1].text_type == TextType.TEXT

    def test_end_with_delim(self):
        node = split_nodes_delimiter([TextNode("Hello *world*", TextType.TEXT)], "*", TextType.ITALIC)
        assert len(node) == 2
        assert node[0].text == "Hello "
        assert node[0].text_type == TextType.TEXT
        assert node[1].text == "world"
        assert node[1].text_type == TextType.ITALIC

    def test_delim_only_space(self):
        with self.assertRaises(Exception):
            node = split_nodes_delimiter([TextNode("Hello * * world", TextType.TEXT)], "*", TextType.ITALIC)

    def test_non_text(self):
        node = split_nodes_delimiter([TextNode("**Hello**", TextType.BOLD)], "**", TextType.BOLD)
        assert len(node) == 1
        assert node[0].text == "Hello"
        assert node[0].text_type == TextType.BOLD

if __name__ == "__main__":
    unittest.main()