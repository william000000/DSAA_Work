"""
Student Controller
"""
import re

VALUE_SEPARATOR = ':'
PART_SEPARATOR = ','
RESERVED_CHARACTER = ("=", "!", "+")
MIN_PASSWORD_LENGTH = 8


class StudentOperation:
    """
    Student Operation Class
    """
    def __init__(self):
        self.students = {}

    def load_students(self, file_name):
        """
        Load Student data
        :param file_name:
        :return:
        """
        try:
            with open(file_name, 'r') as stud_file:
                datafile = stud_file.readlines()

            for line in datafile:
                user_id = line.strip().split(PART_SEPARATOR)[0]
                user_id = user_id.strip().split(VALUE_SEPARATOR)[1].replace('"', '')
                line = line.strip().replace("\n", "")
                self.students.update({user_id: line})

        except FileNotFoundError:
            pass
        return self.students

    def is_valid_id(self, user_id: str) -> bool:
        """
        Check whether user_id is valid or not
        :param user_id:
        :return:
        """
        if self.students.get(user_id):
            return True
        return False

    def get_user(self, user_id):
        """
        Get Student Info
        :param user_id:
        :return:
        """
        return self.students.get(user_id)

    @staticmethod
    def is_password_valid(password: str) -> bool:
        """
        Check whether password is valid or not
        :param password:
        :return:
        """
        password_length = len(password)
        counter = 0
        check_character = 0
        regex = '^[0-9A-Za-z]+$'

        if password_length < MIN_PASSWORD_LENGTH:
            return False
        for char in password:
            if char in RESERVED_CHARACTER:
                return False
            if char.isalnum() or char == ' ':
                counter += 1
            elif not char.isalnum() and char != ' ':
                check_character += 1
                password = password.replace(char, '')
            password = password.replace(' ', '')
        if (counter + check_character) != password_length or (check_character == 0 or counter == 0):
            return False
        if re.search(regex, password):
            return True
        return False

    @staticmethod
    def is_data_exist(file_name: str, user_id: str) -> bool:
        """
        Check whether Student is already saved or not
        :param file_name:
        :param user_id:
        :return:
        """
        try:
            with open(file_name, 'r') as stud_file:
                for data in stud_file:
                    if re.search(user_id, data):
                        return True
        except FileNotFoundError:
            pass
        return False

    def add_to_final_list(self, file_name: str, user_id: str, data: str) -> bool:
        """
        Save a student in the specified file
        :param file_name:
        :param user_id:
        :param data:
        :return:
        """
        if self.is_data_exist(file_name, user_id):
            return print("The User has already been updated in final_student.txt!")
        try:
            with open(file_name, 'a') as user_file:
                user_file.write(f'{data}')

        except FileNotFoundError:
            pass
        return True
