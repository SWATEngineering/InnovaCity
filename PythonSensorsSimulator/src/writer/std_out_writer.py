from src.writer.writer_strategy import WriterStrategy


class StdoutWriter(WriterStrategy):
    def write(self, to_write: str) -> None:
        print(to_write + '\n')
