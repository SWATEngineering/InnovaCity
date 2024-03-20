import os
import ast


def resolve_relative_import(module_path, relative_import):
    """Resolve a relative import to an absolute path."""
    base_path = os.path.dirname(module_path)
    absolute_path = os.path.normpath(os.path.join(base_path, relative_import))
    return absolute_path.replace(os.sep, '.')


def parse_source_file(file_path):
    """Parse a Python source file and extract import statements."""
    with open(file_path, 'r') as f:
        source_code = f.read()
    tree = ast.parse(source_code)
    imports = []

    # Traverse the abstract syntax tree
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module
            if node.level > 0:
                # Resolve relative import to absolute path
                resolved_path = resolve_relative_import(
                    file_path, '.' * node.level + module_name)
                imports.append(resolved_path)
            else:
                if node.names[0].name == '*':
                    imports.append(module_name + ".*")
                else:
                    for alias in node.names:
                        imports.append(module_name + "." + alias.name)

    return imports

# Other functions remain unchanged


def build_dependency_graph(directory):
    """Build dependency graphs for SF-IN and SF-OUT."""
    dependency_graph_in = {}
    dependency_graph_out = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                dependencies = parse_source_file(file_path)
                dependency_graph_out[file_path] = dependencies

                for dependency in dependencies:
                    dependency_graph_in.setdefault(
                        dependency, []).append(file_path)

    return dependency_graph_in, dependency_graph_out


def calculate_sfin_sfout(dependency_graph_in, dependency_graph_out):
    """Calculate SF-IN and SF-OUT metrics."""
    sfin = {module: len(dependencies)
            for module, dependencies in dependency_graph_in.items()}
    sfout = {module: len(dependencies)
             for module, dependencies in dependency_graph_out.items()}
    return sfin, sfout


def calculate_sfin_sfout_for_project(project_directory):
    """Calculate SFIN and SFOUT for all Python files in the project directory."""
    # Initialize dependency graphs
    dependency_graph_in = {}
    dependency_graph_out = {}

    # Iterate through all files in the project directory
    for root, _, files in os.walk(project_directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)

                # Parse the source file and extract dependencies
                dependencies = parse_source_file(file_path)

                # Update the dependency graphs
                dependency_graph_out[file_path] = dependencies
                for dependency in dependencies:
                    dependency_graph_in.setdefault(
                        dependency, []).append(file_path)

    # Calculate SFIN and SFOUT metrics
    sfin, sfout = calculate_sfin_sfout(
        dependency_graph_in, dependency_graph_out)

    return sfin, sfout


if __name__ == "__main__":
    project_directory = 'PythonSensorsSimulator/src'
    sfin, sfout = calculate_sfin_sfout_for_project(project_directory)

    print("Structure Fan-In (SFIN) for each module:")
    for module, value in sfin.items():
        print(f"{module}: {value}")

    print("\nStructure Fan-Out (SFOUT) for each module:")
    for module, value in sfout.items():
        print(f"{module}: {value}")
