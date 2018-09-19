#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : app_events.py
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
        # print('\nHere %s\n'%(request))
        # response = str(eval(request)) + '\n'

        # coords = list(map(float, request.split(',')))
        # print(coords)
        # make_box(coords)
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

def execute(command):
    exec(command)

def evaluate(expression):
    response = str(eval(expression)) + '\n';
    return response

def set_location(loc, new_location):
    loc.x = new_location[0]
    loc.y = new_location[1]
    loc.z = new_location[2]

def make_box(new_location):
    bpy.ops.mesh.primitive_cube_add(location=new_location);


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
