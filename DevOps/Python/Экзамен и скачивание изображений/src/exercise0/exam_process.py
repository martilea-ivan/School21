import time
import random
from multiprocessing import Queue
from examiner import Examiner
from student import Student
from question import Question


def run_examiner_simple(
        examiner: Examiner,
        student_queue: Queue,
        result_queue: Queue,
        questions: list,
        start_time: float
):
    examiner_start = time.time()

    while not student_queue.empty():
        if not examiner.has_lunched and (time.time() - examiner_start) > 30:
            result_queue.put(('lunch', examiner.name, None, None, None))
            lunch_duration = random.uniform(12, 18)
            time.sleep(lunch_duration)
            examiner.has_lunched = True
            result_queue.put(('lunch_end', examiner.name, None, None, None))

        try:
            student = student_queue.get(timeout=1)
        except:
            continue

        examiner.current_student = student
        result_queue.put(('start', examiner.name, student, None, None))

        examiner.conduct_exam(student, questions)

        result_queue.put(('result', examiner.name, student, examiner, questions))

        examiner.current_student = None
        result_queue.put(('end', examiner.name, None, None, None))

    result_queue.put(('finish', examiner.name, None, examiner, questions))