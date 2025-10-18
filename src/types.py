from dataclasses import dataclass
from enum import Enum
from typing import List



@dataclass
class Student:
    name: str
    attendance: int
    scores: List[int]



class Report:
    def __init__(
        self,
        total_students: int,
        passed_count: int,
        failed_count: int,
        class_average: float,
        highest_score: int,
        lowest_score: int,
        average_attendance_rate: float
    ):
        self.total_students = total_students
        self.passed_count = passed_count
        self.failed_count = failed_count
        self.class_average = class_average
        self.highest_score = highest_score
        self.lowest_score = lowest_score
        self.average_attendance_rate = average_attendance_rate


class SubjectStatus(Enum):
    PASS = "Pass",
    FAIL = 'Fail'
    
    
student_dict_T = dict[str, Student]
report_dict_T = dict[Report]