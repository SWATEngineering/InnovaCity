import json
from datetime import datetime
from random import Random
import time
import pytest
import clickhouse_connect
from src.utils.sensor_types import SensorTypes
from src.writer.kafka_logic.adapter_producer import AdapterProducer
from src.simulator.ebike_sensor_simulator import EBikeSensorSimulator
from src.utils.coordinates import Coordinates


class TestEbike:
    @pytest.fixture(scope="class")
    def setup_adapter_producer(self):
        ip = "localhost"
        port = 9093
        topic = SensorTypes.ELECTRIC_BICYCLE
        return AdapterProducer(topic, ip, port)

    @pytest.fixture(scope="class")
    def setup_client(self):
        return clickhouse_connect.get_client(
            host='localhost', port=8123, database="innovacity", user="ic_admin", password="ic_admin")

    @pytest.fixture(scope="class")
    def setup_simulator(self):
        sensor_name = "Test"
        random_obj = Random()
        datetime_obj = datetime
        coordinates = Coordinates(0.0, 0.0)
        return EBikeSensorSimulator(sensor_name, random_obj, datetime_obj, coordinates)

    def setup_before_test(self, setup_adapter_producer, setup_simulator):
        adapter_producer = setup_adapter_producer
        sensor_simulator = setup_simulator
        message = sensor_simulator.simulate()
        adapter_producer.produce(message, None)

    def teardown_after_test(self, setup_client):
        query = "DELETE FROM innovacity.ebikes WHERE name = 'Test';"
        setup_client.query(query)

    def test_persistence(self, setup_client, setup_adapter_producer, setup_simulator):
        self.setup_before_test(setup_adapter_producer, setup_simulator)
        timeout = 30
        start_time = time.time()
        while True:
            query = "SELECT name FROM innovacity.ebikes WHERE name = 'Test';"
            result = setup_client.query(query)
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
        self.teardown_after_test(setup_client)
