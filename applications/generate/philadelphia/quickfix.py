import xml.etree.ElementTree

from . import model


def read_messages(filename):
    def message(elem):
        name = elem.get('name')
        msgtype = elem.get('msgtype')
        return model.Message(name=name, msg_type=msgtype)
    root = xml.etree.ElementTree.parse(filename).find('messages')
    return [message(elem) for elem in root.findall('message')]


def read_fields(filename):
    def value(elem):
        enum = elem.get('enum')
        description = elem.get('description')
        return model.Value(name=description, value=enum)
    def field(root):
        number = root.get('number')
        name = root.get('name')
        type_ = _type(root)
        if name == 'MsgType' or not type_:
            values = []
        else:
            values = [value(elem) for elem in root.findall('value')]
        return model.Field(tag=number, name=name, type_=type_, values=values)
    root = xml.etree.ElementTree.parse(filename).find('fields')
    return sorted([field(elem) for elem in root.findall('field')],
            key=lambda field: int(field.tag))


_TYPES = {
    'CHAR': 'char',
    'INT': 'int',
    'MULTIPLECHARVALUE': 'char',
    'MULTIPLESTRINGVALUE': 'String',
    'NUMINGROUP': 'int',
    'STRING': 'String',
}


def _type(elem):
    type_ = elem.get('type')
    return _TYPES.get(type_)
