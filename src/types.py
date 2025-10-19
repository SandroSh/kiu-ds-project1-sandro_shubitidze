from dataclasses import dataclass
from enum import Enum
from typing import List



@dataclass
class Student:
    name: str
    attendance: int
    scores: List[int]

student_dict_T = dict[str, Student]

class Report:
    def __init__(
        self,
        students:dict[student_dict_T],
        total_students: int,
        passed_count: int,
        passed_rate:float,
        failed_count: int,
        failed_rate:float,
        class_average: float,
        highest_score: int,
        lowest_score: int,
        average_attendance_rate: float,
        
    ):
        self.students_data = students,
        self.total_students = total_students
        self.passed_count = passed_count
        self.passed_rate = passed_rate
        self.failed_count = failed_count
        self.failed_rate = failed_rate
        self.class_average = class_average
        self.highest_score = highest_score
        self.lowest_score = lowest_score
        self.average_attendance_rate = average_attendance_rate

report_dict_T = dict[Report]
class SubjectStatus(Enum):
    PASS = "Pass",
    FAIL = 'Fail'

class FailingCase(Enum):
    LOW_AVERAGE = "Low average"
    LOW_ATTENDANCE = "Insufficient attendance"
    
