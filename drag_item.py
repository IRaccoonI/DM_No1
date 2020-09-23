from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.config import Config
from kivy.metrics import sp
from functools import partial

# When we are generating documentation, Config doesn't exist
_scroll_timeout = _scroll_distance = 0
if Config:
    _scroll_timeout = Config.getint('widgets', 'scroll_timeout')
    _scroll_distance = Config.getint('widgets', 'scroll_distance')


class DragBehavior(object):
    '''
    The DragBehavior `mixin <https://en.wikipedia.org/wiki/Mixin>`_ provides
    Drag behavior. When combined with a widget, dragging in the rectangle
    defined by :attr:`drag_rectangle` will drag the widget. Please see
    the :mod:`drag behaviors module <kivy.uix.behaviors.drag>` documentation
    for more information.

    .. versionadded:: 1.8.0
    '''

    drag_distance = NumericProperty(_scroll_distance)
    '''Distance to move before dragging the :class:`DragBehavior`, in pixels.
    As soon as the distance has been traveled, the :class:`DragBehavior` will
    start to drag, and no touch event will be dispatched to the children.
    It is advisable that you base this value on the dpi of your target device's
    screen.

    :attr:`drag_distance` is a :class:`~kivy.properties.NumericProperty` and
    defaults to the `scroll_distance` as defined in the user
    :class:`~kivy.config.Config` (20 pixels by default).
    '''

    drag_timeout = NumericProperty(_scroll_timeout)
    '''Timeout allowed to trigger the :attr:`drag_distance`, in milliseconds.
    If the user has not moved :attr:`drag_distance` within the timeout,
    dragging will be disabled, and the touch event will be dispatched to the
    children.

    :attr:`drag_timeout` is a :class:`~kivy.properties.NumericProperty` and
    defaults to the `scroll_timeout` as defined in the user
    :class:`~kivy.config.Config` (55 milliseconds by default).
    '''

    drag_rect_x = NumericProperty(0)
    '''X position of the axis aligned bounding rectangle where dragging
    is allowed (in window coordinates).

    :attr:`drag_rect_x` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.
    '''

    drag_rect_y = NumericProperty(0)
    '''Y position of the axis aligned bounding rectangle where dragging
    is allowed (in window coordinates).

    :attr:`drag_rect_Y` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.
    '''

    drag_rect_width = NumericProperty(100)
    '''Width of the axis aligned bounding rectangle where dragging is allowed.

    :attr:`drag_rect_width` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 100.
    '''

    drag_rect_height = NumericProperty(100)
    '''Height of the axis aligned bounding rectangle where dragging is allowed.

    :attr:`drag_rect_height` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 100.
    '''

    drag_rectangle = ReferenceListProperty(drag_rect_x, drag_rect_y,
                                           drag_rect_width, drag_rect_height)
    '''Position and size of the axis aligned bounding rectangle where dragging
    is allowed.

    :attr:`drag_rectangle` is a :class:`~kivy.properties.ReferenceListProperty`
    of (:attr:`drag_rect_x`, :attr:`drag_rect_y`, :attr:`drag_rect_width`,
    :attr:`drag_rect_height`) properties.
    '''

    drag_pinger = ObjectProperty(None, allownone=True)
    put_handler = ObjectProperty(None, allownone=True)


    def __init__(self, **kwargs):
        self._drag_touch = None
        super(DragBehavior, self).__init__(**kwargs)

    def _get_uid(self, prefix='sv'):
        return '{0}.{1}'.format(prefix, self.uid)

    def on_touch_down(self, touch):
        self._start_state = [self.x, self.y]
        xx, yy, w, h = self.drag_rectangle
        x, y = touch.pos
        if not self.collide_point(x, y):
            touch.ud[self._get_uid('svavoid')] = True
            return super(DragBehavior, self).on_touch_down(touch)
        if self._drag_touch or ('button' in touch.profile and
                                touch.button.startswith('scroll')) or\
                not ((xx < x <= xx + w) and (yy < y <= yy + h)):
            return super(DragBehavior, self).on_touch_down(touch)

        # no mouse scrolling, so the user is going to drag with this touch.
        self._drag_touch = touch
        uid = self._get_uid()
        touch.grab(self)
        touch.ud[uid] = {
            'mode': 'unknown',
            'dx': 0,
            'dy': 0}
        Clock.schedule_once(self._change_touch_mode,
                            self.drag_timeout / 1000.)
        return True

    def on_touch_move(self, touch):
        if self._get_uid('svavoid') in touch.ud or\
                self._drag_touch is not touch:
            return super(DragBehavior, self).on_touch_move(touch) or\
                self._get_uid() in touch.ud
        if touch.grab_current is not self:
            return True

        uid = self._get_uid()
        ud = touch.ud[uid]
        mode = ud['mode']
        if mode == 'unknown':
            ud['dx'] += abs(touch.dx)
            # ud['dy'] += abs(touch.dy)
            if ud['dx'] > sp(self.drag_distance):
                mode = 'drag'
            # if ud['dy'] > sp(self.drag_distance):
            #     mode = 'drag'
            ud['mode'] = mode
        if mode == 'drag':
            self.x += touch.dx
            # self.y += touch.dy
        if self.x - self._start_state[0] > self.width / 3:
            self.drag_pinger('right')
        elif self.x - self._start_state[0] < -self.width / 3:
            self.drag_pinger('left')
        else:
            self.drag_pinger('center')

        return True

    def on_touch_up(self, touch):
        if self._get_uid('svavoid') in touch.ud:
            return super(DragBehavior, self).on_touch_up(touch)

        if self._drag_touch and self in [x() for x in touch.grab_list]:
            touch.ungrab(self)
            self._drag_touch = None
            ud = touch.ud[self._get_uid()]
            if ud['mode'] == 'unknown':
                super(DragBehavior, self).on_touch_down(touch)
                Clock.schedule_once(partial(self._do_touch_up, touch), .1)
        else:
            if self._drag_touch is not touch:
                super(DragBehavior, self).on_touch_up(touch)

        if '_start_state' in self.__dict__:
        
            if self.x - self._start_state[0] > self.width / 3:
                self.put_handler('right', self)
            elif self.x - self._start_state[0] < -self.width / 3:
                self.put_handler('left', self)

            [self.x, self.y] = self._start_state
            self.drag_pinger('center')

        return self._get_uid() in touch.ud

    def _do_touch_up(self, touch, *largs):
        super(DragBehavior, self).on_touch_up(touch)
        # don't forget about grab event!
        for x in touch.grab_list[:]:
            touch.grab_list.remove(x)
            x = x()
            if not x:
                continue
            touch.grab_current = x
            super(DragBehavior, self).on_touch_up(touch)
        touch.grab_current = None

    def _change_touch_mode(self, *largs):
        if not self._drag_touch:
            return
        uid = self._get_uid()
        touch = self._drag_touch
        ud = touch.ud[uid]
        if ud['mode'] != 'unknown':
            return
        touch.ungrab(self)
        self._drag_touch = None
        touch.push()
        touch.apply_transform_2d(self.parent.to_widget)
        super(DragBehavior, self).on_touch_down(touch)
        touch.pop()
        return