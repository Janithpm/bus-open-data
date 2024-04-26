import ast

namespaces = {
    'siri': 'http://www.siri.org.uk/siri'
}

def compare(tag, other):
    return tag == '{%s}%s' % (namespaces['siri'], other)

def getName(ele):
    return ele.tag.split('}')[-1]

def getText(ele):
    return ele.text

def find(root, tag):
    return root.find('siri:' + tag, namespaces)

def findall(root, tag):
    return root.findall('siri:' + tag, namespaces)

def typeCast(text):
    try:
        return ast.literal_eval(text)
    except (SyntaxError, ValueError):
        return text