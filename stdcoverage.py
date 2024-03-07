import json

# Read JSON data from a file


def read_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Compute coverage for each file and the total


def compute_coverage(data):
    file_coverages = []

    for filename, file_info in data['files'].items():
        statement_coverage = file_info['summary']['percent_covered']

        num_branches = file_info['summary']['num_branches']
        num_missing_branches = file_info['summary']['missing_branches']
        branch_coverage = (num_branches - num_missing_branches) / \
            num_branches * 100 if num_branches > 0 else 100

        file_coverages.append({
            'Filename': filename,
            'Statement Coverage (%)': statement_coverage,
            'Branch Coverage (%)': branch_coverage
        })

    total_statement_coverage = data['totals']['percent_covered']

    num_total_branches = data['totals']['num_branches']
    num_missing_total_branches = data['totals']['missing_branches']
    total_branch_coverage = (num_total_branches - num_missing_total_branches) / \
        num_total_branches * 100 if num_total_branches > 0 else 100

    total_coverage = {
        'Filename': 'Total',
        'Statement Coverage (%)': total_statement_coverage,
        'Branch Coverage (%)': total_branch_coverage
    }

    return file_coverages, total_coverage

# Print coverage data to standard output


def print_coverage(file_coverages, total_coverage):
    # Print header
    print("{:<40} {:>20}  {:>20}".format(
        'File', 'Stmt Coverage (%)',  'Branch Coverage (%)'))
    print("-" * 100)

    # Print file coverages
    for file_coverage in file_coverages:
        print("{:<40} {:>20.2f}  {:>20.2f}".format(
            file_coverage['Filename'], file_coverage['Statement Coverage (%)'],  file_coverage['Branch Coverage (%)']))

    # Print total coverage
    print("-" * 100)
    print("{:<40} {:>20.2f}  {:>20.2f}".format(
        total_coverage['Filename'], total_coverage['Statement Coverage (%)'], total_coverage['Branch Coverage (%)']))


# Specify the filename of the JSON file
json_filename = 'PythonSensorsSimulator/coverage.json'

# Read JSON data from the file
json_data = read_json_file(json_filename)

# Compute coverage for each file and total
file_coverages, total_coverage = compute_coverage(json_data)

# Print coverage data to standard output
print_coverage(file_coverages, total_coverage)
