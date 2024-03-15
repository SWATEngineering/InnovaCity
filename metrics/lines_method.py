import os
import ast

def get_lines_of_code_per_method(file_path):
    lines_of_code_per_method = []

    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno
                end_line = node.end_lineno
                num_lines = end_line - start_line + 1
                lines_of_code_per_method.append((node.name, num_lines))

    return lines_of_code_per_method

def analyze_directory(directory):
    methods_with_too_many_lines = []

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                lines_per_method = get_lines_of_code_per_method(file_path)
                if lines_per_method:
                    for method_name, num_lines in lines_per_method:
                        if num_lines > 25:
                            methods_with_too_many_lines.append((file_path, method_name, num_lines))

    return methods_with_too_many_lines

directory_to_check = "../PythonSensorsSimulator"
methods_with_too_many_lines = analyze_directory(directory_to_check)

if methods_with_too_many_lines:
    print("Methods with too many lines of code:")
    for file_path, method_name, num_lines in methods_with_too_many_lines:
        print(f"- Method '{method_name}' in file '{file_path}' has {num_lines} lines.")
    exit(1)
else:
    print("All methods have 25 or fewer lines of code. No action needed.")
