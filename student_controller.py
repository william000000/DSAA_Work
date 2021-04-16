import re
import socket
import json

HOST = '127.0.0.1'
PORT = 65432
DATA_SEPARATOR=':'
LINE_SEPARATOR=','
PASSWORD_PATTERN = '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})'
students_json = []


class StudentOperation:
    def __init__(self):
        self.students = {}

    def load_students(self, file_name):
        try:
            with open(file_name, 'r') as s:
                datafile = s.readlines()

            for line in datafile:
                user_id = line.strip().split(LINE_SEPARATOR)[0]
                user_id = user_id.strip().split(DATA_SEPARATOR)[1].replace('"', '')
                line = line.strip().replace("\n", "")
                self.students.update({ user_id: line })

        except FileNotFoundError:
            pass
        return self.students


    def is_valid_id(self, user_id : str) -> bool:
        if self.students.get(user_id):
            return True
        return False

    def get_user(self, user_id):
        return self.students.get(user_id)


    def is_password_valid(self, password: str) -> bool:
        is_matched = re.search(PASSWORD_PATTERN, password)

        if not is_matched:
            return False
        return True
        

    def is_student_exist(self, file_name : str, student_id : str) -> bool:
        try:
            with open(file_name, 'r') as result_file:
                for record in result_file:
                    if record.startswith(f'id:{student_id}'):
                        print("Trueee")
                        return True
        except FileNotFoundError:
            pass
        return False

    def add_to_final_list(self, file_name: str, user_id: str, data: str) -> bool:

        if self.is_student_exist(file_name, user_id):
            return print("The User has already been updated in final_student.txt!")
            
        try:
            with open(file_name, 'a') as user_file:   
                user_file.write(data)

        except FileNotFoundError:
            pass 
        return True


