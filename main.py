import qutip as qt
import numpy as np
from manim import *
from Evolution_Calculation import AQCSystem, simple_time_schedule, optimal_time_schedule, match_by_padding, generate_dimless_timelis


class RotatingState(Scene):
    def construct(self):
        #Plug in the numbers for a0
        n = 100
        tf0 = 200
        tf1 = 100
        dimless_time_lis0,dimless_time_lis1 = generate_dimless_timelis([tf0,tf1],1000)
        init_state = qt.Qobj([[np.sqrt(1 / n)], [np.sqrt((n - 1) / n)]])
        hmlta = qt.Qobj([[1-1/n, -np.sqrt(n-1)/n], [-np.sqrt(n-1)/n, 1-(n-1)/n]])
        hmltb = qt.Qobj([[0,0], [0,1]])

        simpleGrover = AQCSystem(init_state,[hmlta,hmltb],simple_time_schedule,dimless_time_lis0,tf0)
        optimalGrover = AQCSystem(init_state,[hmlta,hmltb],lambda x,tf,i,*args: optimal_time_schedule(x,tf,i,n,*args),dimless_time_lis1,tf1)




        x0, y0 = simpleGrover.slice_coordinate()
        x1, y1 = optimalGrover.slice_coordinate()
        ground_state0 = simpleGrover.ground_state
        ground_state1 = optimalGrover.ground_state
        proj0 = np.array([np.transpose(ground_state0[i].conjugate())@simpleGrover.state_lis[i] for i in range(len(ground_state0))])
        proj1 = np.array([np.transpose(ground_state1[i].conjugate())@optimalGrover.state_lis[i] for i in range(len(ground_state1))])
        dist0 = simpleGrover.state_lis-proj0*ground_state0
        dist1 = optimalGrover.state_lis-proj1*ground_state1
        self.err0 = np.array([np.matmul(np.transpose(simpleGrover.state_lis[i].conjugate()),dist0[i])[0][0] for i in range(len(dist0))])
        self.err1 = np.array([np.matmul(np.transpose(optimalGrover.state_lis[i].conjugate()),dist1[i])[0][0] for i in range(len(dist1))])
        x0, y0, x1, y1, self.err0, self.err1 = match_by_padding(x0,y0,x1,y1, self.err0, self.err1)
        # Generate the animation
        self.now_at = 0
        self.gap0=simpleGrover.energy_gap
        self.gap1=optimalGrover.energy_gap
        error0=DecimalNumber(self.err0[0]).scale(0.7)
        error1=DecimalNumber(self.err1[1]).scale(0.7)
        error0.set_x(-2.5)
        error0.set_y(-2)
        error1.set_x(2.5)
        error1.set_y(-2)
        self.add(error0)
        self.add(error1)
        def updateError0(mob):
            mob.set_value(self.err0[self.now_at])

        def updateError1(mob):
            mob.set_value(self.err1[self.now_at])

        error0.add_updater(updateError0)
        error1.add_updater(updateError1)

        self.len0=len(dimless_time_lis0)
        self.len1=len(dimless_time_lis1)

        dn0 = DecimalNumber(0).scale(1)
        dn0.set_x(-5)
        dn0.set_y(2)
        self.add(dn0)
        self.clock0 = 0
        dn1 = DecimalNumber(0).scale(1)
        dn1.set_x(5)
        dn1.set_y(2)
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

        # Create axes
        axes0 = Axes(
            x_range=[0, 1, 1],  # The range of the x-axis, with step size
            y_range=[0, 1, 1],  # The range of the y-axis, with step size
            axis_config={"color": BLUE},  # Customization for the appearance of the axes
            x_length = 3,  # Length of the x-axis
            y_length = 3,
            tips=True  # No arrow tips
        )
        axes0.move_to([-2,1.5,0])
        self.add(axes0)

        axes1 = Axes(
            x_range=[0, 1, 1],  # The range of the x-axis, with step size
            y_range=[0, 1, 1],  # The range of the y-axis, with step size
            axis_config={"color": BLUE},  # Customization for the appearance of the axes
            x_length = 3,  # Length of the x-axis
            y_length = 3,
            tips=True  # No arrow tips
        )

        axes1.move_to([2,1.5,0])
        self.add(axes1)

        self.err0abs=np.abs(self.err0)
        self.err1abs=np.abs(self.err1)

        axes0plot=Axes(x_range=[0, 1, 1],y_range=[0, 1.7, 1],x_length=2, y_length=2, tips=False,axis_config={"color": BLUE})
        axes0plot.move_to([-5, -0.5, 0])
        self.add(axes0plot)
        graph0 = axes0plot.plot(lambda x: x, x_range=[])
        axes1plot=Axes(x_range=[0, 1, 1],y_range=[0, 1.7, 1],x_length=2, y_length=2, tips=False,axis_config={"color": BLUE})
        axes1plot.move_to([5.5, -0.5, 0])
        self.add(axes1plot)
        graph1 = axes1plot.plot(lambda x: x, x_range=[])
        self.add(graph0)
        self.add(graph1)

        def update_plot0(mob):
            if self.now_at+1<=self.len0:
                t_lis=dimless_time_lis0[0:self.now_at+1]
                mob.become(axes0plot.plot(lambda x:5*np.interp(x,t_lis,self.err0abs[0:self.now_at+1]),x_range=(t_lis[0],t_lis[-1]+0.01,0.001)))
        graph0.add_updater(update_plot0)
        def update_plot1(mob):
            if self.now_at+1<=self.len1:
                t_lis=dimless_time_lis1[0:self.now_at+1]
                mob.become(axes1plot.plot(lambda x:5*np.interp(x,t_lis,self.err1abs[0:self.now_at+1]),x_range=(t_lis[0],t_lis[-1]+0.01,0.001)))
        graph1.add_updater(update_plot1)



        graph0gap = axes0plot.plot(lambda x: x, x_range=[])
        graph1gap = axes1plot.plot(lambda x: x, x_range=[])
        self.add(graph0gap)
        self.add(graph1gap)

        def update_plot0gap(mob):
            if self.now_at+1<=self.len0:
                t_lis=dimless_time_lis0[0:self.now_at+1]
                mob.become(axes0plot.plot(lambda x:np.interp(x,t_lis,self.gap0[0:self.now_at+1]),x_range=(t_lis[0],t_lis[-1]+0.01)))

        def update_plot1gap(mob):
            if self.now_at+1<=self.len1:
                t_lis=dimless_time_lis1[0:self.now_at+1]
                mob.become(axes1plot.plot(lambda x:np.interp(x,t_lis,self.gap1[0:self.now_at+1]),x_range=(t_lis[0],t_lis[-1]+0.01)))

        graph0gap.add_updater(update_plot0gap)
        graph1gap.add_updater(update_plot1gap)

        y_label0 = axes0.get_y_axis_label(
            Tex(r"$||\langle m^\perp|\phi\rangle||$").scale(0.5).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.12,
        )
        x_label0 = axes0.get_x_axis_label(
            Tex(r"$||\langle m|\phi\rangle||$").scale(0.5),
            edge=DOWN,
            direction=DOWN,
            buff=0.12,
        )
        y_label1 = axes1.get_y_axis_label(
            Tex(r"$||\langle m^\perp|\phi\rangle||$").scale(0.5).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.12,
        )
        x_label1 = axes1.get_x_axis_label(
            Tex(r"$||\langle m|\phi\rangle||$").scale(0.5),
            edge=DOWN,
            direction=DOWN,
            buff=0.12,
        )
        y_label0l = axes0plot.get_y_axis_label(
            Tex(r"'Error' \& Energy Gap $\Delta$").scale(0.5).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.15,
        )
        x_label0l =axes0plot.get_x_axis_label(
            Tex("Dimensionless Time $s$").scale(0.5),
            edge=DOWN,
            direction=DOWN,
            buff=0.15,
        )
        y_label1R = axes1plot.get_y_axis_label(
            Tex(r"'Error' \& Energy Gap $\Delta$").scale(0.5).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.15,
        )
        x_label1R = axes1plot.get_x_axis_label(
            Tex("Dimensionless Time $s$").scale(0.5),
            edge=DOWN,
            direction=DOWN,
            buff=0.15,
        )
        self.add(y_label0)
        self.add(x_label0)
        self.add(y_label1)
        self.add(x_label1)
        self.add(y_label0l)
        self.add(x_label0l)
        self.add(y_label1R)
        self.add(x_label1R)

        textt0=Tex(r"Real$^*$ Time/s").scale(0.7)
        textt0.move_to([-5,3,0])
        self.add(textt0)

        textt1 = Tex(r"Real$^*$ Time/s").scale(0.7)
        textt1.move_to([5, 3, 0])
        self.add(textt1)

        text=Tex(r"Transition Amp $\langle \Phi|P-I|\Phi \rangle$").scale(0.7)
        text.move_to([0,-1.5,0])
        self.add(text)

        a0 = Arrow(axes0.c2p(0, 0), axes0.c2p(0, 0) + [3 * np.sqrt(1 / n), 3 * np.sqrt((n - 1) / n), 0],color=GOLD, buff=0)
        a1 = Arrow(axes1.c2p(0, 0), axes1.c2p(0, 0) + [3 * np.sqrt(1 / n), 3 * np.sqrt((n - 1) / n), 0],color=GOLD, buff=0)

        for i in range(1, len(x1)):
            self.play(
                Rotate(
                    a0,
                    angle=np.arctan(np.abs(y0[i][0]/x0[i][0]))-np.arctan(np.abs(y0[i-1][0]/x0[i-1][0])),
                    about_point=axes0.c2p(0,0),
                    rate_func=linear
            ),
            Rotate(
                a1,
                angle=np.arctan(np.abs(y1[i][0] / x1[i][0])) - np.arctan(np.abs(y1[i - 1][0] / x1[i - 1][0])),
                about_point=axes1.c2p(0,0),
                rate_func=linear
            ),
            run_time = 0.033)
            self.now_at+=1

if __name__=="__main__":
    a=RotatingState()
    a.construct()