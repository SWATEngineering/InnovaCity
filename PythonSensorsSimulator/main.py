import os

from Model.BuilderSimulatorExecutor import BuilderSimulatorExecutor
from Model.Writers.KafkaWriter import KafkaWriter

KAFKA_HOST = os.environ.get("KAFKA_HOST", "kafka")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")

# Uso generale di una interfaccia Writer al fine di poter implementare quante politiche diverse di writing si vuole,
# senza dover cambiare nulla sul resto del codice.
# writeToStd = StdoutWriter()
writeToKafkaTemp = KafkaWriter("temperature", KAFKA_HOST, KAFKA_PORT)

symExecBuilder = BuilderSimulatorExecutor()

# Builder pattern per la configurazione dell'esecutore di simulatori.
symExec = (
    symExecBuilder
    .add_temperature_simulator(writeToKafkaTemp, 45.398214, 11.851271, 1)
    .add_temperature_simulator(writeToKafkaTemp, 45.388622, 11.946768, 1.1)
    .add_temperature_simulator(writeToKafkaTemp, 45.378850, 11.860942, 1)
    .add_temperature_simulator(writeToKafkaTemp, 45.390749, 11.849001, 1)
    .add_temperature_simulator(writeToKafkaTemp, 45.423596, 11.905983, 0.9)
    .add_temperature_simulator(writeToKafkaTemp, 45.418965, 11.851800, 1.1)
    .add_temperature_simulator(writeToKafkaTemp, 45.408298, 11.876992, 0.9)
    .add_temperature_simulator(writeToKafkaTemp, 45.445202, 11.883990, 1.1)
    .get_simulator_executor()
)

symExec.run_all()
