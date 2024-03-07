#!/bin/bash
pip install pytest 
pip install coverage

cd PythonSensorsSimulator 

#aimeh le cartelle vanno inserite manualmente
SOURCE_DIRS="Model Model/Simulators"


COVERAGE_COMMAND="coverage run --branch --source=$(echo $SOURCE_DIRS | tr ' ' ',') -m pytest test/"

# Run the coverage command
$COVERAGE_COMMAND

# Generate coverage report in JSON format
coverage json -o coverage.json

# Generate HTML coverage report
coverage html -d coverage_html

cd ..

python stdcoverage.py
