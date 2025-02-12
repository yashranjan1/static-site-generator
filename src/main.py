from textnode import TextNode, TextType

def main():
    new_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(new_node)
    
if __name__ == "__main__":
    main()
