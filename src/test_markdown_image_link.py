import unittest
from markdown_links import *

class TestExtraxtLinksImages(unittest.TestCase):
    # helper tests
    def test_image_eq(self):
        test_tuple = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(test_tuple, expected)

    def test_link_eq(self):
        test_tuple = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        expected =[ ("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(test_tuple, expected)

    def test_given_image(self):
        test_tuple = extract_markdown_links("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = []
        self.assertListEqual(test_tuple, expected)
        
    def test_given_link(self):
        test_tuple = extract_markdown_images("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        expected = []
        self.assertListEqual(test_tuple, expected)

    def test_given_examples(self):
        text1 = "[Back Home](/)"
        text2 = "[wiki here](https://example.com)"

        test1_tuple = extract_markdown_links(text1)
        test2_tuple = extract_markdown_links(text2)
        self.assertListEqual(test1_tuple, [("Back Home","/")])
        self.assertListEqual(test2_tuple, [("wiki here","https://example.com")])
       

    # splitting tests

    def test_image_eq(self):
        test_node = split_nodes_image([TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(test_node, expected)

    def test_link_eq(self):

        test_node = split_nodes_link([TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(test_node, expected)


    def test_missing_attributes_image(self):
        # image_alt
        with self.assertRaises(Exception):
            extract_markdown_images("This is text with a ![]()") 

        with self.assertRaises(Exception):
            extract_markdown_images("This is text with a ![rick roll]()")
        
    def test_missing_attributes_link(self):
        with self.assertRaises(Exception):
            extract_markdown_links("This is text with a link [](https://www.boot.dev)")

    def test_no_image(self):
        test_node = split_nodes_image([TextNode("This has nothing but text", TextType.TEXT)])
        expected = [
            TextNode("This has nothing but text", TextType.TEXT)
        ]
        self.assertListEqual(test_node, expected)

    def test_no_link(self):
        test_node = split_nodes_link([TextNode("This has nothing but text", TextType.TEXT)])
        expected = [
            TextNode("This has nothing but text", TextType.TEXT)
        ]
        self.assertListEqual(test_node, expected)
        
    def test_image_beginninng(self):
        test_node = split_nodes_image([TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and then some text", TextType.TEXT)])
        expected = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and then some text", TextType.TEXT),
        ]
        self.assertListEqual(test_node, expected)

    def test_link_beginninng(self):
        test_node = split_nodes_link([TextNode("[to boot dev](https://www.boot.dev) and then some text", TextType.TEXT)])
        expected = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and then some text", TextType.TEXT),
        ]
        self.assertListEqual(test_node, expected)

    def test_image_end(self):
        test_node = split_nodes_image([TextNode("some text then image ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)])
        expected = [
            TextNode("some text then image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertListEqual(test_node, expected)

    def test_link_end(self):
        test_node = split_nodes_link([TextNode("some text then image [to boot dev](https://www.boot.dev)", TextType.TEXT)])
        expected = [
            TextNode("some text then image ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertListEqual(test_node, expected)

    def test_invalid_image_markdown(self):
        test_node = split_nodes_image([TextNode("some text then image [rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)])
        expected = [
            TextNode("some text then image [rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT),
        ]
        self.assertListEqual(test_node, expected)

    def test_invalid_link_markdown(self):
        test_node = split_nodes_link([TextNode("some text then image ![to boot dev](https://www.boot.dev)", TextType.TEXT)])
        expected = [
            TextNode("some text then image ![to boot dev](https://www.boot.dev)", TextType.TEXT)
        ]
        self.assertListEqual(test_node, expected)

if __name__ == "__main__":
    unittest.main()