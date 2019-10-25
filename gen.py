import yaml



def open_tag(tag_name, attrs=None):
    if attrs != None:
        attr_string = " ".join("{}=\"{!s}\"".format(ak, av) for (ak, av) in attrs.items())

        return "<{} {}>".format(tag_name, attr_string)
    else:
        return "<{}>".format(tag_name)

def close_tag(tag_name):
    return "</{}>".format(tag_name)



def build_xml(data):
    xml = ""

    if isinstance(data, dict):
        xml += handle_dict(data)
    else:
        xml += handle_value(data)
    
    return xml


def handle_value(data):
    return data

def handle_dict(data):
    inner_xml = ""

    for (tag, value) in data.items():

        node_attrs = isinstance(data[tag], dict) and data[tag].get('attrs')

        if node_attrs:
            node_value = data[tag].get('value', '')

            inner_xml += open_tag(tag, attrs=node_attrs)
            inner_xml += node_value

            data[tag] = None
        else:
            inner_xml += open_tag(tag)
            inner_xml += build_xml(value)

        inner_xml += close_tag(tag)

    return inner_xml




with open('1125_ex.yml', 'r') as r_file:
    data = yaml.full_load(r_file)

    xml = build_xml(data)

    with open('fmt.xml', 'w+') as w_file:
        w_file.write(xml)




