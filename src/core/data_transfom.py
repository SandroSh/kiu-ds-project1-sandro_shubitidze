from ..constants import SCORE_GRADES
from ..types import student_dict_T, SubjectStatus,  Report, FailingCase
from data import students


def calculate_average(scores: list[int]) -> float:
    """Calculate the arithmetic mean of a list of scores."""
    return sum(scores) / len(scores)


def assign_grade(average: float) -> str:
    """Convert a numerical average to letter grade based on SCORE_GRADES scale."""
    for grade, range in SCORE_GRADES.items():
        if average >= range[0] and average <= range[1]:
            return grade


def check_eligibility(student: dict) -> tuple[bool, str]:
    """Check if a student passes based on scores and attendance.
    Returns (passed, reason) tuple where reason explains any failure."""
    student_average = calculate_average(student["scores"])
    student_attendance = calculate_attandance_percantage(student["attendance"])
    status = True if student_average >= 60 and student_attendance >= 75 else False
    if not status:
        if student_average < 60 and student_attendance >= 75:
           return (status, f'{FailingCase.LOW_AVERAGE.value} ({round_two_decimals(student_average)}%)')
        elif student_average >= 60 and student_attendance < 75:
            return (status, f'{FailingCase.LOW_ATTENDANCE.value} ({round_two_decimals(student_attendance)}%)')
        else:
            return (status, f'{FailingCase.LOW_AVERAGE.value}({round_two_decimals(student_average)}) , {FailingCase.LOW_ATTENDANCE.value} ({round_two_decimals(student_attendance)}%)')

    return (status, SubjectStatus.PASS.value)


def find_top_performers(
    students: dict[student_dict_T], n: int
) -> list[tuple[str, float]]:
    """Find the top n performers based on average scores.
    Returns list of (name, average) tuples."""
    performance_data = []

    for student_id, student_data in students.items():
        avg = calculate_average(student_data["scores"])
        performance_data.append((student_data["name"], avg))

    performance_data.sort(key=lambda x: x[1])
    return performance_data[-n:]


def generate_report(students: dict[student_dict_T]) -> Report:
    """Generate a comprehensive report with class statistics and student performance metrics."""
    total_students = len(students)
    passed_count = sum(
        1 for eligibility in calculate_total_eligibility(students) if eligibility[0]
    )
    passed_rate = passed_count / total_students * 100
    failed_count = total_students - passed_count
    failed_rate = failed_count / total_students * 100
    class_average = calculate_total_average(students)
    highest_score, lowest_score = find_minmax(students)
    attendance_ratios = calculate_attendance_ratio(students)
    average_attendance_rate = sum(attendance_ratios) / total_students
    report = Report(
        students,
        total_students,
        passed_count,
        passed_rate,
        failed_count,
        failed_rate,
        class_average,
        highest_score,
        lowest_score,
        average_attendance_rate,
    )

    return report


def calculate_attandance_percantage(attandance: int, max_attandance=30) -> float:
    """Calculate attendance percentage based on attended days and maximum possible days."""
    return attandance / max_attandance * 100


def calculate_total_eligibility(
    students: dict[student_dict_T],
) -> list[tuple[bool, str]]:
    """Check eligibility status for all students.
    Returns list of (passed, reason) tuples."""
    total_eligibility = []
    for student_id, student_data in students.items():
        total_eligibility.append(check_eligibility(student_data))
    return total_eligibility


def calculate_total_average(students: dict[student_dict_T]) -> float:
    """Calculate the average score across all students in the class."""
    averages = []

    for student_id, student_data in students.items():
        averages.append(calculate_average(student_data["scores"]))
    return sum(averages) / len(averages)


def find_minmax(students: dict[student_dict_T]) -> tuple[int, int]:
    """Find highest and lowest scores across all students.
    Returns (max_score, min_score) tuple."""
    flattened_scores = []
    min_n = 100
    max_n = 0

    for student_id, student_data in students.items():
        flattened_scores.extend(student_data["scores"])

    for n in flattened_scores:
        if n < min_n:
            min_n = n
        if n > max_n:
            max_n = n

    return (max_n, min_n)


def calculate_attendance_ratio(students: dict[student_dict_T]) -> list[float]:
    """Calculate attendance ratios for all students.
    Returns list of attendance percentages."""
    total_attendance_ratio = []

    for student_id, student_data in students.items():
        total_attendance_ratio.append(
            calculate_attandance_percantage(student_data["attendance"])
        )

    return total_attendance_ratio


def round_two_decimals(x: float) -> float:
    """Round a float to 2 decimal places."""
    return round(x, 2)


def distribute_grades(
    students: dict[student_dict_T],
) -> dict[str, int]:
    """Count number of students achieving each letter grade.
    Returns dict mapping grades to counts."""
    distributed_grades = dict.fromkeys(SCORE_GRADES.keys(), 0)

    for student_id, student_data in students.items():
        s_grade = assign_grade(calculate_average(student_data["scores"]))
        if s_grade is not None:
            distributed_grades[s_grade] += 1

    return distributed_grades


def filter_failed_students(students: dict[student_dict_T]) -> list[dict[str, tuple[bool,str]]]:
    """Get list of students who failed with their failure reasons.
    Returns list of dicts with id, name, and failure reason."""
    failed_students = []

    for student_id, student_data in students.items():
        status = check_eligibility(student_data)
        is_failed = not status[0]
        if is_failed:
            failed_students.append({"id": student_id, "name": student_data["name"], "reason": status[1]})
    return failed_students


def print_report(report: Report):
    """Print formatted report showing class statistics, top performers, failures, and grade distribution."""
    PERFORMER_QUANTITY = 5
    students_data = report.students_data[0] if isinstance(report.students_data, tuple) else report.students_data
    top_5_performer_data = find_top_performers(students_data, PERFORMER_QUANTITY)
    grade_distribution_data = distribute_grades(students_data)
    failed_students_data = filter_failed_students(students_data)
    
    print("=== COURSE STATISTICS ===")

    print(f"Total Students: {report.total_students}")
    print(f"Passed: {report.passed_count} ({round_two_decimals(report.passed_rate)}%)")
    print(f"Failed: {report.failed_count} ({round_two_decimals(report.failed_rate)}%)")
    print(f"Class Average: {report.class_average}")
    print(f"Average Attendance Rate: {report.average_attendance_rate}%")

    print("\n")
    print("=== TOP 5 PERFORMERS ===")
    for index, (student, score) in enumerate(top_5_performer_data, 1):
        print(f"{index}. {student} - {score} ({assign_grade(score)})")

    print("\n")

    print("=== STUDENTS WHO FAILED ===")
    for student in failed_students_data:
        print(f"{student['id']} - {student['name']}: {student['reason']}")
    print("\n")

    print("=== GRADE DISTRIBUTION ===")
    for grade in grade_distribution_data.items():
        print(f"{grade[0]}: {grade[1]} students")


def main():
    """Entry point: generate and print a report for all students."""
    report = generate_report(students)
    print_report(report)


if __name__ == "__main__":
    main()
