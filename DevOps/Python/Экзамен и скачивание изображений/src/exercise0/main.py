import time
from multiprocessing import Process, Queue
from student import Student
from question import Question
from examiner import Examiner
from utils import read_file_with_fallback, parse_person_data
from exam_process import run_examiner_simple
from display import display_status, display_final_results


def main():
    print("Загрузка данных...")

    examiners_raw = read_file_with_fallback('examiners.txt')
    students_raw = read_file_with_fallback('students.txt')
    questions_raw = read_file_with_fallback('questions.txt')

    examiners_data = parse_person_data(examiners_raw)
    students_data = parse_person_data(students_raw)

    examiners = [Examiner(name, gender) for name, gender in examiners_data]
    students = [Student(name, gender) for name, gender in students_data]
    questions = [Question(text) for text in questions_raw]

    print(f"Загружено: {len(examiners)} экзаменаторов, {len(students)} студентов, {len(questions)} вопросов")
    print("Начинаем экзамен...")
    print()

    student_queue = Queue()
    for s in students:
        student_queue.put(s)

    result_queue = Queue()
    processes = []
    start_time = time.time()

    for examiner in examiners:
        p = Process(
            target=run_examiner_simple,
            args=(examiner, student_queue, result_queue, questions, start_time)
        )
        p.start()
        processes.append(p)

    try:
        while any(p.is_alive() for p in processes) or not student_queue.empty() or not result_queue.empty():
            elapsed = time.time() - start_time
            queue_size = student_queue.qsize()

            while not result_queue.empty():
                msg = result_queue.get()
                msg_type = msg[0]

                if msg_type == 'result' or msg_type == 'exam_result':
                    _, name, student, examiner_obj, questions_obj = msg

                    if student:
                        for s in students:
                            if s.id == student.id:
                                s.status = student.status
                                s.exam_time = student.exam_time
                                s.correct_answers = student.correct_answers
                                s.examiner_name = student.examiner_name
                                break

                    if examiner_obj:
                        for ex in examiners:
                            if ex.name == name:
                                ex.total_students = examiner_obj.total_students
                                ex.failed_students = examiner_obj.failed_students
                                ex.work_time = examiner_obj.work_time
                                ex.has_lunched = examiner_obj.has_lunched
                                break

                    if questions_obj:
                        for i, q in enumerate(questions):
                            for q_obj in questions_obj:
                                if q.text == q_obj.text:
                                    q.correct_count = q_obj.correct_count
                                    break

                elif msg_type == 'finish' or msg_type == 'finished':
                    _, name, _, examiner_obj, questions_obj = msg
                    if examiner_obj:
                        for ex in examiners:
                            if ex.name == name:
                                ex.total_students = examiner_obj.total_students
                                ex.failed_students = examiner_obj.failed_students
                                ex.work_time = examiner_obj.work_time
                                ex.current_student = None
                                break

                    if questions_obj:
                        for i, q in enumerate(questions):
                            for q_obj in questions_obj:
                                if q.text == q_obj.text:
                                    q.correct_count = q_obj.correct_count
                                    break

                elif msg_type == 'start' or msg_type == 'exam_start':
                    _, name, student, _, _ = msg
                    for ex in examiners:
                        if ex.name == name:
                            ex.current_student = student
                            break

                elif msg_type == 'end' or msg_type == 'exam_end':
                    _, name, _, _, _ = msg
                    for ex in examiners:
                        if ex.name == name:
                            ex.current_student = None
                            break

                elif msg_type == 'lunch' or msg_type == 'lunch_start':
                    _, name, _, _, _ = msg
                    for ex in examiners:
                        if ex.name == name:
                            ex.current_student = "Обед"
                            break

                elif msg_type == 'lunch_end':
                    _, name, _, _, _ = msg
                    for ex in examiners:
                        if ex.name == name:
                            ex.current_student = None
                            break

            display_status(students, examiners, queue_size, len(students), elapsed)
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nЭкзамен прерван пользователем.")

    for p in processes:
        p.join()

    elapsed = time.time() - start_time
    display_final_results(students, examiners, questions, elapsed)


if __name__ == "__main__":
    main()