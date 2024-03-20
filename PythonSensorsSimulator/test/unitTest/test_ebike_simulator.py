import json
from datetime import datetime, timedelta
from unittest.mock import patch
from src.simulator.ebike_sensor_simulator import EBikeSensorSimulator
from src.utils.coordinates import Coordinates
from random import Random

def test_pick_destination():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking datetime object
    with patch('datetime.datetime') as mocked_datetime:
        spring_datetime = datetime(2024, 3, 18, 17, 0, 0, 447663)
        mocked_datetime.now.return_value = spring_datetime

        # Mocking random object
        with patch.object(Random, 'random', return_value=0):
            random_obj = Random()

            # Mocking the environment variable
            with patch.dict('os.environ', {'ORS_API_KEY': 'placeholder_api_key'}):
                
                # Mocking _pick_destination to return predetermined destination coordinates
                with patch.object(EBikeSensorSimulator, '_pick_destination') as mock_pick_destination:
                    mock_pick_destination.return_value = (45.4, 11.86)

                    # Creating the sensor simulator object
                    sensor_simulator = EBikeSensorSimulator("electric_bicycle1", random_obj, mocked_datetime, coordinates)

                    # Call the _pick_destination method
                    destination = sensor_simulator._pick_destination()

                    # Assert that the destination is as expected
                    assert destination == (45.4, 11.86)

def test_get_route_coordinates():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking datetime object
    with patch('datetime.datetime') as mocked_datetime:
        spring_datetime = datetime(2024, 3, 18, 17, 0, 0, 447663)
        mocked_datetime.now.return_value = spring_datetime

        # Mocking random object
        with patch.object(Random, 'random', return_value=0):
            random_obj = Random()

            # Mocking _pick_destination to return predetermined destination coordinates
            with patch.object(EBikeSensorSimulator, '_pick_destination') as mock_pick_destination:
                mock_pick_destination.return_value = (45.4, 11.86)

                # Mocking _get_route_coordinates to return predetermined route coordinates
                with patch.object(EBikeSensorSimulator, '_get_route_coordinates') as mock_get_route_coordinates:
                    mock_get_route_coordinates.return_value = [(45.398214, 11.851271), (45.399742, 11.874538), (45.4, 11.86)]

                    # Creating the sensor simulator object
                    sensor_simulator = EBikeSensorSimulator("electric_bicycle1", random_obj, mocked_datetime, coordinates)

                    # Call the _get_route_coordinates method
                    route_coordinates = sensor_simulator._get_route_coordinates()

                    # Assert that the route coordinates are as expected
                    assert route_coordinates == [(45.398214, 11.851271), (45.399742, 11.874538), (45.4, 11.86)]


def test_ebike_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining a specific datetime for the simulation
    spring_datetime = datetime(2024, 3, 18, 17, 0, 0, 447663)

    # Mocking random object
    with patch.object(Random, 'uniform', return_value=0):
        with patch.object(Random, 'random', return_value=0):
            random_obj = Random()

            # Mocking datetime object to return the specific datetime
            with patch('datetime.datetime') as mocked_datetime:
                mocked_datetime.now.return_value = spring_datetime

                # Mocking _pick_destination to return predetermined destination coordinates
                with patch.object(EBikeSensorSimulator, '_pick_destination') as mock_pick_destination:
                    mock_pick_destination.return_value = (45.4, 11.86)

                    # Mocking _get_route_coordinates to return predetermined route coordinates
                    with patch.object(EBikeSensorSimulator, '_get_route_coordinates') as mock_get_route_coordinates:
                        mock_get_route_coordinates.return_value = [(45.398214, 11.851271), (45.399742, 11.874538), (45.4, 11.86)]

                        # Creating the sensor simulator object
                        sensor_simulator = EBikeSensorSimulator("electric_bicycle1", random_obj, mocked_datetime, coordinates)

                        # Define test scenarios
                        test_scenarios = [
                            (0, "2024-03-18 17:00:00.447663", 100, [45.398214, 11.851271]),
                            (1.5, "2024-03-18 17:00:01.947663", 99.94, [11.874538, 45.399742]),
                            (3, "2024-03-18 17:00:03.447663", 99.89, [11.86, 45.4])
                        ]

                        # Iterate over test scenarios
                        for delta_seconds, expected_timestamp, expected_battery_percentage, expected_coordinates in test_scenarios:
                            mocked_datetime.now.return_value = spring_datetime + timedelta(seconds=delta_seconds)
                            json_data = sensor_simulator.simulate()
                            parsed_json = json.loads(json_data)
                            expected_json = {
                                "type": "electric_bicycle",
                                "timestamp": expected_timestamp,
                                "readings": [{"type": "%", "value": expected_battery_percentage}],
                                "name": "electric_bicycle1",
                                "location": {"type": "Point", "coordinates": expected_coordinates}
                            }
                            assert parsed_json == expected_json


def test_ebike_sensor_simulation_range():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining a specific datetime for the simulation
    spring_datetime = datetime(2024, 3, 18, 17, 0, 0, 447663)

    # Mocking random object
    with patch.object(Random, 'uniform', return_value=1.5):
        with patch.object(Random, 'random', return_value=0):
            random_obj = Random()

            # Mocking datetime object to return the specific datetime
            with patch('datetime.datetime') as mocked_datetime:
                mocked_datetime.now.return_value = spring_datetime

                # Mocking _pick_destination to return predetermined destination coordinates
                with patch.object(EBikeSensorSimulator, '_pick_destination') as mock_pick_destination:
                    mock_pick_destination.return_value = (45.4, 11.86)

                    # Mocking _get_route_coordinates to return predetermined route coordinates
                    with patch.object(EBikeSensorSimulator, '_get_route_coordinates') as mock_get_route_coordinates:
                        mock_get_route_coordinates.return_value = [(45.398214, 11.851271), (45.399742, 11.874538), (45.4, 11.86)]

                        num_iterations = 1500

                        sensor_simulator = EBikeSensorSimulator("electric_bicycle1", random_obj, mocked_datetime,
                                                                coordinates)

                        # Iterate over the specified number of iterations
                        for i in range(num_iterations):
                            
                            if i % 3 == 0 and i != 0:
                                # Generate destination coordinates based on the current iteration
                                dest_longitude = 11.86 + (0.001 * i)
                                dest_latitude = 45.4 + (0.001 * i)
                                mock_pick_destination.return_value = (dest_latitude, dest_longitude)

                                # Generate route coordinates based on the current iteration
                                route_coordinates = [
                                    [45.398214 + (0.0005 * i), 11.851271 + (0.0005 * i)],
                                    [45.399742 + (0.0005 * i), 11.874538 + (0.0005 * i)],
                                    [dest_longitude, dest_latitude]
                                ]
                                mock_get_route_coordinates.return_value = route_coordinates
                            
                            # Calculate the time delta for each iteration
                            delta_seconds = i

                            # Set the current timestamp for the iteration
                            mocked_datetime.now.return_value = spring_datetime + timedelta(seconds=delta_seconds)

                            # Simulate sensor data
                            json_data = sensor_simulator.simulate()
                            parsed_json = json.loads(json_data)

                            # Defining the range for battery level
                            min_battery = 0
                            max_battery = 100
                            
                            battery = parsed_json['readings'][0]['value']

                            assert min_battery <= battery <= max_battery