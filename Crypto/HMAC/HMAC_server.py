#!/usr/bin/env python3
import asyncio
import websockets
import hashlib


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


async def serve(websocket):
    shared_key = "supersecret"
    await websocket.send("Please provide me a comma-separated message,hmac")
    client_data = await websocket.recv()
    client_message, client_hmac = client_data.split(",", 1)
    server_hmac = gen_sha256_hmac(client_message, shared_key)
    if client_hmac == server_hmac:
        await websocket.send("Access granted!")
    else:
        await websocket.send("Access denied!")


async def main():
    async with websockets.serve(serve, "localhost", 1234):
        print("Server started!")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
