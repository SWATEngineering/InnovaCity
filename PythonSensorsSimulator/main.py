import os
# from src.simulator_utils.kafka_simulator_executor_factory import KafkaSimulatorExecutorFactory
from src.simulator_utils.stdout_simulator_executor_factory import StdoutSimulatorExecutorFactory

# env var reading
KAFKA_HOST = os.environ.get("KAFKA_HOST", "kafka")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")

# JSON config file reading
config_file = open("simulators_config.json", "r")
config_str = config_file.read()
config_file.close()

# configuration factory creation (kafka writer)
# sim_exe_factory = KafkaSimulatorExecutorFactory(
   # configs=config_str,
   # data_broker_host=KAFKA_HOST,
   # data_broker_port=KAFKA_PORT
# )

# configuration factory creation (stdout writer)
sim_exe_factory = StdoutSimulatorExecutorFactory(
    configs=config_str
)

# simulator executor creation
sim_exe = sim_exe_factory.create()

# simulators execution
sim_exe.run_all()
