import qutip as qt
import numpy as np
from manim import *
from Evolution_Calculation import close_evolve, AQCSystem, simple_time_schedule, optimal_time_schedule


class RotatingState(Scene):
    def construct(self):
        #Plug in the numbers for a0
        n = 3
        tf1 = 7000
        dimless_time_lis1 = np.linspace(0, 1, 300)
        init_state = qt.Qobj([[np.sqrt(1 / n)], [np.sqrt((n - 1) / n)]])
        hmlta = qt.Qobj([[1-1/n, -np.sqrt(n-1)/n], [-np.sqrt(n-1)/n, 1-(n-1)/n]])
        hmltb = qt.Qobj([[0,0], [0,1]])

        simpleGrover = AQCSystem(init_state,[hmlta,hmltb],simple_time_schedule,dimless_time_lis1,tf1)
        print(abs(simpleGrover.state_lis)[-1])

        '''
        #Generate the animation
        a0=Arrow([0,0,0],[3*np.sqrt(1/n),3*np.sqrt((n - 1)/n),0])
        x, y = simpleGrover.slice_coordinate()
        for i in range(1, len(dimless_time_lis1)):
            self.play(
                Rotate(
                    a0,
                    angle=np.arctan(np.abs(y[i][0]/x[i][0]))-np.arctan(np.abs(y[i-1][0]/x[i-1][0])),
                    about_point=[0,0,0],
                    rate_func=linear
            ))
        '''

a=RotatingState()
a.construct()