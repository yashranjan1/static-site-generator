import re
from typing import List, Tuple

from htmlnode import LeafNode
from textnode import TextNode, TextType


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

    alt_text_pattern = r"\!\[(.*?)\]\([\w:/.]*\)"
    link_pattern = r"\!\[[\s\w\d]*\]\((.*?)\)"

    alt_text_list = re.findall(alt_text_pattern, text)
    link_list = re.findall(link_pattern, text)

    return list(zip(alt_text_list, link_list))


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Takes text formatted in Markdown and extracts links from it and returns them in a list of tuples

    Args:
    `text: str` => a string of text formatted in markdown

    Returns:
    `List[Tuple[text, link]]`
    """

    text_pattern = r"(?<!!)\[(.*?)\]\([\w:/.]*\)"
    link_pattern = r"(?<!!)\[[\s\w\d]*\]\((.*?)\)"

    text_list = re.findall(text_pattern, text)
    link_list = re.findall(link_pattern, text)

    return list(zip(text_list, link_list))


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
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")

    blocks = filter(lambda block: len(block) != 0, blocks)

    blocks = list(map(lambda block: block.lstrip().rstrip(), blocks))

    return blocks


def block_to_block_type(input: str) -> str:
    input = input.lstrip().rstrip()

    heading_pattern = r"^#{1,6} .+$"
    code_pattern = r"^```[\s\S]*```$"
    block_pattern = r"^(>\s?.*(\n>\s?.*)*)$"
    ul_pattern = r"^(\*|-) .+(\n(\s{2,4}|\t)?(\*|-) .+)*"
    ol_pattern = r"^(\d+\.) .+(\n(\s{2,4}|\t)?\d+\. .+)*"

    match input:
        case input if re.fullmatch(heading_pattern, input):
            sections = input.split()
            return f"h{len(sections[0])}"
        case input if re.fullmatch(code_pattern, input):
            return "code"
        case input if re.fullmatch(block_pattern, input):
            return "block"
        case input if re.fullmatch(ul_pattern, input):
            return "ul"
        case input if re.fullmatch(ol_pattern, input):
            blocks = input.split("\n")
            for i in range(1, len(blocks) + 1):
                if blocks[i - 1][0] != str(i):
                    return "p"
            return "ol"
        case _:
            return "p"
