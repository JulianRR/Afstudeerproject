from vispy import gloo, visuals
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
varying float v_radius;
varying float v_linewidth;
varying float v_antialias;
void main (void) {
    v_radius = size;
    v_linewidth = 1.0;
    v_antialias = 1.0;
    
    gl_Position = vec4(position, 1.0);
    v_color = color;
    gl_PointSize = (v_radius + v_linewidth + 1.5*v_antialias);
}
"""

FRAG_SHADER = """
#version 120
varying vec4 v_color;
varying float v_radius;
varying float v_linewidth;
varying float v_antialias;
void main()
{
    float s = 2.0*(v_radius + v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;
    float r = length((gl_PointCoord.xy - vec2(0.5,0.5))*s);
    float d = abs(r - v_radius) - t;

    float x = 2.0*gl_PointCoord.x - 1.0;
    float y = 2.0*gl_PointCoord.y - 1.0;
    float a = 1.0 - (x*x + y*y);

    if( d < 0.0 )
        gl_FragColor = v_color;
    else
    {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > v_radius)
            gl_FragColor = vec4(v_color.rgb, alpha*v_color.a);
        else
            gl_FragColor = v_color;
    }
    
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

        self.agents = self.nodes[:self.N]
        self.goods = self.nodes[self.N:]

        self.agents['position'][:] = np.random.uniform(-0.25, +0.25, (self.N, 3))
        self.agents['size'] = 30
        self.agents['color'][:] = 0, 0, 1, 1

        self.goods['size'] = 20
        self.goods['color'][:] = 0, 1, 0, 1
        self.goods['position'][:] = np.random.uniform(-0.25, +0.25, (self.M, 3))

        #Text
        self.width = self.size[0]
        self.height = self.size[1]
        self.font_size = 12.
        self.text = [visuals.TextVisual(str(x), bold=True, color='white') for x in range(self.N)]
        self.tr_sys = visuals.transforms.TransformSystem(self)

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
        for t in self.text:
            t.draw(self.tr_sys)

    def on_mouse_press(self, event):
        #self.createGrid()
        pass

    def apply_zoom(self):
        count = 0
        for t in self.text:
            t.font_size = self.font_size
            t.pos = (1 + self.agents['position'][count][0]) * (self.width / 2), (1 + -self.agents['position'][count][1]) * (self.height / 2)
            count += 1
        self.update()

    def createGrid(self):
        root = sqrt(self.N)
        height = ceil(root)
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

            good.grid_pos = self.env.agents_list[current_agent.id].grid_pos
            self.goods['position'][good.id] = good.grid_pos
            self.goods['color'][good.id] = 0, 1, 0, 1
            #self.goods['color'][good.id] = 0, 1, 0, 1
            count += 1
        self.vbo_position.set_data(self.nodes['position'].copy())
        self.vbo_color.set_data(self.nodes['color'].copy())
        self.apply_zoom()

    def move(self, Q, good):
        distance_x = abs(good.grid_pos[0] - self.env.agents_list[Q.id].grid_pos[0])
        distance_y = abs(good.grid_pos[1] - self.env.agents_list[Q.id].grid_pos[1])
        step_x = distance_x / 20
        step_y = distance_y / 20
        good.grid_pos = self.env.agents_list[Q.id].grid_pos
        # for x in range(20):
        #     self.goods['position'][good.id][0] += step_x
        #     self.goods['position'][good.id][1] += step_y
        #     self.vbo_position.set_data(self.nodes['position'].copy())
        #     self.update()
        self.goods['position'][good.id] = good.grid_pos
        self.vbo_position.set_data(self.nodes['position'].copy())
        self.update()

    def updateColor(self):
        for x in range(self.N):
            P_percentage = self.env.agents_list[x].nr_transactions / self.env.nr_transactions
            #Q_percentage = self.env.agents_list[Q.id].nr_transactions / self.env.nr_transactions
            self.agents['color'][x] = P_percentage, 0, 1 - P_percentage, 1
            #self.agents['color'][Q.id] = Q_percentage, 0, 1 - Q_percentage, 1
            #self.vbo_color.set_data(self.nodes['color'].copy())
        for y in range(self.M):
            if self.env.goods_list[y].life == 0:
                self.goods['color'][y][3] = 0.5
            else:
                self.goods['color'][y][3] = 1
        self.vbo_color.set_data(self.nodes['color'].copy())
        self.update()
        # P_percentage = self.env.agents_list[P.id].nr_transactions / self.env.nr_transactions
        # Q_percentage = self.env.agents_list[Q.id].nr_transactions / self.env.nr_transactions
        # self.agents['color'][P.id] = P_percentage, 0, 1 - P_percentage, 1
        # self.agents['color'][Q.id] = Q_percentage, 0, 1 - Q_percentage, 1
        # self.vbo_color.set_data(self.nodes['color'].copy())
        # self.update()

if __name__ == '__main__':
    c = Canvas(10, 3)
    c.show()
    app.run()