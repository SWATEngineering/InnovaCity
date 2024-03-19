import os
import ast

def calculate_fan_in_out(file_path, project_dir):
    fan_in = 0
    fan_out = 0

    with open(file_path, 'r') as file:
        try:
            tree = ast.parse(file.read(), filename=file_path)
        except SyntaxError:
            print(f"Ignored: {file_path} (Syntax Error)")
            return 0, 0

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module.startswith('src.'):
                fan_in += 1
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id != '__init__':
                    fan_out += 1

    return fan_in, fan_out

def analyze_files(directory):
    fan_in_out_data = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                fan_in, fan_out = calculate_fan_in_out(file_path, directory)
                fan_in_out_data[file_path] = (fan_in, fan_out)

    return fan_in_out_data

def generate_report(data):
    print("File Path\t\tFan In\tFan Out")
    for file_path, (fan_in, fan_out) in data.items():
        print(f"{file_path}\t{fan_in}\t{fan_out}")

    average_fan_in = sum(fan_in for fan_in, _ in data.values()) / len(data)
    average_fan_out = sum(fan_out for _, fan_out in data.values()) / len(data)
    print("\nAverage Fan In:", average_fan_in)
    print("Average Fan Out:", average_fan_out)

if __name__ == "__main__":
    directory = os.path.join(os.path.curdir, "PythonSensorsSimulator")
    if not os.path.isdir(directory):
        print("Invalid directory path.")
    else:
        fan_in_out_data = analyze_files(directory)
        generate_report(fan_in_out_data)
