import os
import re
from collections import defaultdict

required_modules = ["2", "3", "4", "5", "7", "10", "11", "12", "13", "17", "18"]

def extract_module_number(name):
    name = name.lower().strip()
    name = re.sub(r'[-_.]', ' ', name)
    match = re.search(r'(?:modul\s*)?0*(\d{1,2})(?=\D|$)', name)
    if match:
        num = match.group(1)
        if num in required_modules:
            return num
    return None

def generate_markdown_table(base_path):
    header = ["| Student ID | " + " | ".join(required_modules) + " |"]
    separator = ["|------------|" + "|".join([":--:"] * len(required_modules)) + "|"]
    rows = []

    students = sorted([s for s in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, s))])
    for student in students:
        if student == ".git":
            continue
        student_id = student.split()[0]
        student_path = os.path.join(base_path, student)

        completed = defaultdict(bool)

        for folder in os.listdir(student_path):
            mod_num = extract_module_number(folder)
            if mod_num:
                completed[mod_num] = True

        row_items = [f"[{student_id}](./{student})"]  # ✅ Link to student folder
        row_items += [("✅" if completed[mod] else "❌") for mod in required_modules]
        rows.append("| " + " | ".join(row_items) + " |")


    return "\n".join(header + separator + rows)

base_folder = "./"
markdown = generate_markdown_table(base_folder)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(markdown)

print("✅ Done. Check 'README.md'")
