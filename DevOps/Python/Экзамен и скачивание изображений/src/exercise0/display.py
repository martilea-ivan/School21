from prettytable import PrettyTable
from utils import clear_screen


def get_unique_students(students):
    seen = set()
    unique = []
    for s in students:
        if s.id not in seen:
            seen.add(s.id)
            unique.append(s)
    return unique


def print_student_table(students: list):
    unique_students = get_unique_students(students)

    table = PrettyTable(["Студент", "Статус"])
    order = {"Очередь": 0, "Сдал": 1, "Провалил": 2}

    for student in sorted(unique_students, key=lambda s: order.get(s.status, 3)):
        table.add_row([student.name, student.status])

    print(table)


def print_examiner_table(examiners: list, detailed: bool = True):
    if detailed:
        headers = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы"]
        table = PrettyTable(headers)
        for ex in examiners:
            current = ex.current_student.name if ex.current_student and hasattr(ex.current_student, 'name') else "-"
            table.add_row([
                ex.name,
                current,
                ex.total_students,
                ex.failed_students,
                f"{ex.work_time:.2f}"
            ])
    else:
        headers = ["Экзаменатор", "Всего студентов", "Завалил", "Время работы"]
        table = PrettyTable(headers)
        for ex in examiners:
            table.add_row([
                ex.name,
                ex.total_students,
                ex.failed_students,
                f"{ex.work_time:.2f}"
            ])

    print(table)


def display_status(students, examiners, queue_size, total_students, elapsed):
    clear_screen()
    print(f"Время: {elapsed:.2f} сек\n")

    print_student_table(students)
    print()
    print_examiner_table(examiners, detailed=True)
    print()
    print(f"Осталось в очереди: {queue_size} из {total_students}")
    print(f"Время с момента начала экзамена: {elapsed:.2f}")


def display_final_results(students, examiners, questions, elapsed):
    clear_screen()
    print("=" * 60)
    print("  ИТОГИ ЭКЗАМЕНА")
    print("=" * 60)
    print()

    unique_students = get_unique_students(students)

    print_student_table(unique_students)
    print()
    print_examiner_table(examiners, detailed=False)
    print()

    print(f"Время с момента начала экзамена: {elapsed:.2f}")
    print()

    passed = [s for s in unique_students if s.status == "Сдал" and s.exam_time is not None]
    if passed:
        min_time = min(s.exam_time for s in passed)
        best = [s.name for s in passed if s.exam_time == min_time]
        print(f"Имена лучших студентов: {', '.join(best)}")
    else:
        print("Имена лучших студентов: Нет")

    active = [e for e in examiners if e.total_students > 0]
    if active:
        min_rate = min(e.failed_students / e.total_students for e in active)
        best = [e.name for e in active if e.failed_students / e.total_students == min_rate]
        print(f"Имена лучших экзаменаторов: {', '.join(best)}")
    else:
        print("Имена лучших экзаменаторов: Нет")

    failed = [s for s in unique_students if s.status == "Провалил" and s.exam_time is not None]
    if failed:
        min_time = min(s.exam_time for s in failed)
        expelled = [s.name for s in failed if s.exam_time == min_time]
        print(f"Имена студентов, которых после экзамена отчислят: {', '.join(expelled)}")
    else:
        print("Имена студентов, которых после экзамена отчислят: Нет")

    if questions:
        max_correct = max(q.correct_count for q in questions)
        if max_correct > 0:
            best = [q.text for q in questions if q.correct_count == max_correct]
            print(f"Лучшие вопросы: {', '.join(best)}")
        else:
            print("Лучшие вопросы: Нет")
    else:
        print("Лучшие вопросы: Нет")

    passed_count = sum(1 for s in unique_students if s.status == "Сдал")
    total = len(unique_students)
    if total > 0 and passed_count / total > 0.85:
        print("Вывод: Экзамен удался")
    else:
        print(f"Вывод: Экзамен не удался ({passed_count}/{total} = {passed_count/total*100:.1f}%)")