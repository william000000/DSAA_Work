"""
My Main App
"""
import sys
import socket
import student_controller
import serializer

HOST = '127.0.0.1'
PORT = 65432
DEFAULT_FILE_NAME = "students.txt"
FILE_NAME = "final_student"
VALUE_SEPARATOR = ':'
PART_SEPARATOR = ','

if __name__ == "__main__":
    TRIALS = 2
    student_class = student_controller.StudentOperation()

    # Load Student Data
    student_data = student_class.load_students(DEFAULT_FILE_NAME)
    user_input_id = input("Enter ID number: ")

    # Check whether the entered ID is valid
    if not student_class.is_valid_id(user_input_id):
        print("The student id is not valid")
        sys.exit(1)
    student_password = input("\nPlease enter a valid password: ")

    # Check if the password is valid
    IS_PASSWORD_VALID = student_class.is_password_valid(student_password)

    # Give student three more chances to try a correct password
    while not IS_PASSWORD_VALID and TRIALS >= 0:
        student_password = input("Please enter a valid password, Please Try again: ")
        IS_PASSWORD_VALID = student_class.is_password_valid(student_password)
        TRIALS -= 1
    if not IS_PASSWORD_VALID:
        print("You have exhausted your password trials, Please try again!")
        sys.exit(1)

    # Get student and update him/her with a valid password
    student_final_data = student_class.get_user(user_input_id)
    student_final_data = f'{student_final_data},password:{student_password}\n'

    # Add an updated student's data to final_student.txt file
    is_student_added = student_class.add_to_final_list(f'{FILE_NAME}.txt',
                                                       user_input_id, student_final_data)

    # Print success message when a student has been created
    if is_student_added:
        print("User has been updated successfully in final_student.txt!")
    is_other_format = input("\nWould you like to print it in any format "
                            "other than .txt? (yes/no): ")
    is_other_format = is_other_format.lower()
    if is_other_format not in ('yes', 'y'):
        sys.exit(0)

    extension_type = input("\nWhich format do you want to save your data in? : ")
    extension_type = extension_type.upper()
    loaded_user = student_class.load_students(f'{FILE_NAME}.txt')

    # Collect student data
    data = student_final_data.strip().split(',')
    user_id = data[0].split(PART_SEPARATOR)[0].split(VALUE_SEPARATOR)[1]
    last_name = data[1].split(PART_SEPARATOR)[0].split(VALUE_SEPARATOR)[1]
    first_name = data[2].split(PART_SEPARATOR)[0].split(VALUE_SEPARATOR)[1]
    password = data[3].split(PART_SEPARATOR)[0].split(VALUE_SEPARATOR)[1]

    # Check whether the student's data has already been serialized in that file or not
    IS_DATA_INSERTED = student_class.is_data_exist(f'{FILE_NAME}.{extension_type}', user_id)
    if IS_DATA_INSERTED:
        print("The data had already been inserted, No worries!")
        sys.exit(1)

    # Serialize Student Data and Convert to any format entered by a user
    student = serializer.Student(user_id, first_name, last_name, password)
    serializers = serializer.ObjectSerializer()
    serialized_data = serializers.serialize(student, extension_type)

    # When Server is on, it will send student data to our server
    try:
        file_name = f'{FILE_NAME}.{extension_type.lower()}'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(str.encode(f'{serialized_data};{file_name};{user_input_id}'))
            transformed_data = s.recv(1024)
        print('Received data', repr(transformed_data.decode()))
    except socket.error as server_error:
        print("Socket error: ", server_error)
