import unittest
from  htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):
    # creation tests
    def test_eq(self):
        node = HTMLNode("test 1","test 2", ["item 1", "item 2"], {"key": "value", "beep": "boop"})
        node2 = HTMLNode("test 1","test 2", ["item 1", "item 2"], {"key": "value", "beep": "boop"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_not_eq(self):
        node = HTMLNode("test 1","test 2", ["item 1", "item 2"], {"key": "value", "beep": "boop"})
        node2 = HTMLNode("test 1", ["item 1", "item 2"], {"key": "value", "beep": "boop"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

    def test_props_to_html(self):
        node = HTMLNode("test 1","test 2", ["item 1", "item 2"], {"key": "value", "beep": "boop"})
        expected_result = ' key="value" beep="boop"'
        self.assertEqual(node.props_to_html(), expected_result)

    # leafNode tests

    def test_eq(self):
        
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), node2.to_html())

    def test_noteq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertNotEqual(node.to_html(), node2.to_html())

    def test_value_exception(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None)
            node.to_html()

    def test_tag_none(self):
        text = "This is a paragraph of text."
        node = LeafNode(tag=None, value=text)
        self.assertEqual(node.to_html(), text)
        
    # parentNode tests

    def test_eq(self):

        child1 = LeafNode("span", "first text")
        child2 = LeafNode("span", "second text")
        node = ParentNode("p", [child1, child2])
        node2 = ParentNode("p", [child1, child2])
        self.assertEqual(node.to_html(), node2.to_html())

    def test_noteq(self):

        child1 = LeafNode("span", "first text")
        child2 = LeafNode("span", "second text")
        child3 = LeafNode("span", "third text")
        node = ParentNode("p", [child1, child2])
        node2 = ParentNode("p", [child1, child2, child3])
        self.assertNotEqual(node.to_html(), node2.to_html())

    def test_tag_empty(self):
        with self.assertRaises(ValueError):
            child1 = LeafNode("span", "first text")
            child2 = LeafNode("span", "second text")
            node = ParentNode(None, [child1, child2])
            node.to_html()

    def test_children_empty(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p",[])
            node.to_html()

    def test_children_None(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

    def test_nested_parents_one(self):
        
        child_of_inner = LeafNode("span", "inner text")
        inner_parent = ParentNode("div", [child_of_inner])
        outer_parent = ParentNode("section", [inner_parent])
        self.assertEqual(outer_parent.to_html(), "<section><div><span>inner text</span></div></section>")

    def test_nested_parents_multiple(self):

        child1 = LeafNode("span", "first text")
        child2 = LeafNode("span", "second text")
        child3 = LeafNode("span", "third text")
        child4 = LeafNode("span", "fourth text")

        inner_inner_parent = ParentNode("p", [child4])
        inner_parent_with_inner_parent = ParentNode("div", [inner_inner_parent, child1])
        inner_parent = ParentNode("div", [child2, child3])
        outer_parent = ParentNode("section", [inner_parent, inner_parent_with_inner_parent])
        self.assertEqual(outer_parent.to_html(), "<section><div><span>second text</span><span>third text</span></div><div><p><span>fourth text</span></p><span>first text</span></div></section>")

    def test_parent_with_props(self):

        child1 = LeafNode("span", "first text")
        child2 = LeafNode("span", "second text")
        node = ParentNode("p", [child1, child2], {"beep": "boop"})
        self.assertEqual(node.to_html(), '<p beep="boop"><span>first text</span><span>second text</span></p>')

    # text_node_to_html tests

    def test_TEXT(self):
        node = TextNode("text", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.to_html(), "text")

    def test_BOLD(self):
        node = TextNode("text", TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.to_html(), "<b>text</b>")

    def test_ITALIC(self):
        node = TextNode("text", TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.to_html(), "<i>text</i>")

    def test_CODE(self):
        node = TextNode("text", TextType.CODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.to_html(), "<code>text</code>")

    def test_LINK(self):
        node = TextNode("text", TextType.LINK, "https://www.youtube.com/")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.youtube.com/">text</a>')

    def test_IMAGE(self):
        node = TextNode("text", TextType.IMAGE, "https://images.app.goo.gl/3V3iKJkuaGpvJ4xp8")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.to_html(), '<img src="https://images.app.goo.gl/3V3iKJkuaGpvJ4xp8" alt="text"/>')

    def test_exception(self):
        with self.assertRaises(Exception):
            node = TextNode("text", TextType.ENLARGE)

