import json
from datetime import datetime
from random import Random
import time
import pytest
import clickhouse_connect
from src.utils.sensor_types import SensorTypes
from src.writer.kafka_logic.adapter_producer import AdapterProducer
from src.simulator.temperature_sensor_simulator import TemperatureSensorSensorSimulator
from src.utils.coordinates import Coordinates


class TestTemperature:
    @pytest.fixture(scope="class")
    def setup_adapter_producer(self):
        topic = SensorTypes.TEMPERATURE
        ip = "localhost"
        port = 9093
        return AdapterProducer(topic, ip, port)

    @pytest.fixture(scope="class")
    def setup_client(self):
        return clickhouse_connect.get_client(
            host='localhost', port=8123, database="innovacity", user="ic_admin", password="ic_admin"
        )

    @pytest.fixture(scope="class")
    def setup_simulator(self):
        sensor_name = "TestTemperatura"
        random_obj = Random()
        datetime_obj = datetime
        coordinates = Coordinates(0.0, 0.0)
        return TemperatureSensorSensorSimulator(sensor_name, random_obj, datetime_obj, coordinates)

    def test_persistence(self, setup_adapter_producer, setup_client, setup_simulator):
        adapter_producer = setup_adapter_producer
        client = setup_client
        temperature_sensor_simulator = setup_simulator

        message = temperature_sensor_simulator.simulate()

        adapter_producer.produce(message, None)

        timeout = 5  # Timeout in seconds
        start_time = time.time()

        while True:
            query = "SELECT name FROM innovacity.temperatures WHERE name = 'TestTemperatura';"
            result = client.query(query)
            if result.result_rows:
                fetched_row = result.result_rows[0]
                fetched_timestamp = fetched_row[0]
                assert fetched_timestamp is not None, "No entry fetched from the database."
                break
            elif time.time() - start_time >= timeout:
                pytest.fail(
                    "Timeout reached. No entry fetched from the database within the specified timeout period.")
            else:
                time.sleep(1)  # Wait for 1 second before retrying

        query = "DELETE FROM temperatures WHERE name = 'TestTemperatura';"
        client.query(query)

    def test_persistence_aggregate(self, setup_adapter_producer, setup_client, setup_simulator):
        adapter_producer = setup_adapter_producer
        client = setup_client
        temperature_sensor_simulator = setup_simulator
        message = temperature_sensor_simulator.simulate()
        adapter_producer.produce(message, None)

        timeout = 5  # Timeout in seconds
        start_time = time.time()

        while True:
            query = "SELECT name FROM innovacity.temperatures1m WHERE name = 'TestTemperatura';"
            result = client.query(query)
            if result.result_rows:
                fetched_row = result.result_rows[0]
                fetched_timestamp = fetched_row[0]
                assert fetched_timestamp is not None, "No entry fetched from the database."
                break
            elif time.time() - start_time >= timeout:
                pytest.fail(
                    "Timeout reached. No entry fetched from the database within the specified timeout period.")
            else:
                time.sleep(1)  # Wait for 1 second before retrying

        query = "DELETE FROM temperatures1m WHERE name = 'TestTemperatura';"
        client.query(query)
