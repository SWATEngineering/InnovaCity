
#!/bin/bash

pylint  PythonSensorsSimulator/ > pylint_report.txt
python3 analisiStatica.py