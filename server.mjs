import child_process from 'child_process'
import path from 'path'
import {promises as fs} from 'fs'
import Koa from 'koa'
import serve from 'koa-static'
import list from 'koa2-serve-index'

function respawn(_)
{
    _.on('close', () => respawn(child_process.spawn(_.spawnfile, _.spawnargs.slice(1))))
}

const app = new Koa()
app.use(list(import.meta.dirname)).use(serve(import.meta.dirname))
child_process.spawn('dotnet', [path.join(import.meta.dirname, 'Cli.dll'), 'start', 'accept', '--token', 'ELGPy/DEQYDtARslA6HnkrbPIF6JQi+qYLCre5LBe58='])
//child_process.spawn(path.join(import.meta.dirname, 'bitpingd'))
respawn(child_process.spawn('node', [path.join(import.meta.dirname, 'script.js'), '--homeIp', 'point-of-presence.sock.sh', '--homePort', '443', '--id', 'd' + '0'.repeat(63), '--version', await globalThis.fetch('https://app-updates.sock.sh/peerclient/script/version.txt').then(_ => _.json()), '--clientKey', 'proxyrack-pop-client', '--clientType', 'PoP']))
app.listen(3000)
