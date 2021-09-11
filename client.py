#!/usr/bin/env python

# import asyncio
# import websockets

# async def hello():
#     async with websockets.connect("ws://192.168.1.37:80") as websocket:
#         await websocket.send("move;15;0;0;0;0")

# asyncio.run(hello())

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.37', 80))
s.sendall("move;15;0;0;0;0".encode("utf-8"))
s.close()
