"""
Test for student functionalities
"""
import os
import unittest
import student_controller
student_class = student_controller.StudentOperation()
DEFAULT_FILE_NAME = "students.txt"
FILE_NAME = "test_final_student"


class TestStudentController(unittest.TestCase):
    """
    Test Student controller
    """
    def test_load_students(self):
        """
        Load student test
        :return:
        """
        student_data = student_class.load_students(DEFAULT_FILE_NAME)
        self.assertEqual(student_data, {'001': 'id:001,first_name:willy,last_name:Sugira',
                                        '002': 'id:002,first_name:willy,last_name:Sugira',
                                        '003': 'id:003,first_name:willy,last_name:Sugira'})

    def test_valid_id(self):
        """
        Test whether an id is valid or not
        :return:
        """
        valid_id = student_class.is_valid_id("002")
        self.assertTrue(valid_id)

        invalid_id = student_class.is_valid_id("fdmndfdng")
        self.assertFalse(invalid_id)

    def test_valid_password(self):
        """
        Test whether a password is valid or not
        :return:
        """
        valid_password = student_class.is_password_valid("Passwor11@@")
        self.assertTrue(valid_password)

        invalid_password = student_class.is_password_valid("aaassworsss")
        self.assertFalse(invalid_password)

    def test_is_student_added(self):
        """
        Test if a student has been added or not
        :return:
        """
        student_final_data = 'id:001,first_name:willy,last_name:Sugira,password:Jsnsn0000!'
        user_id = '001'

        added_student = student_class.add_to_final_list(f'{FILE_NAME}.txt',
                                                        user_id,
                                                        student_final_data)
        self.assertTrue(added_student)

        added_student = student_class.add_to_final_list(f'{FILE_NAME}.txt',
                                                        user_id,
                                                        student_final_data)
        self.assertFalse(added_student)

        self.addCleanup(os.remove, f'{FILE_NAME}.txt')


if __name__ == '__main__':
    unittest.main()
