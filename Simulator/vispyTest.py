from vispy import gloo, visuals
from vispy import app
import numpy as np

# Create vetices
n = 10000
v_position = 0.25 * np.random.randn(n, 3).astype(np.float32)
v_color = np.random.uniform(0, 1, (n, 3)).astype(np.float32)
v_size = np.random.uniform(2, 12, (n, 1)).astype(np.float32)

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

        self.font_size = 48.
        self.text = [visuals.TextVisual(str(1), bold=True), visuals.TextVisual(str(2), bold=True), visuals.TextVisual(str(3), bold=True)]
        self.tr_sys = visuals.transforms.TransformSystem(self)
        self.apply_zoom()
        # Set uniform and attribute
        self.program['a_color'] = gloo.VertexBuffer(v_color)
        self.program['a_position'] = gloo.VertexBuffer(v_position)
        self.program['a_size'] = gloo.VertexBuffer(v_size)
        gloo.set_state(clear_color='white', blend=True,
                       blend_func=('src_alpha', 'one_minus_src_alpha'))

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.size)

    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        #self.program.draw('points')
        for tex in self.text:
            tex.draw(self.tr_sys)

    def apply_zoom(self):
        #self.text.text = '%s pt' % round(self.font_size, 1)
        for t in self.text:
            t.font_size = self.font_size
            t.pos = self.size[0] , self.size[1] 
            print(t.pos)
        self.update()


if __name__ == '__main__':
    c = Canvas()
    c.show()
    app.run()