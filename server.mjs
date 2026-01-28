import asyncio, aiohttp.web, pathlib, uvloop, sys, fileinput, wizardgain, builtins, uuid, os

async def main():
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.static('/', pathlib.Path(__file__).resolve().parent, show_index=True)])
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, port=3000)
    await site.start()
    asyncio.create_task(wizardgain.run_client(builtins.str(uuid.uuid4()), 'chaowen.guo1@gmail.com', 'https://connector.wizardgain.com'))
    while True:
        node = await asyncio.create_subprocess_exec('node', pathlib.Path(__file__).resolve().parent.joinpath('script.js'), '--homeIp', 'point-of-presence.sock.sh', '--homePort', '443', '--id', 'galaxycloud', '--version', '54', '--clientKey', 'proxyrack-pop-client', '--clientType', 'PoP')
        await node.wait()

if __name__ == '__main__': uvloop.run(sys.modules[__name__].main())
