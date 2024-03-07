
#!/bin/bash

pylint  PythonSensorsSimulator/src/* > pylint_report.txt
python3 analisiStatica.py