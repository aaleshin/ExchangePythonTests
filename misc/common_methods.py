import websockets
import random
import string


async def ws_request(uri, req):
    async with websockets.connect(uri) as ws:
        await ws.send(req)
        return await ws.recv()


def generate_random_string():
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(6))
    return rand_string
