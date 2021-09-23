from bqplot.marks import Scatter
from bqplot_image_gl import LinesGL
from bqplot_image_gl.interacts import MouseInteraction, mouse_events
from echo.core import add_callback
from math import sqrt

class LineDrawHandler(object):

    def __init__(self, app, viewer):
        self._app = app
        self._viewer = viewer
        self._follow_cursor = False
        self._drawn_line = None
        self._endpt = None

        figure = viewer.figure
        self._original_interaction = figure.interaction
        scales_image = figure.marks[0].scales
        self._interaction = MouseInteraction(x_scale=scales_image['x'], y_scale=scales_image['y'], move_throttle=70, next=None,
                                events=mouse_events)
        self._interaction.on_msg(self._message_handler)

        add_callback(self._app.state, 'draw_on', self._draw_on_changed)

    def _done_editing(self):
        self._app.state.draw_on = False

    def _message_handler(self, interaction, data, buffers):
        event_type = data['event']
        if event_type == 'mousemove':
            self._handle_mousemove(data)
        elif event_type == 'click':
            self._handle_click(data)

    def _circle_radius(self):
        viewer_range_x = self.viewer.state.x_max - self.viewer.state.x_min
        viewer_range_y = self.viewer.state.y_max - self.viewer.state.y_min
        return 0.01 * max(viewer_range_x, viewer_range_y)

    def _handle_mousemove(self, data):

        image = self.figure.marks[0]
        domain = data['domain']
        x, y = domain['x'], domain['y']

        if self._drawn_line is None:
            self._drawn_line = LinesGL(x=[0, self.viewer.state.x_max], y=[0,0], scales=image.scales, colors=['black'])
            self.figure.marks = self.figure.marks + [self._drawn_line]
            self._follow_cursor = True
        elif self._endpt is not None:
            delta_x = x - self._endpt.x[0]
            delta_y = y - self._endpt.y[0]
            dist = sqrt(delta_x ** 2 + delta_y ** 2)
            #opacity = 1 if dist <= self._circle_radius() else 0
            
        if self._follow_cursor:
            self._drawn_line.x = [0, x]
            self._drawn_line.y = [0, y]


    def _handle_click(self, data):
        if self._follow_cursor:

            # Clear the old endpoint
            domain = data['domain']
            x, y = domain['x'], domain['y']
            self.figure.marks = [mark for mark in self.figure.marks if mark is not self._endpt]
            
            # Add a new one
            image = self.figure.marks[0]
            endpt = Scatter(x=[x],
                              y=[y],
                              colors=['black'],
                              scales = {'x': image.scales['x'], 'y': image.scales['y']},
                              interactions = {'click':'select'}
                            )
            endpt.on_element_click(self._on_endpt_click)
            endpt.opacities = [0]

            # If we don't put the endpoint first, it doesn't receive the click event
            # Something (the ImageGL?) in front of it seems to be capturing that event
            self.figure.marks = [endpt] + self.figure.marks
            self._endpt = endpt
            print("Making endpt: ", self._endpt)

            # End drawing
            self._follow_cursor = False
            self._done_editing()

    def _on_endpt_click(self, element, event):
        print(element, event)
        if not self._app.state.draw_on:
            return

        self._viewer.figure.interaction = self._interaction
        self._follow_cursor = True
        self._endpt.opacities = [0]

    def _draw_on_changed(self, draw_on):
        if draw_on:
            if self._endpt is not None:
                self._viewer.figure.interaction = None
                self._endpt.opacities = [1]
            else:
                self._viewer.figure.interaction = self._interaction
        else:
            self._viewer.figure.interaction = self._original_interaction

    @property
    def viewer(self):
        return self._viewer

    @property
    def figure(self):
        return self.viewer.figure

    @property
    def image(self):
        return self.figure.marks[0]
