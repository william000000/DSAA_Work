import json
import xml.etree.ElementTree as et

class Student:
    def __init__(self, student_id, first_name, last_name, password):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
    def serialize(self, serializer):
        serializer.start_object('student_id', self.student_id)
        serializer.add_property('first_name', self.first_name)
        serializer.add_property('last_name', self.last_name)
        serializer.add_property('password', self.password)

class JsonSerializer:
    def __init__(self):
        self._current_object = None
    def start_object(self, object_name, object_id):
        self._current_object = {
            'id': object_id
        }
    def add_property(self, name, value):
        self._current_object[name] = value

    def to_str(self):
        return json.dumps(self._current_object, indent = 4)

class XmlSerializer:
    def __init__(self):
        self._element = None

    def start_object(self, object_name, object_id):
        self._element = et.Element(object_name, attrib = {'id': object_id })
    def add_property(self, name, value):
        prop = et.SubElement(self._element, name)
        prop.text = value
    def to_str(self):
        return et.tostring(self._element, encoding = 'unicode')
    

class SerializerFactory:
    def __init__(self):
        self._creators = {}
    def register_format(self, format, creator):
        self._creators[format] = creator
    def get_serializer(self, format):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError("Invalid format, Please try again later!")
        return creator()


factory = SerializerFactory()
factory.register_format('JSON', JsonSerializer)
factory.register_format('XML', XmlSerializer)


class ObjectSerializer:
    def serialize(self, serializable, format):
        serializer = factory.get_serializer(format)
        print("serialer---", serializer)
        serializable.serialize(serializer)
        return serializer.to_str()