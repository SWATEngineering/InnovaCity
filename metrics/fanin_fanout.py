import os

def calculate_fan_in_out(folder_path):
    fan_in_out = {}
    for filename in os.listdir(folder_path):
        print(filename)
        if os.path.isfile(filename) and filename.endswith('.py'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                fan_in = 0
                fan_out = 0
                for line in file:
                    words = line.split()
                    for word in words:
                        if word == filename:
                            fan_in += 1
                        elif word in os.listdir(folder_path) and os.path.isfile(word):
                            fan_out += 1
                fan_in_out[filename] = {'fan_in': fan_in, 'fan_out': fan_out}
    return fan_in_out

current_folder = os.path.join(os.getcwd(), "PythonSensorsSimulator")
print(current_folder)
result = calculate_fan_in_out(current_folder)
for filename, values in result.items():
    print(f"File: {filename}, Fan In: {values['fan_in']}, Fan Out: {values['fan_out']}")
