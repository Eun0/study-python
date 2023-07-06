class EOFError(Exception):
    pass

class AsyncConnectionBase:
    def __init__(self, reader, writer):  # 변경됨
        self.reader = reader  # 변경됨
        self.writer = writer  # 변경됨

    async def send(self, command):
        line = command + '\n'
        data = line.encode()
        self.writer.write(data)  # 변경됨
        await self.writer.drain()  # 변경됨

    async def receive(self):
        line = await self.reader.readline()  # 변경됨
        if not line:
            raise EOFError('연결 닫힘')
        return line[:-1].decode()
