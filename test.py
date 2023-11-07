import qutip as qt
import numpy as np
tmax=700
time_lis=np.linspace(0,1,300)
n=3
init_state = qt.Qobj([[np.sqrt(1 / n)], [np.sqrt((n - 1) / n)]])
hmlta = qt.Qobj([[1 - 1 / n, -np.sqrt(n - 1) / n], [-np.sqrt(n - 1) / n, 1 - (n - 1) / n]])
hmltb = qt.Qobj([[0,0],[0,1]])
print(time_lis*tmax)
a=qt.mesolve([[hmlta,lambda x,*arg:(tmax-x)/tmax],[hmltb,lambda x,*arg: x/tmax]], init_state, time_lis*tmax, [], [])
print(np.abs(a.states)[-1])