import sys
import re


def format_jinja2_html(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    indent_level = 0
    indent_size = 4  # Adjust this to your preferred indentation size
    open_tags = []
    self_closing_tags = [
        "br",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "area",
        "base",
        "col",
        "command",
        "embed",
        "keygen",
        "param",
        "source",
        "track",
        "wbr",
    ]

    formatted_lines = []

    for line in lines:
        stripped_line = line.strip()

        # Check for Jinja2 blocks and HTML tags
        jinja_blocks = re.findall(r"{%.*?%}", stripped_line)
        html_tags = re.findall(r"<[^>]+>", stripped_line)

        # Process each Jinja2 block and HTML tag
        for tag in jinja_blocks + html_tags:
            if tag.startswith("{%") and "end" in tag:
                indent_level = max(indent_level - 1, 0)
            elif (
                tag.startswith("<")
                and tag[1:3] != "br"
                and not tag[1:].startswith(tuple(self_closing_tags))
                and not tag.endswith("/>")
            ):
                if tag.startswith("</"):
                    indent_level = max(indent_level - 1, 0)
                else:
                    open_tags.append(tag)

        # Apply indentation
        formatted_line = " " * (indent_size * indent_level) + stripped_line
        formatted_lines.append(formatted_line)

        # Adjust indentation for next line
        for tag in jinja_blocks + html_tags:
            if tag.startswith("{%") and "end" not in tag:
                indent_level += 1
            elif (
                tag.startswith("<")
                and tag[1:3] != "br"
                and not tag[1:].startswith(tuple(self_closing_tags))
                and not tag.endswith("/>")
                and not tag.startswith("</")
            ):
                indent_level += 1
            elif tag.startswith("</") and open_tags and tag == f"</{open_tags[-1][1:]}":
                open_tags.pop()
    print(formatted_lines)
    # Write the formatted content to a new file
    # with open('formatted_' + file_path, 'w') as file:
    #    for line in formatted_lines:
    #        file.write(line + '\n')


# Usage
format_jinja2_html(sys.argv[1])
