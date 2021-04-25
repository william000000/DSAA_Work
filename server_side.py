"""
My Server
"""
import sys
import socket
import student_controller

HOST = '127.0.0.1'
PORT = 65432
PART_SEPARATOR = ';'

try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, address = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    student_class = student_controller.StudentOperation()
                    data = data.decode().split(PART_SEPARATOR)
                    file_name = data[1].strip()
                    user_id = data[2].strip()
                    student_data = data[0].strip()

                    add_student_format = student_class.add_to_final_list(file_name,
                                                                         user_id, student_data)
                    HAS_PASSED = True
                    if not add_student_format:
                        MESSAGE = "Something went wrong!"
                        conn.sendall(MESSAGE.encode())
                        HAS_PASSED = False
                    if HAS_PASSED:
                        MESSAGE = "The User has been added successfully!"
                        conn.sendall(MESSAGE.encode())

except FileNotFoundError:
    pass
except socket.error as err:
    print('Server error:', err)
    sys.exit(1)
