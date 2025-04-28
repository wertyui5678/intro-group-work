import csv
from tabulate import tabulate

class Student:
    def __init__(self, student_id, name, student_type):
        self.__student_id = student_id
        self.__student_name = name
        self.__student_type = student_type
        self.__enrolled_courses = []

    @property
    def student_id(self):
        return self.__student_id

    @property
    def student_name(self):
        return self.__student_name

    @property
    def student_type(self):
        return self.__student_type

    @property
    def enrolled_courses(self):
        return self.__enrolled_courses

    def can_enroll(self):
        return len(self.__enrolled_courses) < 4

    def add_course(self, course_name):
        if course_name not in self.__enrolled_courses:
            self.__enrolled_courses.append(course_name)

    def drop_course(self, course_name):
        if course_name in self.__enrolled_courses:
            self.__enrolled_courses.remove(course_name)

    def __str__(self):
        return f"{self.__student_name} (ID: {self.__student_id}, Type: {self.__student_type})"


class Course:
    def __init__(self, course_code, name, max_capacity):
        self.__course_code = course_code
        self.__course_name = name
        self.__max_capacity = int(max_capacity)
        self.__enrolled_students = []

    @property
    def course_code(self):
        return self.__course_code

    @property
    def course_name(self):
        return self.__course_name

    @property
    def max_capacity(self):
        return self.__max_capacity

    @property
    def enrolled_students(self):
        return self.__enrolled_students

    def add_student(self, student):
        if len(self.__enrolled_students) >= self.__max_capacity:
            return False
        if student in self.__enrolled_students:
            return False
        self.__enrolled_students.append(student)
        return True

    def drop_student(self, student):
        if student in self.__enrolled_students:
            self.__enrolled_students.remove(student)
            return True
        return False

    def __str__(self):
        return f"{self.__course_name} (Code: {self.__course_code}, Enrolled: {len(self.__enrolled_students)}/{self.__max_capacity})"


class Advisor:
    def __init__(self, name):
        self.__advisor_name = name
        self.__assigned_students = []
        self.__pending_requests = []

    @property
    def advisor_name(self):
        return self.__advisor_name

    @property
    def assigned_students(self):
        return self.__assigned_students

    @property
    def pending_requests(self):
        return self.__pending_requests

    def add_assigned_student(self, student):
        if len(self.__assigned_students) < 3:
            self.__assigned_students.append(student)

    def add_request(self, student, course):
        self.__pending_requests.append((student, course))

    def approve_request(self, student, course):
        if (student, course) in self.__pending_requests:
            self.__pending_requests.remove((student, course))
            return True
        return False

    def deny_request(self, student, course):
        if (student, course) in self.__pending_requests:
            self.__pending_requests.remove((student, course))
            return True
        return False

    def __str__(self):
        return self.__advisor_name


def load_students(file_name):
    students = []
    with open(file_name, 'r') as student_file:
        csv_reader = csv.reader(student_file)
        next(csv_reader)
        for row in csv_reader:
            students.append(Student(row[0], row[1], row[2]))
    return students


def load_courses(file_name):
    courses = []
    with open(file_name, 'r') as course_file:
        csv_reader = csv.reader(course_file)
        next(csv_reader)
        for row in csv_reader:
            courses.append(Course(row[0], row[1], row[2]))
    return courses


def load_advisors(file_name, students):
    advisors = []
    with open(file_name, 'r') as advisor_file:
        csv_reader = csv.reader(advisor_file)
        next(csv_reader)
        for row in csv_reader:
            advisor = Advisor(row[0])
            for student_id in row[1:]:
                for student in students:
                    if student.student_id == student_id:
                        advisor.add_assigned_student(student)
            advisors.append(advisor)
    return advisors


def get_student(students, name):
    for student in students:
        if student.student_name.lower() == name.lower():
            return student
    return None


def get_course(courses, name):
    for course in courses:
        if course.course_name.lower() == name.lower():
            return course
    return None


def get_advisor(student, advisors):
    for advisor in advisors:
        if student in advisor.assigned_students:
            return advisor
    return None


def enrol_student(students, courses, advisors):
    while True:
        course_name = input("Enter the name of the course: ").strip()
        course = get_course(courses, course_name)
        if course:
            break
        print(f'"{course_name}" not found. Try again.')

    while True:
        student_name = input("Enter the name of the student: ").strip()
        student = get_student(students, student_name)
        if student:
            break
        print(f'"{student_name}" not found. Try again.')

    if course.course_name in student.enrolled_courses:
        print(f"Student {student.student_name} is already enrolled in {course.course_name}.")
        print(f'Failure! Student "{student.student_name}" NOT enrolled in course "{course.course_name}".')
        return

    if not student.can_enroll():
        print(f"Student {student.student_name} cannot enroll in more than 4 courses.")
        return

    if student.student_type.lower() == "postgraduate":
        advisor = get_advisor(student, advisors)
        if advisor:
            advisor.add_request(student, course)
            print(f"Request sent to advisor {advisor.advisor_name} for approval.")
        else:
            print(f"No advisor found for {student.student_name}.")
    else:
        if course.add_student(student):
            student.add_course(course.course_name)
            print(f'Success! Student "{student.student_name}" enrolled in course "{course.course_name}".')
        else:
            print(f"Failure! Student \"{student.student_name}\" NOT enrolled in course \"{course.course_name}\".")


def drop_course(students, courses):
    while True:
        course_name = input("Enter the name of the course to drop: ").strip()
        course = get_course(courses, course_name)
        if course:
            break
        print(f'"{course_name}" not found. Try again.')

    while True:
        student_name = input("Enter the name of the student: ").strip()
        student = get_student(students, student_name)
        if student:
            break
        print(f'"{student_name}" not found. Try again.')

    if course.course_name not in student.enrolled_courses:
        print(f'Failure! Student "{student.student_name}" NOT enrolled in "{course.course_name}".')
        return

    if course.drop_student(student):
        student.drop_course(course.course_name)
        print(f'Success! Student "{student.student_name}" dropped from course "{course.course_name}".')
    else:
        print(f'Failure! Student "{student.student_name}" NOT dropped from course "{course.course_name}".')


def list_enrolled(courses):
    course_name = input("Enter the name of the course: ").strip()
    course = get_course(courses, course_name)
    if course:
        print(f"{course.course_name} (Code: {course.course_code}, Enrolled: {len(course.enrolled_students)}/{course.max_capacity})")
        if not course.enrolled_students:
            print("  None")
        else:
            for student in course.enrolled_students:
                print(f"  {student}")
    else:
        print(f'"{course_name}" not found.')


def list_all_courses(courses):
    table = []
    for course in courses:
        names = ", ".join([student.student_name for student in course.enrolled_students]) or "None"
        table.append([
            course.course_code,
            course.course_name,
            course.max_capacity,
            len(course.enrolled_students),
            names
        ])
    print(tabulate(table, headers=["Course Code", "Course Name", "Max Capacity", "Enrolled Students", "Student Names"],
                   tablefmt="grid"))


# ✅ FINAL CORRECT advisor_menu
def advisor_menu(advisors, students, courses):
    advisor_name = input("Enter your name: ").strip()
    advisor = None
    for a in advisors:
        if a.advisor_name.lower() == advisor_name.lower():
            advisor = a
            break

    if not advisor:
        print(f"No advisor found with the name {advisor_name}.")
        return

    if not advisor.pending_requests:
        print("No pending requests.")
        return

    print(f"Welcome, {advisor.advisor_name}. Here are your pending requests:")
    for i, (student, course) in enumerate(advisor.pending_requests, 1):
        print(f"{i}. Student {student.student_name} requests to enroll in {course.course_name}.")

    while advisor.pending_requests:
        action = input("Would you like to approve or deny a request? (a = approve, d = deny, q = quit): ").lower()
        if action == "q":
            print("Exiting advisor menu.")
            break
        elif action not in ("a", "d"):
            print("Invalid option. Please enter 'a' to approve, 'd' to deny, or 'q' to quit.")
            continue

        try:
            num = int(input("Enter the number of the request to approve/deny: "))
            student, course = advisor.pending_requests[num-1]
        except (ValueError, IndexError):
            print("Invalid request number.")
            continue

        if action == "a":
            if course.add_student(student):
                student.add_course(course.course_name)
                advisor.approve_request(student, course)
                print(f"Request approved. {student.student_name} is now enrolled in {course.course_name}.")
        elif action == "d":
            advisor.deny_request(student, course)
            print(f"Request denied for {student.student_name}.")

        if not advisor.pending_requests:
            break


def main():
    students = load_students("students.csv")
    courses = load_courses("courses.csv")
    advisors = load_advisors("advisors.csv", students)
    print(f"Initialised {len(students)} students, {len(advisors)} advisors including {len(courses)} courses.")

    while True:
        print("\n===============================")
        print("Enter your choice:")
        print("1. Enroll Student.")
        print("2. Drop a Course.")
        print("3. Re-enroll in a Course.")
        print("4. List Enrolled Students.")
        print("5. List All Courses and Enrolled Students.")
        print("6. Advisor Login.")
        print("0. Quit.")
        print("===============================")
        choice = input()

        if choice == "1":
            enrol_student(students, courses, advisors)
        elif choice == "2":
            drop_course(students, courses)
        elif choice == "3":
            enrol_student(students, courses, advisors)
        elif choice == "4":
            list_enrolled(courses)
        elif choice == "5":
            list_all_courses(courses)
        elif choice == "6":
            advisor_menu(advisors, students, courses)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

