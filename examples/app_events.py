#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ./app_events.py
# Author            : Pradeep Rajendran <pradeepunique1989@gmail.com>
# Date              : 16.09.2018
# Last Modified Date: 17.09.2018
# Last Modified By  : Pradeep Rajendran <pradeepunique1989@gmail.com>
import bpy
import asyncio
from asyncio import Task, coroutine, sleep
import blender_async
from blender_async import app_handler

# obj  = bpy.data.objects['Cube']
# mesh = obj.data
# vert = mesh.vertices[0]
# mat_world = obj.matrix_world
#
# pos_world = mat_world * vert.co
# pos_world.z += 0.1
# vert.co = mat_world.inverted() * pos_world

x = (1.1,2.2,3.3,4.4)
y = (1.1,2.2,3.3,4.4)
z = (1.1,2.2,3.3,4.4)
#
# for index,val in enumerate(x):
#         new_obj = bpy.data.objects.new('new_obj', None)
#             new_obj.location = (x[index],y[index],z[index])
#                 bpy.context.scene.objects.link(new_obj)
async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.read(255)).decode('utf8')
        print('\nHere %s\n'%(request))
        # response = str(eval(request)) + '\n'
        increment_x(bpy.data.objects['Cube'].location, float(request))
        response = "OK\n";
        writer.write(response.encode('utf8'))

# loop = asyncio.get_event_loop()
# loop.create_task(asyncio.start_server(handle_client, 'localhost', 15555))
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     loop.close()
def increment_x(loc, value):
    loc.x = value


async def main():
    await sleep(1)
    # obj = bpy.data.objects['Cube']
    # mesh = obj.data
    # vert = mesh.vertices[0]
    for i in range(3):
        print("Please change Frame")
        new_obj = bpy.data.objects.new('new_obj', None)
        new_obj.location = (x[i], y[i], z[i])
        bpy.context.scene.objects.link(new_obj)
        await app_handler("frame_change_post")



loop = blender_async.get_event_loop()
loop.create_task(main())
loop.create_task(asyncio.start_server(handle_client, 'localhost', 15555))
