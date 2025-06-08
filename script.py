import re
import json

def parse_sections(filename):
    with open(filename, encoding="utf-8") as f:
        lines = f.read().splitlines()
    data = {}
    current_num = None
    current_title = None
    current_content = []
    for line in lines:
        match = re.match(r'^(\d+)\.\s*(.*)', line)
        if match:
            # Зберігаємо попередній розділ
            if current_num is not None:
                data[current_num] = {
                    "title": current_title,
                    "content": "\n".join(current_content).strip()
                }
            current_num = match.group(1)
            current_title = match.group(2).strip() or None
            current_content = []
        else:
            current_content.append(line)
    # Зберегти останній розділ
    if current_num is not None:
        data[current_num] = {
            "title": current_title,
            "content": "\n".join(current_content).strip()
        }
    return data

# Парсимо обидва файли
topics = parse_sections("data.txt")
formulas = parse_sections("formulas.txt")

# Об'єднуємо формули у topics, якщо є
for num, formula_data in formulas.items():
    if num in topics:
        topics[num]["formulas"] = formula_data["content"]
    else:
        # Якщо формула є для теми, якої немає в topics,
        # можемо додати або пропустити
        topics[num] = {
            "title": None,
            "content": "",
            "formulas": formula_data["content"]
        }

# Записуємо результат у JSON-файл
with open("all_topics.json", "w", encoding="utf-8") as f:
    json.dump(topics, f, ensure_ascii=False, indent=2)

print("Файл all_topics.json створено успішно!")
