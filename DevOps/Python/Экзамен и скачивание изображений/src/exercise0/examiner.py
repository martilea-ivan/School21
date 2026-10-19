import time
import random
from student import Student
from question import Question


class Examiner:
    def __init__(self, name: str, gender: str):
        self.name = name
        self.gender = gender
        self.current_student = None
        self.total_students = 0
        self.failed_students = 0
        self.work_time = 0.0
        self.has_lunched = False

    def get_mood(self, correct_count: int) -> bool:
        mood = random.choices(
            ["bad", "neutral", "good"],
            weights=[1/8, 5/8, 1/4],
            k=1
        )[0]

        if mood == "bad":
            return False
        elif mood == "good":
            return True
        else:
            wrong = 3 - correct_count
            return correct_count > wrong

    def conduct_exam(self, student: Student, questions: list) -> bool:
        self.total_students += 1

        exam_duration = random.uniform(len(self.name) - 1, len(self.name) + 1)
        time.sleep(exam_duration)

        self.work_time += exam_duration
        student.exam_time = exam_duration
        student.examiner_name = self.name

        selected = random.sample(questions, min(3, len(questions)))
        correct_count = 0

        for question in selected:
            student_word = question.student_answer(student.gender)
            examiner_words = question.examiner_answers()

            if student_word in examiner_words:
                correct_count += 1
                question.correct_count += 1

        student.correct_answers = correct_count

        passed = self.get_mood(correct_count)

        if not passed:
            self.failed_students += 1
            student.status = "Провалил"
        else:
            student.status = "Сдал"

        return passed

    def get_state(self):
        return {
            'name': self.name,
            'gender': self.gender,
            'total_students': self.total_students,
            'failed_students': self.failed_students,
            'work_time': self.work_time,
            'has_lunched': self.has_lunched
        }

    def __repr__(self):
        return f"Examiner({self.name}, students={self.total_students})"