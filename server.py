class AsyncSession(AsyncConnectionBase):  # 변경됨
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state(None, None)

    def _clear_state(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.guesses = []

    async def loop(self):  # 변경됨
        while command := await self.receive():  # 변경됨
            parts = command.split(' ')
            if parts[0] == 'PARAMS':
                self.set_params(parts)
            elif parts[0] == 'NUMBER':
                await self.send_number()  # 변경됨
            elif parts[0] == 'REPORT':
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)

    def set_params(self, parts):
        assert len(parts) == 3
        lower = int(parts[1])
        upper = int(parts[2])
        self._clear_state(lower, upper)

    def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    async def send_number(self):
        guess = self.next_guess()
        self.guesses.append(guess)
        await self.send(format(guess))

    def receive_report(self, parts):
        assert len(parts) == 2
        decision = parts[1]
        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f'서버: {last}는 {decision}')
