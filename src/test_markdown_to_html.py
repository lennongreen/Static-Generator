import unittest
from markdown_to_html import *
from htmlnode import *

class TestMarkdowntoHTML(unittest.TestCase):
    # tests for text_to_tag
    def test_heading(self):
        test_string1 = "heading 1"
        test_string2 = "heading 3"
        test_string3 = "heading 6"
        result1 = "h1"
        result2 = "h3"
        result3 = "h6"
        self.assertEqual(text_to_tag(test_string1), result1)
        self.assertEqual(text_to_tag(test_string2), result2)
        self.assertEqual(text_to_tag(test_string3), result3)

    def test_paragraph(self):
        test_string = "paragraph"
        expected = "p"
        self.assertEqual(text_to_tag(test_string), expected)

    def test_code(self):
        test_string = "code"
        expected = "pre"
        self.assertEqual(text_to_tag(test_string, False), expected)

    def test_quote(self):
        test_string = "quote"
        expected = "blockquote"
        self.assertEqual(text_to_tag(test_string), expected)

    def test_unordered_list_parent(self):
        test_string = "unordered_list"
        expected = "ul"
        self.assertEqual(text_to_tag(test_string, False), expected)

    def test_unordered_list_child(self):
        test_string = "unordered_list"
        expected = "li"
        self.assertEqual(text_to_tag(test_string, True), expected)
        
    def test_ordered_list_parent(self):
        test_string = "ordered_list"
        expected = "ol"
        self.assertEqual(text_to_tag(test_string, False), expected)

    def test_ordered_list_child(self):
        test_string = "ordered_list"
        expected = "li"
        self.assertEqual(text_to_tag(test_string, True), expected)

    # testing create_child_list
        
    def test_ul(self):
        test_list = ["First Item", "Second Item", "Third Item"]
        expected = [

            ParentNode("li", "" ,[LeafNode(None, "First Item")]),
            ParentNode("li", "" , [LeafNode(None, "Second Item")]),
            ParentNode("li", "" ,[LeafNode(None, "Third Item")])

        ]
        self.assertEqual(create_child_list(test_list, "unordered_list"), expected)

    def test_ol(self):
        test_list = ["First Item", "Second Item", "Third Item", "Fourth Item"]
        expected = [

            ParentNode("li", "" ,[LeafNode(None, "First Item")]),
            ParentNode("li", "" , [LeafNode(None, "Second Item")]),
            ParentNode("li", "" ,[LeafNode(None, "Third Item")]),
            ParentNode("li", "" ,[LeafNode(None, "Fourth Item")])

        ]
        self.assertEqual(create_child_list(test_list, "ordered_list"), expected)

    def test_no_children(self):
        test_string = "First Item and only item"
        expected = [
             ParentNode("li", "" ,[LeafNode(None, "First Item and only item")]),
        ]
        self.assertEqual(create_child_list([test_string], "unordered_list"), expected)


    # test trim_blocks
    def test_trim_ul(self):
        test_tag = "ul"
        test_block = "* First Item\n- Second Item\n* Third Item"
        expected = "First Item\nSecond Item\nThird Item"
        self.assertEqual(trim_blocks(test_block, test_tag), expected)

    def test_trim_ol(self):
        test_tag = "ol"
        test_block = "1. First Item\n2. Second Item\n3. Third Item"
        expected = "First Item\nSecond Item\nThird Item"
        self.assertEqual(trim_blocks(test_block, test_tag), expected)

    def test_trim_heading(self):
        test_tag1 = "h1"
        test_tag2 = "h3"
        test_tag3 = "h6"
        test_block1 = "# Header"
        test_block2 = "### Header"
        test_block3 = "###### Header"
        expected = "Header"
        self.assertEqual(trim_blocks(test_block1, test_tag1), expected)
        self.assertEqual(trim_blocks(test_block2, test_tag2), expected)
        self.assertEqual(trim_blocks(test_block3, test_tag3), expected)

    def test_trim_quote(self):
        test_tag = "blockquote"
        test_block = "> Some quote"
        expected = "Some quote"
        self.assertEqual(trim_blocks(test_block, test_tag), expected)

    def test_trim_code(self):
        test_tag = "pre"
        test_block = "```Some Code```"
        expected = "Some Code"
        self.assertEqual(trim_blocks(test_block, test_tag), expected)

    def test_trim_paragraph(self):
        test_tag = "p"
        test_block = "Some words"
        expected = "Some words"
        self.assertEqual(trim_blocks(test_block, test_tag), expected)

    # testing markdown_to_html_node
    def test_eq(self):
        markdown = """

                # Heading 1

                Here's a paragraph with *italic* and **bold** text.

                > A blockquote with a line.

                - First item in an unordered list
                - Second item
                - Third item

        """
        expected = HTMLNode(

                "div",
                "",
                [
                    ParentNode("h1", "" , [LeafNode(None,"Heading 1")]),
                    ParentNode("p", "", [

                            LeafNode( None,"Here's a paragraph with "),
                            LeafNode("i" , "italic"),
                            LeafNode( None," and "),
                            LeafNode("b","bold"),
                            LeafNode( None," text.")
                    
                    ]
                    ),
                    ParentNode("blockquote", "" , [LeafNode(None,"A blockquote with a line.")]),
                    ParentNode(

                        "ul",
                        "",
                        [
                            ParentNode("li", "" , [LeafNode(None,"First item in an unordered list")]),
                            ParentNode("li", "" , [LeafNode(None,"Second item")]),
                            ParentNode("li", "" , [LeafNode(None,"Third item")])
                        ]
                    )
                ],
            )
        
        testing_html = markdown_to_html_node(markdown) 
        # tag test
        self.assertEqual(testing_html.tag, expected.tag)
        # value test
        self.assertEqual(testing_html.value,  expected.value)
        # children test
        self.assertEqual(testing_html.children,  expected.children)

    
        

if __name__ == "__main__":
    unittest.main()