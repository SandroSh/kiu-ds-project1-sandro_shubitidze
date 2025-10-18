from ..constants import score_grade
from ..types import student_dict_T, SubjectStatus, report_dict_T, Report
from data import students


def calculate_average(scores: list[int]) -> float:
    return sum(scores) / len(scores)


def assign_grade(average: float) -> str:

    for grade, range in score_grade.items():
        if average >= range[0] and average <= range[1]:
            return grade


def check_eligibility(student_dict: student_dict_T) -> tuple[bool, str]:

    status = (
        True
        if calculate_average(student_dict[1].scores) >= 60
        and calculate_attandance_percantage(student_dict[1].attendance) >= 75
        else False
    )

    return (status, SubjectStatus.PASS if status else SubjectStatus.FAIL)


def find_top_performers(
    students: dict[student_dict_T], n: int
) -> list[tuple[str, float]]:

    performance_data = []

    for student in students:
        performance_data.append((student[0], calculate_average(student[2].scores)))

    performance_data.sort()

    return performance_data[-n:]


def generate_report(students: dict[student_dict_T]) -> Report:
    total_students = len(students)
    passed_count = sum(
        1 for eligibility in calculate_total_eligibility(students) if eligibility[0]
    )
    failed_count = total_students - passed_count
    class_average = calculate_total_average(students)
    highest_score, lowest_score = find_minmax(students)
    average_attendance_rate = sum(calculate_attendance_ratio) / total_students
    report = Report(
        total_students,
        passed_count,
        failed_count,
        class_average,
        highest_score,
        lowest_score,
        average_attendance_rate,
    )

    return report


def calculate_attandance_percantage(attandance: int, max_attandance=30) -> float:
    return attandance / max_attandance * 100


def calculate_total_eligibility(
    students: dict[student_dict_T],
) -> list[tuple[bool, str]]:
    total_eligibility = []
    for s in students:
        total_eligibility.append(check_eligibility(s[1].scores))
    return total_eligibility


def calculate_total_average(students: dict[student_dict_T]) -> float:
    averages = []

    for student in students:
        averages.append(calculate_average(student[1].scores))
    return sum(averages) / len(averages)


def find_minmax(students: dict[student_dict_T]) -> tuple[int, int]:
    flattened_scores = []
    min_n = 100
    max_n = 0

    for s in students:
        flattened_scores.extend(s[1].scores)

    for n in flattened_scores:
        if n < min_n:
            min_n = n
        elif n > max_n:
            max_n = n

    return (min, max)


def calculate_attendance_ratio(students: dict[student_dict_T]) -> list[float]:
    total_attendance_ratio = []

    for student in students:
        total_attendance_ratio.append(
            calculate_attandance_percantage(student[1].attendance)
        )

    return total_attendance_ratio

def round_two_decimals(x: float) -> float:
    return round(x, 2)

def main():
    report = generate_report(students)
    print("=== COURSE STATISTICS ===")
    print(f"Total Students: {report.total_students}")
    print(f"Passed: {report.passed_count}")
    print(f"Failed: {report.failed_count}")
    print(f"Class Average: {report.class_average}")
    print(f"Average Attendance Rate: {report.average_attendance_rate}%")
    print("\n")
    print("=== TOP 5 PERFORMERS ===")
    print(f"")
    print(f"\n")
    print("=== STUDENTS WHO FAILED ===")
    print(f"")
    print(f"\n")
    print("=== GRADE DISTRIBUTION ===")


if __name__ == "__main__":
    main()
