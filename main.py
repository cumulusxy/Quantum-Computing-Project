import qutip as qt
import numpy as np
from manim import *
from Evolution_Calculation import close_evolve, AQCSystem, simple_time_schedule, optimal_time_schedule, match_by_padding, generate_dimless_timelis, get_ground_state


class RotatingState(Scene):
    def construct(self):
        #Plug in the numbers for a0
        n = 30
        tf0 = 100
        tf1 = 80
        dimless_time_lis0,dimless_time_lis1 = generate_dimless_timelis([tf0,tf1],50)
        init_state = qt.Qobj([[np.sqrt(1 / n)], [np.sqrt((n - 1) / n)]])
        hmlta = qt.Qobj([[1-1/n, -np.sqrt(n-1)/n], [-np.sqrt(n-1)/n, 1-(n-1)/n]])
        hmltb = qt.Qobj([[0,0], [0,1]])

        simpleGrover = AQCSystem(init_state,[hmlta,hmltb],simple_time_schedule,dimless_time_lis0,tf0)
        optimalGrover = AQCSystem(init_state,[hmlta,hmltb],lambda x,tf,i,*args: optimal_time_schedule(x,tf,i,n,*args),dimless_time_lis1,tf1)



        a0=Arrow([-3,0,0],[-3+3*np.sqrt(1/n),3*np.sqrt((n - 1)/n),0])
        a1=Arrow([3,0,0],[3+3*np.sqrt(1/n),3*np.sqrt((n - 1)/n),0])
        x0, y0 = simpleGrover.slice_coordinate()
        x1, y1 = optimalGrover.slice_coordinate()
        ground_state0 = simpleGrover.ground_state
        ground_state1 = optimalGrover.ground_state
        proj0 = np.array([np.transpose(ground_state0[i].conjugate())@simpleGrover.state_lis[i] for i in range(len(ground_state0))])
        proj1 = np.array([np.transpose(ground_state1[i].conjugate())@optimalGrover.state_lis[i] for i in range(len(ground_state1))])
        dist0 = simpleGrover.state_lis-proj0*ground_state0
        dist1 = optimalGrover.state_lis-proj1*ground_state1
        self.err0 = np.array([np.matmul(np.transpose(simpleGrover.state_lis[i].conjugate()),dist0) for i in range(len(dist0))])[0]
        self.err1 = np.array([np.matmul(np.transpose(optimalGrover.state_lis[i].conjugate()),dist1) for i in range(len(dist1))])[0]
        x0, y0, x1, y1, self.err0, self.err1 = match_by_padding(x0,y0,x1,y1, self.err0, self.err1)
        # Generate the animation
        self.now_at = 0
        error0=DecimalNumber(self.err0[0][0][0])
        error1=DecimalNumber(self.err1[1][0][0])
        error0.set_x(-3)
        error0.set_y(-3)
        error1.set_x(3)
        error1.set_y(-3)
        self.add(error0)
        self.add(error1)
        def updateError0(mob):
            mob.set_value(self.err0[self.now_at][0][0])

        def updateError1(mob):
            mob.set_value(self.err1[self.now_at][0][0])

        error0.add_updater(updateError0)
        error1.add_updater(updateError1)

        self.len0=len(dimless_time_lis0)
        self.len1=len(dimless_time_lis1)

        dn0 = DecimalNumber(0)
        dn0.set_x(-3)
        dn0.set_y(-2)
        self.add(dn0)
        self.clock0 = 0
        dn1 = DecimalNumber(0)
        dn1.set_x(3)
        dn1.set_y(-2)
        self.add(dn1)
        self.clock1 = 0
        def update_timer0(mob, dt):
            if self.now_at<=self.len0:
                self.clock0 += dt
                mob.set_value(self.clock0)


        def update_timer1(mob, dt):
            if self.now_at<=self.len1:
                self.clock1 += dt
                mob.set_value(self.clock1)


        dn0.add_updater(update_timer0)
        dn1.add_updater(update_timer1)

        for i in range(1, len(x1)):
            self.play(
                Rotate(
                    a0,
                    angle=np.arctan(np.abs(y0[i][0]/x0[i][0]))-np.arctan(np.abs(y0[i-1][0]/x0[i-1][0])),
                    about_point=[-3,0,0],
                    rate_funpic=linear
            ),
            Rotate(
                a1,
                angle=np.arctan(np.abs(y1[i][0] / x1[i][0])) - np.arctan(np.abs(y1[i - 1][0] / x1[i - 1][0])),
                about_point=[3, 0, 0],
                rate_func=linear
            )
            )
            self.now_at+=1

if __name__=="__main__":
    a=RotatingState()
    a.construct()