from vispy import gloo
from vispy import app
import numpy as np
import time
from math import *
import random


VERT_SHADER = """
#version 120
attribute vec3 position;
attribute vec4 color;
attribute float size;

varying vec4 v_color;
void main (void) {
    gl_Position = vec4(position, 1.0);
    v_color = color;
    gl_PointSize = size;
}
"""

FRAG_SHADER = """
#version 120
varying vec4 v_color;
void main()
{
    float x = 2.0*gl_PointCoord.x - 1.0;
    float y = 2.0*gl_PointCoord.y - 1.0;
    float a = 1.0 - (x*x + y*y);
    gl_FragColor = vec4(v_color.rgb, a*v_color.a);
}

"""


class Canvas(app.Canvas):

    def __init__(self, env):
        app.Canvas.__init__(self, keys='interactive')

        self.env = env
        self.N = env.N
        self.M = env.M

    def on_initialize(self, event):
        self.nodes = np.zeros(self.M + self.N, [('position', 'f4', 3),
                             ('color', 'f4', 4),
                             ('size', 'f4', 1)])

        self.agents = self.nodes[self.M:]
        self.goods = self.nodes[:self.M]

        self.agents['position'][:] = np.random.uniform(-0.25, +0.25, (self.N, 3))
        self.agents['size'] = 30
        self.agents['color'][:] = 0, 0, 1, 1

        self.goods['size'] = 50
        self.goods['color'][:] = 0, 1, 0, 1
        self.goods['position'][:] = np.random.uniform(-0.25, +0.25, (self.M, 3))

        self.program = gloo.Program(VERT_SHADER, FRAG_SHADER)
        # Set uniform and attribute
        self.vbo_position = gloo.VertexBuffer(self.nodes['position'].copy())
        self.vbo_color = gloo.VertexBuffer(self.nodes['color'].copy())
        self.vbo_size = gloo.VertexBuffer(self.nodes['size'].copy())

        self.program['color'] = self.vbo_color
        self.program['size'] = self.vbo_size
        self.program['position'] = self.vbo_position

        gloo.set_state(clear_color='white', blend=True,
               blend_func=('src_alpha', 'one_minus_src_alpha'))

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.size)

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('points')

    def on_mouse_press(self, event):
        #self.createGrid()
        pass

    def createGrid(self):
        root = sqrt(self.N)
        height = floor(root)
        width = ceil(root)
        step_x = 2 / width
        step_y = 2 / height
        #print(width, height, step_x, step_y)
        count = 0
        x = -1 + 0.5*step_x
        y = -1 + 0.5*step_y
        for p in range(self.N):
            self.agents['position'][p][0] = x
            self.agents['position'][p][1] = y
            self.agents['position'][p][2] = 0.0
            count += 1
            if count < width:
                x += step_x
            if count == width:
                x = -1 + 0.5 * step_x
                y += step_y
                count = 0
            self.env.agents_list[p].grid_pos = self.agents['position'][p]
            #agents[p].grid_pos = v_position[0]
        count = 1
        for agent in self.env.current_agents:
            current_agent = agent[0]
            good = agent[1]

            good.grid_pos = self.env.agents_list[current_agent].grid_pos
            self.goods['position'][good.id] = good.grid_pos
            self.goods['color'][good.id] = random.uniform(0, 1), random.uniform(0, 1), 0, 1
            count += 1
        self.vbo_position.set_data(self.nodes['position'].copy())
        self.vbo_color.set_data(self.nodes['color'].copy())

    def move(self, Q, good):
        distance_x = abs(good.grid_pos[0] - self.env.agents_list[Q].grid_pos[0])
        distance_y = abs(good.grid_pos[1] - self.env.agents_list[Q].grid_pos[1])
        step_x = distance_x / 20
        step_y = distance_y / 20
        good.grid_pos = self.env.agents_list[Q].grid_pos
        # for x in range(20):
        #     self.goods['position'][good.id][0] += step_x
        #     self.goods['position'][good.id][1] += step_y
        #     self.vbo_position.set_data(self.nodes['position'].copy())
        #     self.update()
        self.goods['position'][good.id] = good.grid_pos
        self.vbo_position.set_data(self.nodes['position'].copy())
        self.update()

    def updateColor(self, P, Q):
        P_percentage = self.env.agents_list[P].nr_transactions / self.env.nr_transactions
        Q_percentage = self.env.agents_list[Q].nr_transactions / self.env.nr_transactions
        self.agents['color'][P] = P_percentage, 0, 1 - P_percentage, 1
        self.agents['color'][Q] = Q_percentage, 0, 1 - Q_percentage, 1
        self.vbo_color.set_data(self.nodes['color'].copy())
        self.update()

if __name__ == '__main__':
    c = Canvas(10, 3)
    c.show()
    app.run()