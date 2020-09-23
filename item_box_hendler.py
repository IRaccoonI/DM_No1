from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from drag_item import DragBehavior

class DragLabelItem(DragBehavior, Label):
    pass

# Class 4 handling item boxes

def create_item(val, drag_pinger, put_handler):
    item = DragLabelItem(text = val, drag_pinger=drag_pinger, put_handler=put_handler)

    return item

def do_nothing():
    pass

class ItemBoxHandler():
    def __init__(self, item_box, hold_left, hold_right, hold_center):
        self.item_box = item_box
        self.set = set()

        def drag_pinger(pos):
            if pos == 'center':
                hold_center()
            elif pos == 'right':
                hold_right()
            elif pos == 'left':
                hold_left()
        
        self.drag_pinger = drag_pinger
    
    def add_put_handler(self, put_left, put_right):
        def put_handler(pos, el):
            if pos == 'right':
                put_right(el)
            elif pos == 'left':
                put_left(el)
        self.put_handler = put_handler

    def add_by_el(self, el):
        val = el.text
        self._add(val)

    def add_by_val(self, val):
        val = str(val)
        self._add(val)
    
    def _add(self, val):
        if val in self.set:
            return
        new_widget = create_item(val, self.drag_pinger, self.put_handler)
        self.item_box.add_widget(new_widget)
        self.set.add(val)


    def set_list(self, lst):
        self.clear()
        for i in lst:
            self.add_by_val(i)
    
    def clear(self):
        self.item_box.clear_widgets()
        self.set.clear()

    def remove_by_el(self, el):
        self.set.remove(el.text)
        self.item_box.remove_widget(el)

    def get_set(self):
        return self.set
    
class ItemsGroup():
    def __init__(self, data):
        self.data = data

        def muffle_all():
            data['center']['wrapper'].muffle()
            data['right']['wrapper'].muffle()
            data['left']['wrapper'].muffle()

        _u = ItemBoxHandler(
            data['center']['box'],
            hold_left = lambda: data['left']['wrapper'].hightlight(),
            hold_center = lambda: muffle_all(),
            hold_right = lambda: data['right']['wrapper'].hightlight()
        )
        self._u = _u
        _a = ItemBoxHandler(
            data['left']['box'],
            hold_left = lambda: do_nothing(),
            hold_center = lambda: muffle_all(),
            hold_right = lambda: data['center']['wrapper'].hightlight(),
        )
        self._a = _a
        _b = ItemBoxHandler(
            data['right']['box'],
            hold_left = lambda: data['center']['wrapper'].hightlight(),
            hold_center = lambda: muffle_all(),
            hold_right = lambda: do_nothing(),
        )
        self._b = _b

        _u.add_put_handler(
            put_left = lambda el: _a.add_by_el(el),
            put_right = lambda el: _b.add_by_el(el),
        )
        _a.add_put_handler(
            put_left = lambda el: do_nothing(),
            put_right = lambda el: _a.remove_by_el(el),
        )
        _b.add_put_handler(
            put_left = lambda el: _b.remove_by_el(el),
            put_right = lambda el: do_nothing(),
        )

    def new_universum(self, lst):
        self._u.set_list(lst)
        self._a.clear()
        self._b.clear()

    def get_sets(self):
        return [self._u.get_set(), self._a.get_set(), self._b.get_set()]


    #'center': {
    #         'wrapper': wrapper_dist_lst_box_u,
    #         'box': dist_lst_box_u
    #     },
    #'left': {
    #         'wrapper': wrapper_dist_lst_box_a,
    #         'box': dist_lst_box_a
    #     },
    #'right': {
    #         'wrapper': wrapper_dist_lst_box_b,
    #         'box': dist_lst_box_b
    #     }