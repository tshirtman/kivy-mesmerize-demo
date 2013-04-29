from kivy.app import App
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from itertools import izip, chain
from random import randint


kv = '''
#:import sin math.sin
#:import cos math.cos
#:import izip itertools.izip
#:import chain itertools.chain

MyWidget:
    points:
        [
        (
        self.x + (x + 1) * self.width / (self.nb_points + 2),
        self.center_y + self.height * sin(x * self.mult * 1.0 / self.nb_points + self.offset) / 2
        )
        for x in range(self.nb_points)
        ]

    canvas:
        Color:
            rgba: self.color
        #Line:
            #points: self.points and list(chain(*self.points)) or []
            #width: 5
        #Line:
            #points: self.points and list(chain(* ((x, self.top - y) for (x, y) in self.points))) or []
            #width: 5

        Line:
            points:
                list(chain(* ((root.width / 4 + cos(x) * y / 2, root.height / 2 + sin(x) * y / 2) for (x, y) in self.points)))\
                if self.points else []
            width: 5
        Line:
            points:
                list(chain(* ((3 * root.width / 4 - cos(x) * y / 2, root.height / 2 - sin(x) * y / 2) for (x, y) in reversed(self.points))))\
                if self.points else []
            width: 5
            #close: True
'''


class MyWidget(Widget):
    nb_points = NumericProperty(150)
    offset = NumericProperty(0)
    mult = NumericProperty(50)
    color = ListProperty([1, 0, 1, 1])


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
        #Clock.schedule_interval(self.change_nb_points, 1)
        return self.root

    def change_nb_points(self, *args):
        print "called"
        self.nb_points = randint(1, 200)
        print self.nb_points
        return True


MyApp().run()
