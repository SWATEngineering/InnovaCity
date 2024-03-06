import os
from simulator_utils.kafka_simulator_executor_factory import KafkaSimulatorExecutorFactory

# env var reading
KAFKA_HOST = os.environ.get("KAFKA_HOST", "kafka")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")

# JSON config file reading
config_file = open("simulator_utils", "r")
config_str = config_file.read()
config_file.close()

# configuration factory creation
sim_exe_factory = KafkaSimulatorExecutorFactory(
    _SimulatorExecutorFactory__configs=config_str,
    _SimulatorExecutorFactory__data_broker_host=KAFKA_HOST,
    _SimulatorExecutorFactory__data_broker_port=KAFKA_PORT
)

# simulator executor creation
sim_exe = sim_exe_factory.create()

# simulators execution
sim_exe.run_all()
