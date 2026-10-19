import json
import os


def merge_lists(list1, list2):

    result = []
    i = j = 0

    while i < len(list1) and j < len(list2):
        if list1[i]["year"] <= list2[j]["year"]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1

    while i < len(list1):
        result.append(list1[i])
        i += 1

    while j < len(list2):
        result.append(list2[j])
        j += 1

    return result


def validate_film(film):

    if not isinstance(film, dict):
        return False

    if "title" not in film or "year" not in film:
        return False

    if not isinstance(film["title"], str):
        return False

    if not isinstance(film["year"], int):
        return False

    return True


def validate_list(films):

    if not isinstance(films, list):
        return False

    for film in films:
        if not validate_film(film):
            return False

    return True


def is_sorted_by_year(films):

    for i in range(len(films) - 1):
        if films[i]["year"] > films[i + 1]["year"]:
            return False
    return True


def main():

    if not os.path.exists("input.txt"):
        print("Invalid input")
        return

    try:
        with open("input.txt", "r", encoding="utf-8") as f:
            content = f.read()

        if not content or not content.strip():
            print("Empty file")
            return

        data = json.loads(content)

        if "list1" not in data or "list2" not in data:
            print("Invalid input")
            return

        list1 = data["list1"]
        list2 = data["list2"]

        if not validate_list(list1) or not validate_list(list2):
            print("Invalid input")
            return

        if not is_sorted_by_year(list1) or not is_sorted_by_year(list2):
            print("Invalid input")
            return

        merged = merge_lists(list1, list2)

        result = {"list0": merged}
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except json.JSONDecodeError:
        print("Invalid input")
    except Exception:
        print("Invalid input")


if __name__ == "__main__":
    main()