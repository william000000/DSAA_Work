import student_controller, serializer
import sys
import socket

HOST = '127.0.0.1'
PORT = 65432
DEFAULT_FILE_NAME = "students.txt"
FILE_NAME = "final_student"

if __name__ == "__main__":
    trials = 2
    student_class = student_controller.StudentOperation()

    # Load Student Data 
    student_data = student_class.load_students(DEFAULT_FILE_NAME)

    user_input_id = input("Enter ID number: ")

    # Check whether the entered ID is valid
    if not student_class.is_valid_id(user_input_id):
        print("The student id is not valid")
        sys.exit(1)
    
    student_password = input("Please enter a valid password: ")

    # Check if the password is valid 
    is_password_valid = student_class.is_password_valid(student_password)

    # Give a student three more chances to try a correct password
    while not is_password_valid and trials >= 0:
        student_password = input("Please enter a valid password, Please Try again: ")
        is_password_valid = student_class.is_password_valid(student_password)
        trials -= 1
    
    if not is_password_valid:
        print("You have exhausted your password trials, Please try again!")
        sys.exit(1)

    # Get Student and update him/her with a valid password 
    student_final_data = student_class.get_user(user_input_id)
    student_final_data = f'{student_final_data},password:{student_password}\n'

    # Add Updated Student to final_student.txt file
    is_student_added = student_class.add_to_final_list(f'{FILE_NAME}.txt', user_input_id, student_final_data)

    # Print Success Message when Student has been created
    if is_student_added:
        print("User has been updated successfully!")
    extension_type = input("Which format do you want to save your data in? : ")
    extension_type = extension_type.upper()
    loaded_user = student_class.load_students(f'{FILE_NAME}.txt')

    # Get student data values
    data = student_final_data.strip().split(',')
    user_id = data[0].split(',')[0].split(':')[1]
    last_name = data[1].split(',')[0].split(':')[1]
    first_name = data[2].split(',')[0].split(':')[1]
    password = data[3].split(',')[0].split(':')[1]

    # Serialize Student Data and Convert to any format entered by a user
    student = serializer.Student(user_id, first_name, last_name, password)
    serializers = serializer.ObjectSerializer()
    transformed_data = serializers.serialize(student, extension_type)
    add_student_format = student_class.add_to_final_list(f'{FILE_NAME}.{extension_type.lower()}', user_input_id, transformed_data)

    # When Server is on, it will send student data to our server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    
        s.connect((HOST, PORT))
        s.sendall(transformed_data.encode())
        transformed_data = s.recv(1024)
    print('Received data', repr(transformed_data))




    
