import time

from Model.Writers.StdoutWriter import StdoutWriter
from Model.BuilderSimulatorExecutor import BuilderSimulatorExecutor

#Uso generale di una interfaccia Writer al fine di poter implementare quante politiche diverse di writing si vuole,
#senza dover cambiare nulla sul resto del codice.
writeToStd = StdoutWriter()

symExecBuilder = BuilderSimulatorExecutor(writeToStd)

# Builder pattern per la configurazione dell'esecutore di simulatori.
symExec = (
    symExecBuilder
    .addTemperatureSimulator("#1",0.5)
    .addTemperatureSimulator("#2",0.75)
    .addTemperatureSimulator("#3",1.5)
    .getSimulatorExecutor()
)

symExec.run_all()
time.sleep(3.25) # do un tempo di 2 secondi per far si che si fermi da solo.
symExec.stop_all()

#NOTA: ereditarietà usata solamente per l'implementazione di metodi di classi astratte.