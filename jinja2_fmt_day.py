import re

def format_jinja2_html(file_path):
    formatted_lines = []
    indent_level = 0
    indent_size = 4  # You can adjust this to your preferred indentation size

    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()

            # Decrease indent for end tags and Jinja2 end blocks
            if re.match(r'({% end\w+ %}|</\w+>)', stripped_line):
                indent_level = max(0, indent_level - 1)

            # Apply indentation
            formatted_lines.append(' ' * (indent_size * indent_level) + stripped_line)

            # Increase indent for start tags and Jinja2 blocks
            if re.match(r'(<\w+(?!/).*?>|{% \w+ %})', stripped_line) and not stripped_line.endswith('/>'):
                indent_level += 1

    # Write the formatted content to a new file
    #with open('formatted_' + file_path, 'w') as file:
    #    file.write('\n'.join(formatted_lines))
    print(f"{formatted_lines}")

# Usage
format_jinja2_html('path_to_your_jinja2_html_file.html')
