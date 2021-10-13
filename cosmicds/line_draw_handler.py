from bqplot.marks import Scatter
from bqplot_image_gl import LinesGL
from bqplot_image_gl.interacts import MouseInteraction, mouse_events
from echo.core import add_callback

class LineDrawHandler(object):
    """
    This class handles the interactions for allowing a student to draw a line on a glue-jupyter scatter viewer.
    """

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
        self._app.state.bestfit_drawn = True

    def _message_handler(self, interaction, data, buffers):
        event_type = data['event']
        if event_type == 'mousemove':
            self._handle_mousemove(data)
        elif event_type == 'click':
            self._handle_click(data)

    def _handle_mousemove(self, data):

        figure = self._viewer.figure
        image = figure.marks[0]

        # Note that, since the image scales of the glue-jupyter scatter viewer are from 0 to 1
        # we don't need to worry about any normalization
        # If this weren't the case, we could grab the normalized coordinates via
        # 
        # image = self._viewer.figure.marks[0]
        # normalized_x = (domain_x - image.x[0]) / (image.x[1] - image.x[0])
        # normalized_y = (domain_y - image.y[0]) / (image.y[1] - image.y[0])
        domain = data['domain']
        x, y = domain['x'], domain['y']

        if self._drawn_line is None:
            self._drawn_line = LinesGL(x=[0, self._viewer.state.x_max], y=[0,0], scales=image.scales, colors=['black'])
            figure.marks = figure.marks + [self._drawn_line]
            self._follow_cursor = True
            
        if self._follow_cursor:
            self._drawn_line.x = [0, x]
            self._drawn_line.y = [0, y]


    def _handle_click(self, data):
        if self._follow_cursor:

            figure = self._viewer.figure

            # Clear the old endpoint
            domain = data['domain']
            x, y = domain['x'], domain['y']
            figure.marks = [mark for mark in figure.marks if mark is not self._endpt]
            
            # Add a new one
            image = figure.marks[0]
            endpt = Scatter(x=[x],
                              y=[y],
                              colors=['black'],
                              scales = {'x': image.scales['x'], 'y': image.scales['y']},
                              interactions = {'click':'select'}
                            )
            endpt.on_drag_start(self._on_endpt_drag_start)
            endpt.on_drag(self._on_endpt_drag)
            endpt.on_drag_end(self._on_endpt_drag_end)
            #endpt.opacities = [0]
            endpt.hovered_style = {'cursor' : 'grab'}
            endpt.enable_move = True
            figure.marks = figure.marks + [endpt]
            self._endpt = endpt

            # End drawing
            self._follow_cursor = False
            self._done_editing()

    def _on_endpt_drag_start(self, element, event):
        self._endpt.hovered_style = {'cursor' : 'grabbing'}

    def _on_endpt_drag_end(self, element, event):
        x = self._endpt.x[0]
        y = self._endpt.y[0]
        x_adj, y_adj = self._coordinates_in_bounds(x,y)
        if x_adj != x or y_adj != y:
            self._drawn_line.x = [0, x_adj]
            self._drawn_line.y = [0, y_adj]
            self._endpt.x = [x_adj]
            self._endpt.y = [y_adj]

    def _on_image_hover(self, element, event):
        if self._endpt is not None:
            self._endpt.opacities = [1]

    def _on_endpt_drag(self, element, event):
        point = event["point"]
        x, y = point["x"], point["y"]
        self._drawn_line.x = [0, x]
        self._drawn_line.y = [0, y]

    def _draw_on_changed(self, draw_on):
        have_endpt = self._endpt is not None

        # if have_endpt:
        #     self._endpt.opacities = [int(draw_on)]
        #     self._endpt.hovered_style = {'cursor' : 'grab'} if draw_on else {}
        #     self._endpt.enable_move = draw_on

        if have_endpt:
            self._viewer.figure.interaction = None
        elif draw_on:
            self._viewer.figure.interaction = self._interaction
        else:
            self._viewer.figure.interaction = self._original_interaction

    def _coordinates_in_bounds(self, x, y):
        """
        If a student drags the endpoint beyond the viewer bounds, we want to bring it back inside.
        This function, given x and y coordinates of a chosen endpoint, this function finds the
        coordinates of the point where their line crosses the boundary of the viewer.
        """

        # Get the current viewer bounds
        state = self._viewer.state
        x_min, x_max, y_min, y_max = state.x_min, state.x_max, state.y_min, state.y_max

        # If the point is in bounds, do nothing
        if x > x_min and x < x_max and y > y_min and y < y_max:
            return x, y

        # Vertical line
        if x == 0:
            y_adj = y_min if y < y_min else y_max
            return x, y_adj

        # Horizontal line
        if y == 0:
            x_adj = x_min if x < x_min else x_max
            return x_adj, y

        t1 = x_min / x
        t2 = x_max / x
        t3 = y_min / y
        t4 = y_max / y
        ts = [t for t in [t1,t2,t3,t4] if t > 0 and t < 1]
        t = min(ts or [0])

        return x * t, y * t


    def clear(self):
        figure = self._viewer.figure
        to_remove = [x for x in [self._drawn_line, self._endpt] if x is not None]
        figure.marks = [mark for mark in figure.marks if mark not in to_remove]
        self._drawn_line = None
        self._endpt = None
        self._app.state.draw_on = False
        self._app.state.bestfit_drawn = False
