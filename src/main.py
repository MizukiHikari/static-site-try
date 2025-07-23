from textnode import TextNode, TextType


def main():
    obj = TextNode("Hello, World!", TextType.BOLD, "http://example.com")
    print(obj)


if __name__ == "__main__":
    main()
