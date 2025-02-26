import re
from typing import List, Tuple

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Takes a `TextNode` and converts it into an HTMLNode.

    Args:
    `text_node: TextNode` => a textnode that you want converted.

    Returns:
    `HTMLNode`
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url or ""})
        case TextType.IMAGE:
            return LeafNode(
                "img", "", {"src": text_node.url or "", "alt": text_node.text}
            )
        case _:
            raise Exception("invalid type")


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    """
    Takes a list of `TextNode`s and seperates them based on a defined delimiter

    Args:
    `old_nodes: List[TextNode]` => a list of nodes that you want seperated
    `delimiter: str` => a delimiter that you want to use for seperation
    `text_type: TextType` => the type of the text that isnt surrounded by the delimiter

    Returns:
    `List[TextNode]`
    """
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        node_text = node.text.split(delimiter)
        for i in range(len(node_text)):
            if len(node_text[i]) == 0:
                continue
            if i % 2 == 0:
                new_node = TextNode(node_text[i], node.text_type, node.url)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(node_text[i], text_type, node.url)
                new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Takes text formatted in Markdown and extracts images from it and returns them in a list of tuples

    Args:
    `text: str` => a string of text formatted in markdown

    Returns:
    `List[Tuple[alt_text, link_to_image]]`
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Takes text formatted in Markdown and extracts links from it and returns them in a list of tuples

    Args:
    `text: str` => a string of text formatted in markdown

    Returns:
    `List[Tuple[text, link]]`
    """

    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        node_text = node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0:
            new_nodes.append(node)
        else:
            sections = [node_text]
            for text, link in links:
                sub_sections = sections[-1].split(f"[{text}]({link})", 1)
                sections.pop()
                sections.extend(sub_sections)
            for index in range(len(sections)):
                section = sections[index]
                is_empty = not has_content(section)
                if not is_empty:
                    new_nodes.append(TextNode(section, node.text_type))
                if index != len(sections) - 1:
                    new_nodes.append(
                        TextNode(links[index][0], TextType.LINK, links[index][1])
                    )

    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        node_text = node.text
        images = extract_markdown_images(node_text)
        if len(images) == 0:
            new_nodes.append(node)
        else:
            sections = [node_text]
            for text, link in images:
                sub_sections = sections[-1].split(f"![{text}]({link})", 1)
                sections.pop()
                sections.extend(sub_sections)
            for index in range(len(sections)):
                section = sections[index]
                is_empty = not has_content(section)
                if not is_empty:
                    new_nodes.append(TextNode(section, node.text_type))
                if index != len(sections) - 1:
                    new_nodes.append(
                        TextNode(images[index][0], TextType.IMAGE, images[index][1])
                    )

    return new_nodes


def has_content(text: str) -> bool:
    return bool(text.strip())


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")

    blocks = filter(lambda block: len(block) != 0, blocks)

    blocks = list(map(lambda block: block.lstrip().rstrip(), blocks))

    return blocks


def block_to_block_type(block: str) -> str:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text: str) -> List[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
