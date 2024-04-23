import re

a = """
Дыбка степная[1] (лат. Saga pedo) — кузнечик подсемейства дыбок. Самы(лат. Saga pedo) — кузнечик подсем(лат. Saga pedo) — кузнечик подсем(лат. Saga pedo) — кузнечик подсем(лат. Saga pedo) — кузнечик подсемй крупный кузнечик России. Занесён в Красную книгу МСОП, Европейский Красный список, Приложение 2 Бернской конвенции, в Красные книги Украины и РФ в категорию 2 (сокращающийся в численности вид).
"""

def print_hi(name):
    pattern = "\(лат\.([^)]+)\)"
    match = re.search(pattern, a)

    print(match)
    if match:
        latin_name = match.group(1)
        return latin_name
    else:
        return "1"


if __name__ == '__main__':
    print(print_hi('PyCharm'))
