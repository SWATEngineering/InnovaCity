import os
import ast

def get_methods_with_too_many_parameters(file_path):
    methods_with_too_many_parameters = []

    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                num_params = len(node.args.args) + len(node.args.kwonlyargs)
                if num_params > 5:
                    methods_with_too_many_parameters.append((node.name, num_params))

    return methods_with_too_many_parameters

def analyze_directory(directory):
    methods_with_too_many_parameters = []

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                methods = get_methods_with_too_many_parameters(file_path)
                if methods:
                    for method_name, num_params in methods:
                        methods_with_too_many_parameters.append((file_path, method_name, num_params))

    return methods_with_too_many_parameters

directory_to_check = "../PythonSensorsSimulator"
methods_with_too_many_parameters = analyze_directory(directory_to_check)

if methods_with_too_many_parameters:
    print("Methods with too many parameters:")
    for file_path, method_name, num_params in methods_with_too_many_parameters:
        print(f"- Method '{method_name}' in file '{file_path}' has {num_params} parameters.")
    print("Exiting because methods with too many parameters were found.")
else:
    print("All methods have 5 or fewer parameters. No action needed.")
