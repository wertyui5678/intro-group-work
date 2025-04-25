import csv

class Student:
    def __init__(self, student_id, name, student_type):
        self.name = name  
        self.student_id = student_id
        self.student_type = student_type

    def __str__(self):
        return f"{self.name} (Student id: {self.student_id}, Student type: {self.student_type})"

class Course:
    def __init__(self, course_code, name, max_capacity):
        self.name = name
        self.course_code = course_code
        self.max_capacity = int(max_capacity)
        self.enrolled = 0  
    def __str__(self):
        return f"{self.name} (Code: {self.course_code}, Enrolled: {self.enrolled}/{self.max_capacity})"


with open('students.csv', 'r') as student_file:
    csv_reader = csv.reader(student_file)
    next(csv_reader, None)  
    students = [Student(column[0], column[1], column[2]) for column in csv_reader]


with open('courses.csv', 'r') as course_file:
    csv_reader = csv.reader(course_file)
    next(csv_reader, None) 
    courses = [Course(column[0], column[1], column[2]) for column in csv_reader]

print("Students:")
for i in students:
    print(i)


print("\nCourses:")
for i in courses:
    print(i)


