#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ./examples/app_events.py
# Author            : Pradeep Rajendran <pradeepunique1989@gmail.com>
# Date              : 16.09.2018
# Last Modified Date: 18.09.2018
# Last Modified By  : Pradeep Rajendran <pradeepunique1989@gmail.com>
import bpy
import asyncio
from asyncio import Task, coroutine, sleep
import blender_async
from blender_async import app_handler
import warnings

async def handle_client(reader, writer):
    request = ""
    while False == request.startswith('quit'):
        request = (await reader.readline()).decode('utf8')
        # print(request)
        resp = "OK\n"
        cmd = request.split('#')
        if '0' == cmd[0]:
            # Execute command
            execute(cmd[1])
        elif '1' == cmd[0]:
            resp = evaluate(cmd[1])
        else:
            warnings.warn('Bad command')

        writer.write(resp.encode('utf8'))
    return

def execute(command):
    exec(command)

def evaluate(expression):
    response = str(eval(expression)) + '\n';
    return response

loop = blender_async.get_event_loop()
loop.create_task(asyncio.start_server(handle_client, 'localhost', 15555))


# async def main():
#     await sleep(1)
#     # obj = bpy.data.objects['Cube']
#     # mesh = obj.data
#     # vert = mesh.vertices[0]
#     for i in range(3):
#         print("Please change Frame")
#         new_obj = bpy.data.objects.new('new_obj', None)
#         new_obj.location = (x[i], y[i], z[i])
#         bpy.context.scene.objects.link(new_obj)
#         await app_handler("frame_change_post")
# loop.create_task(main())
