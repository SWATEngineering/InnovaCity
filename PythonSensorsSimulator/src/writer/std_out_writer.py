from writer import writer_strategy


class StdoutWriter(WriterStrategy):
    def write(self, to_write: str) -> None:
        print(to_write + '\n')
