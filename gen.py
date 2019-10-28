import yaml
import textwrap


def open_tag(tag_name, attrs=None):
    if attrs != None:
        attr_string = " ".join("{}=\"{!s}\"".format(ak, av) for (ak, av) in attrs.items())

        return "<{} {}>".format(tag_name, attr_string)
    else:
        return "<{}>".format(tag_name)

def close_tag(tag_name):
    return "</{}>".format(tag_name)

def add_indent(text, indent=1):
    return textwrap.indent(text=text, prefix=" " * 2 * indent)

def add_newline(text):
    return text + "\n"


def build_xml(data, indent=1):
    xml = ""

    if isinstance(data, dict):
        xml += handle_dict(data, indent)
    else:
        xml += handle_value(data)

    return xml


def handle_value(data):
    return data

def handle_dict(data, indent):
    inner_xml = ""

    for (tag, value) in data.items():

        node_attrs = isinstance(data[tag], dict) and data[tag].get('_attrs')

        if node_attrs:
            node_value = data[tag].get('_value', '')

            inner_xml += add_indent(open_tag(tag, attrs=node_attrs), indent=indent+1)
            inner_xml += node_value
            inner_xml += add_newline(close_tag(tag))

            data[tag] = None
        else:
            if isinstance(value, dict):
                inner_xml += add_newline(add_indent(open_tag(tag), indent=indent+1))
                inner_xml += build_xml(value, indent=indent+1)
                inner_xml += add_newline(add_indent(close_tag(tag), indent=indent+1))
            else:
                inner_xml += add_indent(open_tag(tag), indent=indent+1)
                inner_xml += build_xml(value, indent=indent+1)
                inner_xml += add_newline(close_tag(tag))

    return inner_xml




with open('1125_ex.yml', 'r') as r_file:
    data = yaml.full_load(r_file)

    xml = build_xml(data)

    with open('fmt.xml', 'w+') as w_file:
        w_file.write(xml)




