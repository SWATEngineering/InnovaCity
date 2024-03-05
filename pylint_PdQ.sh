#!/bin/bash

pylint  PythonSensorsSimulator/ > pylint_report.txt
python3 pypylint_PdQ.py
