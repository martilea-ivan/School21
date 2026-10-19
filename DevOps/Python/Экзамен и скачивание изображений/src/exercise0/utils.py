import os


def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')


def read_file_with_fallback(filename: str) -> list:

    encodings = ['utf-8', 'cp1251', 'windows-1251', 'latin-1']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                lines = [line.strip() for line in f if line.strip()]
            return lines
        except UnicodeDecodeError:
            continue


    with open(filename, 'rb') as f:
        data = f.read()
        text = data.decode('utf-8', errors='replace')
        lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines


def parse_person_data(raw_lines: list) -> list:

    result = []
    for line in raw_lines:
        parts = line.split()
        if len(parts) >= 2:
            name = ' '.join(parts[:-1])
            gender = parts[-1]
        else:
            name = parts[0]
            gender = 'М'  # По умолчанию — мужчина
        result.append([name, gender])
    return result