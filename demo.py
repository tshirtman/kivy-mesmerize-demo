from kivy.app import App
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from itertools import izip, chain
from random import randint


kv = '''
#:import sin math.sin
#:import cos math.cos
#:import izip itertools.izip
#:import chain itertools.chain
#:import Window kivy.core.window.Window

MyWidget:
    points:
        [(
        x * 1.0 / self.nb_points,
        sin(x * self.mult / self.nb_points + self.offset) / 2
        ) for x in range(self.nb_points) ]

    points2: [ (x * 10 ** 4, y) for (x, y) in self.points ]

    canvas:
        Color:
            rgba: self.color

        Line:
            points:
                list(chain(* ((
                root.pos_1[0] + cos(x) * Window.height * y,
                root.pos_1[1] + sin(x) * Window.height * y
                ) for (x, y) in self.points2)))\
                if self.points else []
            width: 5

        Color:
            rgba: self.color[3:0:-1] + self.color[3:]
        Line:
            points:
                list(chain(* ((
                root.pos_2[0] - cos(x) * Window.height * y,
                root.pos_2[1] - sin(x) * Window.height * y
                ) for (x, y) in reversed(self.points2))))\
                if self.points else []
            width: 5
            #close: True
'''


class MyWidget(Widget):
    nb_points = NumericProperty(100)
    offset = NumericProperty(0)
    mult = NumericProperty(50)
    color = ListProperty([1, 0, 1, 1])
    size_1 = NumericProperty(200)
    size_2 = NumericProperty(200)
    pos_1 = ListProperty([0, 0])
    pos_2 = ListProperty([0, 0])


class MyApp(App):
    def build(self):
        self.root = Builder.load_string(kv)
        program = (
                Animation(mult=50, offset=10, d=10, t='in_out_circ') +
                Animation(mult=10, offset=0, d=10, t='in_out_quad')
                )
        program &= (
                Animation(color=[0, 1, 1, 1], d=6) +
                Animation(color=[1, 1, 0, 1], d=6) +
                Animation(color=[1, 0, 1, 1], d=6)
                )

        program.start(self.root)
        program.bind(on_complete=lambda *args: program.start(self.root))
        Clock.schedule_interval(self.change_nb_points, 20)
        self.update_pos_size()
        return self.root

    def change_nb_points(self, *args):
        self.root.nb_points = randint(5, 150)
        return True

    def update_pos_size(self, *args):
        new_size = randint(0, Window.height / 2)
        print self.root.height, new_size
        new_pos_x = randint(new_size, Window.width - new_size)
        new_pos_y = randint(new_size, Window.height - new_size)

        if randint(0, 1):
            a = Animation(size_1=new_size, pos_1=[new_pos_x, new_pos_y], d=5, t='in_out_quad')
        else:
            a = Animation(size_2=new_size, pos_2=[new_pos_x, new_pos_y], d=5, t='in_out_quad')

        a.bind(on_complete=self.update_pos_size)
        a.start(self.root)

MyApp().run()
