from bqplot import ScatterGL
from bqplot_image_gl import LinesGL
from math import sqrt

class LineDrawHandler(object):

    def __init__(self, viewer, done_editing):
        self._viewer = viewer
        self._done_editing = done_editing
        self._follow_pointer = False
        self._drawn_line = None
        self._drawn_line_endpt = None

    def message_handler(self, interaction, data, buffers):
        event_type = data['event']
        if event_type == 'mousemove':
            self._handle_mousemove(data)
        elif event_type == 'click':
            self._handle_click(data)


    def _normalized_coordinates(self, data):
        image = self.image
        domain = data['domain']
        domain_x = domain['x']
        domain_y = domain['y']
        normalized_x = (domain_x - image.x[0]) / (image.x[1] - image.x[0])
        normalized_y = (domain_y - image.y[0]) / (image.y[1] - image.y[0])
        return normalized_x, normalized_y

    def _circle_radius(self):
        viewer_range_x = self.viewer.state.x_max - self.viewer.state.x_min
        viewer_range_y = self.viewer.state.y_max - self.viewer.state.y_min
        return 0.01 * max(viewer_range_x, viewer_range_y)

    def _handle_mousemove(self, data):

        image = self.figure.marks[0]
        circle_radius = 10 # TODO: A real value here
        normalized_x, normalized_y = self._normalized_coordinates(data)
        print(self._drawn_line_endpt)

        if self._drawn_line is None:
            self._drawn_line = LinesGL(x=[0, self.viewer.state.x_max], y=[0,0], scales=image.scales, colors=['black'])
            self.figure.marks = self.figure.marks + [self._drawn_line]
            self._follow_pointer = True
        elif self._drawn_line_endpt is not None:
            delta_x = normalized_x - self._drawn_line_endpt.x[0]
            delta_y = normalized_y - self._drawn_line_endpt.y[0]
            dist = sqrt(delta_x ** 2 + delta_y ** 2)
            opacity = 1 if dist <= self._circle_radius() else 0
            print(opacity)
            self._drawn_line_endpt.opacities = [opacity]
            print(dist)
            print(self._circle_radius())
            
        if self._follow_pointer:
            self._drawn_line.x = [0, normalized_x]
            self._drawn_line.y = [0, normalized_y]


    def _handle_click(self, data):
        if self._follow_pointer:

            # Clear the old endpoint
            normalized_x, normalized_y = self._normalized_coordinates(data)
            self.figure.marks = [mark for mark in self.figure.marks if mark is not self._drawn_line_endpt]
            
            # Add a new one
            endpt = ScatterGL(x=[normalized_x], y=[normalized_y], color=['black'])
            endpt.opacities = [1]
            self.figure.marks = self.figure.marks + [endpt]
            self._drawn_line_endpt = endpt
            print("Making endpt: ", self._drawn_line_endpt)

            # End drawing
            self._follow_pointer = False
            self._done_editing()
        elif self._drawn_line_endpt.visible:
            self._follow_pointer = True
            self._drawn_line_endpt.opacities = [1]

    @property
    def viewer(self):
        return self._viewer

    @property
    def figure(self):
        return self.viewer.figure

    @property
    def image(self):
        return self.figure.marks[0]