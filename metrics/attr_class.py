import os
import ast

def count_attributes_in_classes(folder_path):
    problematic_classes = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    try:
                        tree = ast.parse(file.read(), filename=file_name)
                        for node in tree.body:
                            if isinstance(node, ast.ClassDef):
                                class_name = node.name
                                class_attributes = node.body
                                num_attributes = len([attr for attr in class_attributes if isinstance(attr, ast.AnnAssign)])
                                if num_attributes > 6:
                                    problematic_classes.append((file_name, class_name, num_attributes))
                    except SyntaxError:
                        print(f"Syntax error in file: {file_name}")
    return problematic_classes

if __name__ == "__main__":
    folder_path = "../PythonSensorsSimulator"
    problematic_classes = count_attributes_in_classes(folder_path)
    if problematic_classes:
        print("Classes with more than 6 attributes:")
        for file_name, class_name, num_attributes in problematic_classes:
            print(f"In file: {file_name}, class: {class_name}, attributes: {num_attributes}")
        exit()
    else:
        print("No classes found with more than 6 attributes.")
