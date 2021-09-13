import os
import sys
path = r"C:\Users\User\Downloads\ATHARVAVEDA-SAUNAKA_text.txt"

with open(path, encoding="utf-8", errors="ignore") as file:
    text = file.read()
    text = text.replace('\n', '')

    print(text)