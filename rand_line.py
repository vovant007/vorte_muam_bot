import numpy as np

def _read_line(file_name, line_number):
    with open(file_name, 'r', encoding='utf-8') as file:
        for index, line in enumerate(file, start=1):
            if index == line_number:
                return line

n_line = np.random.randint(1, 84)
line = _read_line(file_name = 'facts.txt', line_number = n_line)
print(line)