import qutip as qt
import numpy as np
from manim import *
from Evolution_Calculation import close_evolve, AQCSystem, simple_time_schedule, optimal_time_schedule, match_by_padding, generate_dimless_timelis


class RotatingState(Scene):
    def construct(self):
        #Plug in the numbers for a0
        n = 10
        tf1 = 100
        tf2 = 65
        dimless_time_lis1,dimless_time_lis2 = generate_dimless_timelis([tf1,tf2],50)
        init_state = qt.Qobj([[np.sqrt(1 / n)], [np.sqrt((n - 1) / n)]])
        hmlta = qt.Qobj([[1-1/n, -np.sqrt(n-1)/n], [-np.sqrt(n-1)/n, 1-(n-1)/n]])
        hmltb = qt.Qobj([[0,0], [0,1]])

        simpleGrover = AQCSystem(init_state,[hmlta,hmltb],simple_time_schedule,dimless_time_lis1,tf1)
        optimalGrover = AQCSystem(init_state,[hmlta,hmltb],lambda x,tf,i,*args: optimal_time_schedule(x,tf,i,n,*args),dimless_time_lis2,tf2)


        #Generate the animation
        a0=Arrow([-3,0,0],[-3+3*np.sqrt(1/n),3*np.sqrt((n - 1)/n),0])
        a1=Arrow([3,0,0],[3+3*np.sqrt(1/n),3*np.sqrt((n - 1)/n),0])
        x0, y0 = simpleGrover.slice_coordinate()
        x1, y1 = optimalGrover.slice_coordinate()

        x0, y0, x1, y1 = match_by_padding(x0,y0,x1,y1)

        for i in range(1, len(x1)):
            self.play(
                Rotate(
                    a0,
                    angle=np.arctan(np.abs(y0[i][0]/x0[i][0]))-np.arctan(np.abs(y0[i-1][0]/x0[i-1][0])),
                    about_point=[-3,0,0],
                    rate_func=linear
            ),
            Rotate(
                a1,
                angle=np.arctan(np.abs(y1[i][0] / x1[i][0])) - np.arctan(np.abs(y1[i - 1][0] / x1[i - 1][0])),
                about_point=[3, 0, 0],
                rate_func=linear
            )
            )

if __name__=="__main__":
    a=RotatingState()
    a.construct()