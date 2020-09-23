from kivy.app import App

# set window size !!! TEMP !!!
import kivy
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')

# import widgets

from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout

from kivy.properties import NumericProperty, Property
from kivy.graphics import Color, Rectangle


from item_box_hendler import ItemBoxHandler, DragLabelItem, ItemsGroup


#inic class 4 customize appearance

class MainLayout(BoxLayout):
    pass

class ReportLayout(BoxLayout):
    pass

class SetLayout(BoxLayout):
    pass

class GOTOButton(Button):
    pass

class IntSlider(Slider):
    pass

class SubmitButton(Button):
    pass

class DistributionBox(BoxLayout):
    pass

class DistributionListBox(BoxLayout):
    pass

class MainListBoxSet(BoxLayout):
    brightness = NumericProperty(1)

    def hightlight(self):
        if self.brightness != 1.5:
            self.brightness = 1.5
    
    def muffle(self):
        if self.brightness != 1.0:
            self.brightness = 1.0

class SubListBoxSet(BoxLayout):
    brightness = NumericProperty(1)

    def hightlight(self):
        if self.brightness != 2.0:
            self.brightness = 2.0
    
    def muffle(self):
        if self.brightness != 1.0:
            self.brightness = 1.0

class ItemsBox(GridLayout):
    pass

class ReportGrid(GridLayout):
    pass

class ReportGridItem(BoxLayout):
    pass

# Builder.load_file('./main.kv')

# Apppppp

class MainApp(App):
    def build(self):

        root = BoxLayout(
            orientation='vertical',
            size=(Window.width, Window.height)
        )

        ###### Init All Screen ######

        report_layout = ReportLayout(
            orientation='vertical',
            padding=15
        )
        set_layout = SetLayout(
            orientation='vertical',
            padding=15
        )
        info_layout = SetLayout(
            orientation='vertical',
            padding=15
        )

        def set_main_layout(layout):
            root.clear_widgets()
            root.add_widget(layout)

        ### Buttons 4 them ###

        btn_to_set_layout = GOTOButton(text='go to set')
        btn_to_info_layout = GOTOButton(text='go to info')
        btn_to_report_layout = GOTOButton(text='go to report')
        btn2_to_report_layout = GOTOButton(text='go to report')
        btn_to_set_layout.bind(on_press=lambda a: set_main_layout(set_layout))
        btn_to_report_layout.bind(on_press=lambda a: set_main_layout(report_layout))
        btn_to_info_layout.bind(on_press=lambda a: set_main_layout(info_layout))
        btn2_to_report_layout.bind(on_press=lambda a: set_main_layout(report_layout))

        ###### SLider ######

        slider_box = BoxLayout(
            orientation='vertical',
            size_hint=[1, None],
            height=100,
        )
        first_slider_line = BoxLayout()

        int_slider = IntSlider(min=1, max=15, value=5, step=1)

        slider_val_label = Label(
            text='Length of Union: ' + str(int_slider.value),
            size_hint=[None, 1],
            width=150
        )
        
        def on_int_slider_val_change(instance, value):
            slider_val_label.text = 'Length of Union: ' + str(value)

        int_slider.bind(value=on_int_slider_val_change)

        second_slider_line = BoxLayout()
        slider_submit_button = SubmitButton(text='Submit')

        first_slider_line.add_widget(slider_val_label)
        first_slider_line.add_widget(int_slider)

        second_slider_line.add_widget(slider_submit_button)

        slider_box.add_widget(first_slider_line)
        slider_box.add_widget(second_slider_line)

        ###### Distribution elements between all ###### 

        distribution_box = DistributionBox(
            spacing=10,
            padding=[0, 15]
        )

        wrapper_dist_lst_box_u = MainListBoxSet()
        wrapper_dist_lst_box_a = SubListBoxSet()
        wrapper_dist_lst_box_b = SubListBoxSet()

        scroll_view4lst_box_u = ScrollView(do_scroll_y=True)
        scroll_view4lst_box_a = ScrollView(do_scroll_y=True)
        scroll_view4lst_box_b = ScrollView(do_scroll_y=True)

        dist_lst_box_u = ItemsBox()
        dist_lst_box_a = ItemsBox()
        dist_lst_box_b = ItemsBox()

        scroll_view4lst_box_u.add_widget(dist_lst_box_u)
        scroll_view4lst_box_a.add_widget(dist_lst_box_a)
        scroll_view4lst_box_b.add_widget(dist_lst_box_b)

        wrapper_dist_lst_box_u.add_widget(scroll_view4lst_box_u)
        wrapper_dist_lst_box_a.add_widget(scroll_view4lst_box_a)
        wrapper_dist_lst_box_b.add_widget(scroll_view4lst_box_b)

        distribution_box.add_widget(wrapper_dist_lst_box_a)
        distribution_box.add_widget(wrapper_dist_lst_box_u)
        distribution_box.add_widget(wrapper_dist_lst_box_b)

        item_group = ItemsGroup(
            {
                'center': {
                    'wrapper': wrapper_dist_lst_box_u,
                    'box': dist_lst_box_u
                },
                'left': {
                    'wrapper': wrapper_dist_lst_box_a,
                    'box': dist_lst_box_a
                },
                'right': {
                    'wrapper': wrapper_dist_lst_box_b,
                    'box': dist_lst_box_b
                }
            }
        )

        [u, a, b] = item_group.get_sets()


        slider_submit_button.bind(on_press= lambda x:item_group.new_universum(list(range(int_slider.value + 1))))

        ###### Report Filling ######

        report_scroll = ScrollView()
        report_box = ReportGrid()

        report_scroll.add_widget(report_box)

        btn_submit_report = SubmitButton(text='Get Report')

        def make_item(title, val):
            _item = ReportGridItem()
            _item.add_widget(Label(text=str(title), size_hint_x=.5))
            _item.add_widget(Label(text=str(val)))
            return _item

        def filling_report():
            if not u or not a or not b:
                return

            report_box.clear_widgets()

            report_box.add_widget(make_item('U: ', u))
            report_box.add_widget(make_item('A: ', a))
            report_box.add_widget(make_item('B: ', b))

            report_box.add_widget(make_item('|U|: ', len(u)))
            report_box.add_widget(make_item('|A|: ', len(a)))
            report_box.add_widget(make_item('|B|: ', len(b)))

            report_box.add_widget(make_item('A ~ B: ', len(b) == len(a)))
            report_box.add_widget(make_item('A == B: ', a == b))
            report_box.add_widget(make_item('A <= B: ', a.issubset(b)))
            report_box.add_widget(make_item('B <= A: ', b.issubset(a)))

            report_box.add_widget(make_item('A U B: ', a.union(b)))
            report_box.add_widget(make_item('A П B: ', a.intersection(b)))
            report_box.add_widget(make_item('!A: ', u.difference(a)))
            report_box.add_widget(make_item('!B: ', u.difference(b)))
            report_box.add_widget(make_item('A \ B: ', a.difference(b)))
            report_box.add_widget(make_item('B \ A: ', b.difference(a)))
            report_box.add_widget(make_item('A - B: ', a.symmetric_difference(b)))



        btn_submit_report.bind(on_press=lambda a: filling_report())



        ###### Adding widgets 4 all important layoutes ######

        report_layout.add_widget(btn_submit_report)
        report_layout.add_widget(report_scroll)
        report_layout.add_widget(btn_to_set_layout)
        report_layout.add_widget(btn_to_info_layout)

        set_layout.add_widget(slider_box)
        set_layout.add_widget(distribution_box)
        set_layout.add_widget(btn_to_report_layout)

        info_layout.add_widget(Label(text='Gamirkin Ilya\n2282\nGit: https://github.com/IRaccoonI/DM_No1'))
        info_layout.add_widget(btn2_to_report_layout)

        root.add_widget(report_layout)
        # root.add_widget(set_layout)

        return root
 
if __name__ == '__main__':
    app = MainApp()
    app.run()