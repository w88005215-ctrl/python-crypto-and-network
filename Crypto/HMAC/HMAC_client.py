#!/usr/bin/env python3
import asyncio
import websockets
import hashlib

MY_NAME = "Muse"


def gen_sha256_hmac(message, key):
    blocksize = 64
    trans_5C = bytes((x ^ 0x5C) for x in range(256))
    trans_36 = bytes((x ^ 0x36) for x in range(256))
    key_hex = key.encode().hex()[2:]
    key_bytes = bytes.fromhex(key_hex).ljust(blocksize, b"\0")
    xored_ipad = key_bytes.translate(trans_36)
    h1 = hashlib.sha256(xored_ipad + message.encode())
    xored_opad = key_bytes.translate(trans_5C)
    return hashlib.sha256(xored_opad + h1.digest()).hexdigest()


async def try_auth(uri):
    async with websockets.connect(uri) as websocket:
        shared_key = "supersecret"
        message = f"Hello from {MY_NAME}"
        welcome_message = await websocket.recv()
        print(f"Server answered: {welcome_message}")
        message_hmac = gen_sha256_hmac(message, shared_key)
        client_data = f"{message},{message_hmac}"
        await websocket.send(client_data)
        answer = await websocket.recv()
        print(answer)


if __name__ == "__main__":
    asyncio.run(try_auth("ws://localhost:1234"))
