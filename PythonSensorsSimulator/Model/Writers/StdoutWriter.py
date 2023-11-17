from PythonSensorsSimulator.Model.Writers import Writer


class StdoutWriter(Writer.Writer):
    def write(self, to_write: str) -> None:
        print(to_write + '\n')
