"""
Serialize Student Data
"""
import sys
import json
import xml.etree.ElementTree as Et


class Student:
    """
    Student class with the following properties
    """
    def __init__(self, student_id, first_name, last_name, password):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def serialize(self, serializer):
        """
        Initialize the student properties
        :param serializer:
        :return:
        """
        serializer.start_object('student_id', self.student_id)
        serializer.add_property('first_name', self.first_name)
        serializer.add_property('last_name', self.last_name)
        serializer.add_property('password', self.password)


class JsonSerializer:
    """
    Json Serializer
    """
    def __init__(self):
        self._current_object = None

    def start_object(self, object_name, object_id):
        """
        Initiate an object
        :param object_name:
        :param object_id:
        :return:
        """
        self._current_object = {
            'id': object_id
        }

    def add_property(self, name, value):
        """
        Add property in the dictionary
        :param name:
        :param value:
        :return:
        """
        self._current_object[name] = value

    def to_str(self):
        """
        Return in the string
        :return:
        """
        return json.dumps(self._current_object, default=lambda o: o.__dict__)


class XmlSerializer:
    """
    XML Serializer
    """
    def __init__(self):
        self._element = None

    def start_object(self, object_name, object_id):
        """
        It initiates the id
        :param object_name:
        :param object_id:
        :return:
        """
        self._element = Et.Element(object_name, attrib={'id': object_id})

    def add_property(self, name, value):
        """
        It adds a value in the dictionary
        :param name:
        :param value:
        :return:
        """
        prop = Et.SubElement(self._element, name)
        prop.text = value

    def to_str(self):
        """
        Convert to String
        :return:
        """
        return Et.tostring(self._element, encoding='unicode')


class CsvSerializer:
    """
    CSV Serializer
    """
    def __init__(self):
        self._current_object = {}

    def start_object(self, object_name, object_id):
        """
        It initiates the id
        :param object_name:
        :param object_id:
        :return:
        """
        self._current_object = {
            'id': object_id
        }

    def add_property(self, name, value):
        """
        It adds a value in the dictionary
        :param name:
        :param value:
        :return:
        """
        self._current_object[name] = value

    def to_str(self):
        """
        Convert to String
        :return:
        """
        data = self._current_object.values()
        data = list(data)
        user_id = data[0]
        first_name = data[1]
        last_name = data[2]
        password = data[3]

        line = f'{user_id},{first_name},{last_name},{password}'
        return line


class SerializerFactory:
    """
    Our Factory for serializer
    """
    def __init__(self):
        self._creators = {}

    def register_format(self, format_input, creator):
        """
        Register a format
        :param format_input:
        :param creator:
        :return:
        """
        self._creators[format_input] = creator

    def get_serializer(self, format_input):
        """
        Get a format for serializer
        :param format_input:
        :return:
        """
        creator = self._creators.get(format_input)
        if not creator:
            print("Invalid format, Please try again later!")
            sys.exit(0)
        return creator()


factory = SerializerFactory()
factory.register_format('JSON', JsonSerializer)
factory.register_format('XML', XmlSerializer)
factory.register_format('CSV', CsvSerializer)


class ObjectSerializer:
    """
    Object Serializer
    """
    def __init__(self):
        self._obj = {}

    @staticmethod
    def serialize(serializable, format_input):
        """
        Make use of serializers
        :param serializable:
        :param format_input:
        :return:
        """
        serializer = factory.get_serializer(format_input)
        serializable.serialize(serializer)
        return serializer.to_str()
