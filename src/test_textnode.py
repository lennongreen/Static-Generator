import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("Testing 1", TextType.IMAGE)
        node2 = TextNode("Testing 1", TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Testing 1", TextType.IMAGE)
        node2 = TextNode("Testing 2", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    
if __name__ == "__main__":
    unittest.main()