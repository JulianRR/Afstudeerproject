from vispy import gloo
from vispy import app
import numpy as np
import time

# Create vetices
n = 10
v_position = 0.25 * np.random.randn(n, 3).astype(np.float32)
#print(v_position)
v_color = np.random.uniform(0, 1, (n, 3)).astype(np.float32)
v_color = [[ 0.2, 1.0, 0.4] for i in range(n)]
#print(v_color)
v_size = np.random.uniform(2, 12, (n, 1)).astype(np.float32)
v_size = [[10.0] for i in range(n)]
#print(v_size)

VERT_SHADER = """
attribute vec3  a_position;
attribute vec3  a_color;
attribute float a_size;

varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_radius;
varying float v_linewidth;
varying float v_antialias;

void main (void) {
    v_radius = a_size;
    v_linewidth = 1.0;
    v_antialias = 1.0;
    v_fg_color  = vec4(0.0,0.0,0.0,0.5);
    v_bg_color  = vec4(a_color,    1.0);

    gl_Position = vec4(a_position, 1.0);
    gl_PointSize = 2.0*(v_radius + v_linewidth + 1.5*v_antialias);
}
"""

FRAG_SHADER = """
#version 120

varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_radius;
varying float v_linewidth;
varying float v_antialias;
void main()
{
    float size = 2.0*(v_radius + v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;
    float r = length((gl_PointCoord.xy - vec2(0.5,0.5))*size);
    float d = abs(r - v_radius) - t;
    if( d < 0.0 )
        gl_FragColor = v_fg_color;
    else
    {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > v_radius)
            gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
        else
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
    }
}
"""


class Canvas(app.Canvas):

    def __init__(self):
        app.Canvas.__init__(self, keys='interactive')

    def on_initialize(self, event):
        self.program = gloo.Program(VERT_SHADER, FRAG_SHADER)
        # Set uniform and attribute
        self.program['a_color'] = gloo.VertexBuffer(v_color)
        #self.program['u_color'] = 0.2, 1.0, 0.4, 1
        self.program['a_position'] = gloo.VertexBuffer(v_position)
        self.program['a_size'] = gloo.VertexBuffer(v_size)
        gloo.set_state(clear_color='white', blend=True,
                       blend_func=('src_alpha', 'one_minus_src_alpha'))

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.size)

    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        #v_position = 0.25 * np.random.randn(n, 3).astype(np.float32)
        #self.program['a_position'] = gloo.VertexBuffer(v_position)
        self.program.draw('points')

    def on_mouse_move(self, event):
        if event.is_dragging:
            button = event.press_event.button

            if button == 1:
                self.update()

    def updateVis(self):
        #v_position = 0.25 * np.random.randn(n, 3).astype(np.float32)
        print(v_position[0])
        for i in range(5):
            time.sleep(0.05)
            v_position[0][0] = 1.0
            v_position[0][1] = 1.0
            v_position[0][2] = 1.0
            v_color[0] = [0.0, 1.0, 0.0]
            v_position[1][0] = 0
            v_position[1][1] = 0
            v_position[1][2] = 0
            v_color[1] = [1.0, 0.0, 0.0]
            v_position[2][0] = -1.0
            v_position[2][1] = -1.0
            v_position[2][2] = -1.0
            v_color[2] = [0.0, 0.0, 1.0]
            self.program['a_color'] = gloo.VertexBuffer(v_color)
            self.program['a_position'] = gloo.VertexBuffer(v_position)
            self.update()


if __name__ == '__main__':
    c = Canvas()
    c.show()
    app.run()