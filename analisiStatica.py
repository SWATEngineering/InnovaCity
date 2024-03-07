# Open the Pylint report file
with open('pylint_report.txt', 'r') as f:
    report_lines = f.readlines()

# Count violations for specific rules
count_max_statements = sum('R0915' in line for line in report_lines)
count_max_attributes = sum('R0902' in line for line in report_lines)
count_max_args = sum('R0913' in line for line in report_lines)
count_ciclomatic = sum('too-complex' in line for line in report_lines)

# Print the counts
print("VIOLAZIONI DI MPC-LCM:", count_max_statements)
print("VIOLAZIONI DI MPC-ATC:", count_max_attributes)
print("VIOLAZIONI DI MPC-PM", count_max_args)
print("VIOLAZIONI MPD-CCM:", count_ciclomatic)
