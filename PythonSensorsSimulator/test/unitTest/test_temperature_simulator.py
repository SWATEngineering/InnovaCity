import json
from datetime import datetime, timedelta
from unittest.mock import patch
from PythonSensorsSimulator.src.simulator.temperature_sensor_simulator import TemperatureSensorSensorSimulator
from PythonSensorsSimulator.src.utils.coordinates import Coordinates
from random import Random


def test_temperature_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining a specific datetime for the simulation
    simulated_datetime = datetime(2024, 3, 18, 10, 19, 9, 447663)

    # Mocking random object
    with patch.object(Random, 'uniform', return_value=0):
        with patch.object(Random, 'random', return_value=0):
            random_obj = Random()

            # Mocking datetime object to return the specific datetime
            with patch('datetime.datetime') as mocked_datetime:
                mocked_datetime.now.return_value = simulated_datetime

                # Creating an instance of the TemperatureSensorSensorSimulator with coordinates
                sensor_simulator = TemperatureSensorSensorSimulator("temperature1", random_obj, mocked_datetime,
                                                                    coordinates)

                # Running the simulate method to get the JSON data
                json_data = sensor_simulator.simulate()

                # Parsing the JSON data
                parsed_json = json.loads(json_data)

                # Define the expected JSON structure
                expected_json = {
                    "type": "temperature",
                    "timestamp": "2024-03-18 10:19:09.447663",
                    "readings": [{"type": "Celsius Degrees", "value": 15.58}],
                    "name": "temperature1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }

                # Assert that the parsed JSON matches the expected JSON
                assert parsed_json == expected_json


def test_temperature_sensor_simulation_range():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking random object
    random_obj = Random()

    # Defining the range for temperature
    min_temp = 3.5
    max_temp = 18.5

    # Running the simulation 1000 times with different timestamps
    for i in range(24*60):
        # Creating a timestamp for the simulation
        simulated_datetime = datetime(2024, 3, 18, 0, 0, 0) + timedelta(minutes=i)
        with patch('datetime.datetime') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime

            # Creating an instance of the TemperatureSensorSensorSimulator with coordinates
            sensor_simulator = TemperatureSensorSensorSimulator("temperature1", random_obj, mocked_datetime,
                                                                coordinates)

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Extracting the temperature value
            temperature = parsed_json['readings'][0]['value']

            # Assert that the temperature is within the specified range
            assert min_temp <= temperature <= max_temp
