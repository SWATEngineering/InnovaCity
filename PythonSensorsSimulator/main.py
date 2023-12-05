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
    .add_temperature_simulator(writeToKafkaTemp, 1)
    .add_temperature_simulator(writeToKafkaTemp, 1)
    .add_temperature_simulator(writeToKafkaTemp, 1)
    .get_simulator_executor()
)

symExec.run_all()
