import asyncio

def handle_connection(connection):
    with connection:
        session = Session(connection)
        try:
            session.loop()
        except EOFError:
            pass

def run_server(address):
    with socket.socket() as listener:
        listener.bind(address)
        listener.listen()
        while True:
            connection, _ = listener.accept()
            thread = Thread(target=handle_connection,
                            args=(connection,),
                            daemon=True)
            thread.start()

async def run_client(address):
    # 서버가 시작될 수 있게 기다려주기
    await asyncio.sleep(0.1)

    streams = await asyncio.open_connection(*address)   # New
    client = AsyncClient(*streams)                      # New

    async with client.session(1, 5, 3):
        results = [(x, await client.report_outcome(x))
                   async for x in client.request_numbers(5)]

    async with client.session(10, 15, 12):
        async for number in client.request_numbers(5):
            outcome = await client.report_outcome(number)
            results.append((number, outcome))

    _, writer = streams                                # 새 기능
    writer.close()                                     # 새 기능
    await writer.wait_closed()                         # 새 기능

    return results

async def main():
    address = ('127.0.0.1', 4321)

    server = run_server(address)
    asyncio.create_task(server)

    results = await run_client(address)
    for number, outcome in results:
        print(f'클라이언트: {number}는 {outcome}')

asyncio.run(main())
