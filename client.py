class AsyncClient(AsyncConnectionBase):
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        self.secret = None
        self.last_distance = None

    @contextlib.asynccontextmanager                         # 변경됨
    async def session(self, lower, upper, secret):          # 변경됨
        print(f'\n{lower}와 {upper} 사이의 숫자를 맞춰보세요!'
              f' 쉿! 그 숫자는 {secret} 입니다.')
        self.secret = secret
        await self.send(f'PARAMS {lower} {upper}')          # 변경됨
        try:
            yield
        finally:
            self._clear_state()
            await self.send('PARAMS 0 -1')                   # 변경됨

    async def request_numbers(self, count):            # 변경됨
        for _ in range(count):
            await self.send('NUMBER')                  # 변경됨
            data = await self.receive()                # 변경됨
            yield int(data)
            if self.last_distance == 0:
                return

    async def report_outcome(self, number):                    # 변경됨
        new_distance = math.fabs(number - self.secret)
        decision = UNSURE

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER

        self.last_distance = new_distance

        await self.send(f'REPORT {decision}')                  # 변경됨

        # 잠시 대기해서 출력 순서 조정
        await asyncio.sleep(0.01)
        return decision
