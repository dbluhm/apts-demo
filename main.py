import argparse
import hashlib
import json
import os

from aiohttp import web

from aries_staticagent import StaticAgentConnection, Dispatcher, crypto

from protocols.connections import Connections

# Config Start

def config():
    """ Get config """
    def environ_or_required(key):
        if os.environ.get(key):
            return {'default': os.environ.get(key)}
        return {'required': True}

    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', **environ_or_required('ARIES_ENDPOINT'))
    parser.add_argument('--port', **environ_or_required('PORT'))
    args = parser.parse_args()
    return args

def main():
    """ Main startup """
    args = config()

    test_vk, _test_sk = crypto.create_keypair(
        hashlib.sha256(b'aries-protocol-test-suite').digest()
    )
    subject_vk, subject_sk = crypto.create_keypair(
        hashlib.sha256(b'aries-protocol-test-subject').digest()
    )

    dispatcher = Dispatcher()

    a = StaticAgentConnection(
        args.endpoint,
        test_vk,
        subject_vk,
        subject_sk,
        dispatcher=dispatcher
    )

    connections = Connections(
        'http://localhost:{}'.format(args.port),
        dispatcher
    )

    a.route_module(connections)

    @a.route("test/protocol/1.0/test")
    async def simple_message(msg):
        print('Received:', msg.pretty_print())
        await a.send_async({
            "@type": "test/protocol/1.0/test",
            "msg": "pong"
        })

    async def handle(request):
        msg = await request.read()
        try:
            await a.handle(msg)
            raise web.HTTPAccepted
        except ValueError as err:
            print("Message not for main connection to test suite.", err)

        for key, conn in connections.connections.items():
            try:
                await conn.handle(msg)
                raise web.HTTPAccepted
            except ValueError as err:
                print(err)
                continue


        raise web.HTTPNotAcceptable()



    app = web.Application()
    app.add_routes([web.post('/', handle)])

    web.run_app(app, port=args.port)

if __name__ == '__main__':
    main()
