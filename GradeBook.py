from typing import IO, Tuple, List, Dict

ADDCOURSE = ["1", "a", "add"]
REMOVECOURSE = ["2", "r", "remove"]
MODIFYCOURSE = ["3", "m", "modify"]
VIEWCOURSE = ["4", "v", "view"]
VIEWCOURSES = ["5", "c", "courses"]
SAVE = ["6", "s", "save"]
QUIT = ["7","q", "quit"]

LINE = "\n────────────────────────────────────\n"


class Assignment:
    def __init__(self, assignment_name: str,
                 weight: int,
                 grade: int):
        """
        creates an assignment object
        """
        self.assignment_name = assignment_name
        self.weight = weight
        self.grade = grade

    def __str__(self) -> str:
        """
        returns a string representation of the assignment
        """
        return f"Assignment Name: {self.assignment_name}\nWeight: {self.weight}\nGrade: {self.grade}"


class Course:
    def __init__(self, course_name: str, assignments_dict: dict[str, Assignment]):
        """
        creates a course object
        """
        self.course_name = course_name
        self.assignments_dict = assignments_dict

    def __str__(self) -> str:
        """
        returns a string representation of the course
        """
        return f"Course Name: {self.course_name}\n {self.get_assignments_print_string()} \nFinal Grade: {self.get_final_grade()}\nLetter Grade: {self.letter_grade()}"

    def remove_assignment(self, assignment_name: str) -> None:
        """
        removes an assignment from the assignments dictionary
        """
        self.assignments_dict.pop(assignment_name)

    def print_assignments(self) -> None:
        """
        prints all the assignments in the assignments dictionary
        """
        print("\nAssignments:")
        print("─────────")
        ## loop through every assignment and print it
        for assignment in self.assignments_dict.values():
            print("•", assignment.assignment_name)

    def get_assignments_print_string(self) -> str:
        """
        returns a string of all the assignments in the assignments dictionary
        """
        assignments_string = ""
        assignments_string += "Assignments:\n"
        assignments_string += "─────────"
        ## loop through every assignment and add it to the string
        for assignment in self.assignments_dict.values():
            assignments_string += f"\n• {assignment.assignment_name}"
        print(assignments_string)
        return assignments_string

    def get_final_grade(self) -> float:
        """
        returns the final grade
        """
        final_grade = 0
        ## loop through every assignment
        for assignment in self.assignments_dict.values():
            ## add the weighted grade to the final grade
            final_grade += assignment.weight * assignment.grade
        return final_grade / 100

    def letter_grade(self) -> str:
        """
        returns the letter grade
        """
        final_grade = self.get_final_grade()
        if final_grade >= 93:
            return "A"
        elif final_grade >= 90:
            return "A-"
        elif final_grade >= 87:
            return "B+"
        elif final_grade >= 83:
            return "B"
        elif final_grade >= 80:
            return "B-"
        elif final_grade >= 77:
            return "C+"
        elif final_grade >= 73:
            return "C"
        elif final_grade >= 70:
            return "C-"
        elif final_grade >= 67:
            return "D+"
        elif final_grade >= 63:
            return "D"
        elif final_grade >= 60:
            return "D-"
        else:
            return "F"

    def course_menu(self) -> None:
        """
        displays the course menu
        """
        print(LINE)
        print("Course Menu")
        print("1. Add an assignment")
        print("2. Edit an assignment")
        print("3. Remove an assignment")
        print("B. Back")
        print("Q. Quit")


def open_file() -> IO:
    """
    gets the file name from the user and returns the file pointer
    """
    file = None
    ## loop until file is opened
    while file is None:
        file_name = input("Enter a filename: ")
        try:
            file = open(file_name, "r")
        ## if the file cannot be opened
        except IOError:
            ## loop and try again
            print("Error in filename.")
    return file


def create_file() -> IO:
    """
    gets the file name from the user and returns the file pointer
    """
    file = None
    ## loop until file is created
    while file is None:
        file_name = input("Enter a filename: ")
        try:
            file = open(file_name, "w")
        ## if the file cannot be created
        except IOError:
            ## loop and try again
            print("Error in filename.")
    return file


def get_verify_weight() -> int:
    """
    gets the weight from the user and verifies it
    """
    weight = input("Enter the weight of the assignment: ")
    ## loop until the weight is valid
    while not weight.isnumeric() or int(weight) < 0 or int(weight) > 100:
        print("Invalid weight.")
        weight = input("Enter the weight of the assignment: ")
    return int(weight)


def get_verify_grade() -> int:
    """
    gets the grade from the user and verifies it
    """
    grade = input("Enter the grade of the assignment: ")
    ## loop until the grade is valid
    while not grade.isnumeric() or int(grade) < 0 or int(grade) > 100:
        print("Invalid grade.")
        grade = input("Enter the grade of the assignment: ")
    return int(grade)


def edit_assignment(course: Course) -> None:
    """
    allows the user to edit an assignment
    """
    ## print the assignments
    course.print_assignments()

    ## get the assignment name
    assignment_name = str(input("Enter the name of the assignment you want to edit: ")).strip()
    if assignment_name.lower() not in course.assignments_dict.keys():
        print("Assignment does not exist.")
        return

    name_or_weight = input("Do you want to edit the name or weight of the assignment? (N/W): ").strip()
    ## loop until the user enters a valid option
    while name_or_weight.lower() not in ["n", "w"]:
        print("Invalid option.")
        name_or_weight = input("Do you want to edit the name or weight of the assignment? (N/W): ")

    if name_or_weight.lower() == "n":
        ## edit the assignment name
        new_name = input("Enter the new name of the assignment: ")
        temp_assign = course.assignments_dict[assignment_name.lower()]
        temp_assign.assignment_name = new_name
        course.assignments_dict[new_name.lower()] = temp_assign
        print("Assignment edited successfully.")

    elif name_or_weight.lower() == "w":
        if assignment_name.lower() in course.assignments_dict.keys():

            weight = get_verify_weight()
            ## add up all weights and make sure they don't exceed 100
            total_weight = 0
            for assignment in course.assignments_dict.values():
                total_weight += assignment.weight

            ## if the total weight exceeds 100
            if total_weight + weight > 100:
                print("Total weight exceeds 100. Please try again.")
                return
            grade = get_verify_grade()

            ## edit the assignment
            course.assignments_dict[assignment_name.lower()] = Assignment(assignment_name, weight, grade)
            print("Assignment edited successfully.")
        else:
            print("Assignment not found.")


def remove_assignment(course: Course) -> None:
    """
    allows the user to remove an assignment
    """

    ## print the assignments
    course.print_assignments()

    assignment_name = str(input("Enter the name of the assignment you want to remove: ")).lower().strip()
    if assignment_name in course.assignments_dict.keys():
        ## remove the assignment
        course.remove_assignment(assignment_name)
        print("Assignment removed successfully.")
    else:
        print("Assignment not found.")


def add_assignment(course: Course) -> None:
    """
    allows the user to add an assignment
    """

    ## print the assignments
    print("\nAssignments:")
    print("─────────")
    ## if there are no assignments
    if len(course.assignments_dict) == 0:
        print("There are currently no assignments in this course.")
    ## if there are assignments
    for assignment in course.assignments_dict.values():
        print("•", assignment.assignment_name)

    assignment_name = str(input("Enter the name of the assignment you want to add: "))
    if assignment_name.lower() not in course.assignments_dict.keys():
        weight = get_verify_weight()
        ## add up all weights and make sure they don't exceed 100
        total_weight = 0
        for assignment in course.assignments_dict.values():
            total_weight += assignment.weight

        ## if the total weight exceeds 100
        if total_weight + weight > 100:
            print("Total weight exceeds 100. Please try again.")
            return
        grade = get_verify_grade()

        ## add the assignment
        course.assignments_dict[assignment_name.lower()] = Assignment(assignment_name, weight, grade)
        print("Assignment added successfully.")
    else:
        print("Assignment already exists.")


def add_course(course_dict: dict[str, Course]) -> None:
    """
    allows the user to add a course
    """
    course_name = str(input("Enter the name of the course you want to add: ")).strip()
    if course_name.lower() not in course_dict.keys():
        ## add the course
        course_dict[course_name.lower()] = Course(course_name, {})
        print("Course added successfully.")
    else:
        print("Course already exists.")


def edit_course(course_dict: dict[str, Course]) -> None:
    """
    allows the user to edit a course
    """
    course_name = str(input("Enter the name of the course you want to edit: ")).strip()
    if course_name.lower() in course_dict.keys():
        ## edit the course
        choice = input("Choose what you want to edit: \n1. Course name\n2. Assignments\nEnter your choice:")
        ## loop until the choice is valid
        while choice != "1" and choice != "2":
            print("Invalid choice.")
            choice = input("Choose what you want to edit: \n1. Course name\n2. Assignments\nEnter your choice:")
        ## if choice is name
        if choice == "1":
            new_name = str(input("Enter the new name of the course: ")).strip()
            course_dict[course_name.lower()].course_name = new_name
            course_dict[new_name.lower()] = course_dict.pop(course_name.lower())
            print("Course edited successfully.")
        ## if choice is assignments
        elif choice == "2":
            course_dict[course_name.lower()].course_menu()
            course_choice = input("Enter an action: ").upper()
            ## loop until the user wants to go back and not quit and check choice is valid
            while course_choice != "B" and course_choice != "Q" and course_choice != "1" and course_choice != "2" and course_choice != "3":
                print("Invalid choice.")
                course_dict[course_name].course_menu()
                course_choice = input("Enter an action: ").upper()
            ## loop until the user wants to go back and not quit
            while course_choice != "B" and course_choice != "Q":
                ## if choice is add assignment
                if course_choice == "1":
                    add_assignment(course_dict[course_name])
                ## if choice is edit assignment
                elif course_choice == "2":
                    if len(course_dict[course_name].assignments_dict) == 0:
                        print("No assignments to remove.")
                    else:
                        edit_assignment(course_dict[course_name])
                ## if choice is remove assignment
                elif course_choice == "3":
                    if len(course_dict[course_name].assignments_dict) == 0:
                        print("No assignments to remove.")
                    else:
                        remove_assignment(course_dict[course_name])
                course_dict[course_name.lower()].course_menu()
                course_choice = input("Enter an action: ").upper().strip()
                ## loop until the user wants to go back and not quit and check choice is valid
                while course_choice != "B" and course_choice != "Q" and course_choice != "1" and course_choice != "2" and course_choice != "3":
                    print("Invalid choice.")
                    course_dict[course_name].course_menu()
                    course_choice = input("Enter an action: ").upper().strip()
        print("Course edited successfully.")
    else:
        print("Course not found.")


def remove_course(course_dict: dict[str, Course]) -> None:
    """
    allows the user to remove a course
    """
    course_name = str(input("Enter the name of the course you want to remove: ")).lower().strip()
    if course_name in course_dict.keys():
        ## remove the course
        course_dict.pop(course_name)
        print("Course removed successfully.")
    else:
        print("Course not found.")


def view_course(course_dict: dict[str, Course]) -> None:
    """
    allows the user to view a course
    """
    course_name = str(input("Enter the name of the course you want to view: ")).lower().strip()
    if course_name in course_dict.keys():
        ## view the course
        print(course_dict[course_name])
    else:
        print("Course not found.")

def view_all_courses(course_dict: dict[str, Course]) -> None:
    """
    allows the user to view all courses
    """
    ## loop through all courses
    print("\nCourses:")
    print("─────────")
    if len(course_dict) == 0:
        print("There are currently no courses.")
    for course in course_dict.values():
        print("•",course.course_name)
def print_menu() -> None:
    """
    prints the menu
    """
    print(LINE)
    print("Main Menu:")
    print("1. Add a course")
    print("2. Remove a course")
    print("3. Modify a course")
    print("4. View a course")
    print("5. View all courses")
    print("S. Save")
    print("Q. Quit")


def select_action(course_dict: dict[str, Course]) -> str:
    """
    selects the action to perform
    """
    print_menu()
    action = input("Enter an action: ").strip()
    ## loop until the action is valid
    while action.lower() not in ADDCOURSE and action.lower() not in REMOVECOURSE and action.lower() not in MODIFYCOURSE and action.lower() not in VIEWCOURSE and action.lower() not in VIEWCOURSES and action.lower() not in QUIT and action.lower() not in SAVE:
        print("Invalid action.")
        action = input("Enter an action: ")
    ## if the action is edit
    if action.lower() in ADDCOURSE:
        add_course(course_dict)
    ## if the action is remove
    elif action.lower() in REMOVECOURSE:
        if(len(course_dict) == 0):
            print("No courses to remove.")
        else:
            remove_course(course_dict)
    ## if the action is add
    elif action.lower() in MODIFYCOURSE:
        edit_course(course_dict)
    ## if the action is view
    elif action.lower() in VIEWCOURSE:
        view_course(course_dict)
    ## if the action is view all courses
    elif action.lower() in VIEWCOURSES:
        view_all_courses(course_dict)
    elif action.lower() in SAVE:
        save_file(course_dict)
    ## if the action is quit
    elif action.lower() in QUIT:
        return "Quit"
    return "Continue"


def read_create_file() -> str:
    """
    reads or creates the file
    """
    read_create_file_choice = input(
        "Would you like to read from an existing file or create a new file? (Enter 'r' to read, "
        "'c' to create, 'q' to quit): ").lower().strip()
    ## loop until the input is valid
    while read_create_file_choice not in ["r", "read", "c", "create", "q", "quit"]:
        print("Invalid input.")
        read_create_file_choice = input(
            "Would you like to read from an existing file or create a new file? (Enter 'r' to read, "
            "'c' to create, 'q' to quit): ")
    return read_create_file_choice


def save_file(course_dict: dict[str, Course]) -> None:
    """
    saves the file
    """
    file_name = input("Enter a filename: ")
    file = open(file_name, "w")
    ## write the number of courses
    file.write(str(len(course_dict)) + "\n")
    ## loop through all courses
    for course in course_dict.values():
        file.write(course.course_name + "\n")
        ## write the number of assignments
        file.write(str(len(course.assignments_dict)) + "\n")
        ## loop through all assignments
        for assignment in course.assignments_dict.values():
            file.write(f"{assignment.assignment_name},{assignment.weight},{assignment.grade}\n")
    print("Saving...")
    file.close()


def initialisation() -> dict[str, Course]:
    """
    initialises the program
    """
    course_dict = {}

    ##check if read from existing file or new file
    read_create_file_choice = read_create_file()

    ## if the input is quit
    if read_create_file_choice == "q" or read_create_file_choice == "quit":
        input("Thanks for using the Gradebook Calculator!")
        ## exit the program
        exit()

    ## if the input is read
    elif read_create_file_choice == "r" or read_create_file_choice == "read":
        file = open_file()

        ## read the number of courses
        num_courses = int(file.readline())
        ## loop through the number of courses
        for i in range(num_courses):
            ## read the course name
            course_name = file.readline().strip().lower().strip()
            ## read the number of assignments
            num_assignments = int(file.readline())
            ## create the course
            course_dict[course_name] = Course(course_name, {})
            ## loop through the number of assignments
            for j in range(num_assignments):
                ## read the assignment name, weight, and grade
                assignment_name, weight, grade = file.readline().strip().split(",")
                ## create the assignment
                course_dict[course_name].assignments_dict[assignment_name] = Assignment(assignment_name, float(weight), float(grade))
        file.close()

    return course_dict


def main():
    """
    main function
    """
    print("Welcome to the Gradebook Calculator!")
    ## initialise the program
    course_dict = initialisation()

    action = "Continue"
    # while the action is not quit
    while action != "Quit":
        action = select_action(course_dict)

    ## if the input is quit
    input("Thanks for using the Gradebook Calculator!")


if __name__ == "__main__":
    main()
