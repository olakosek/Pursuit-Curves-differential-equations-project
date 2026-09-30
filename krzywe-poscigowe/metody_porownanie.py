#%matplotlib widget
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.animation import FuncAnimation
plt.close('all')
#constans

TIME_SPAN = (0, 25)
T_EVAL = np.linspace(TIME_SPAN[0],TIME_SPAN[1], 2000)
starting_pos = [20,0]
starting_pos_target = [0.0,0.0]
def target(t):
    return np.array([starting_pos_target[0],starting_pos_target[1]+t])#ruch jednostajny

def dynamics(t, pos):
    curr_pos = np.array([pos[0], pos[1]])
    curr_target = target(t)
    distance_to_target=np.linalg.norm(curr_target - curr_pos)
    if distance_to_target < 1e-5: return np.array([0.0, 0.0])#target caught
    unit_vector = (curr_target - curr_pos) / distance_to_target #dx/dt=V*(x_lion-x_target)/(distance); same with y:this is our differential equation
    return 1.3*unit_vector
#euler method
def euler_method(dynamics,time_span, y0,dt):#y0 is our initial condition
    time_values=[time_span[0]]
    y_values=[np.array(y0)]#list to save our steps
    t=time_span[0]
    y=np.array(y0)
    while t<time_span[1]:
        dydt=np.array(dynamics(t, y))#our derivative is equal to what we calculated in lion dynamics
        y=y+dt*dydt#step
        t+=dt
        y_values.append(y.copy())
        time_values.append(t)
    return np.array(time_values), np.array(y_values).T

#rungego-kutty method
def runge_kutty_method(dynamics,time_span,y0,h):
    time_values=[time_span[0]]
    y_values=[np.array(y0)]
    t=time_span[0]
    y=np.array(y0)
    while t<time_span[1]:
        a=np.array(dynamics(t, y))
        b=np.array(dynamics(t+(h/2), y+(h/2)*a))
        c=np.array(dynamics(t+(h/2), y+(h/2)*b))
        d=np.array(dynamics(t+(h/2), y+(h/2)*c))
        y=y+ (h/6)*(a+2*b+2*c+d)
        t+=h
        y_values.append(y.copy())
        time_values.append(t)
    return np.array(time_values), np.array(y_values).T

#movement
DT=0.5
time_E, y_E = euler_method(dynamics,TIME_SPAN, starting_pos, DT)#we get steps in time and coordiates
time_R, y_R = runge_kutty_method(dynamics,TIME_SPAN, starting_pos, DT)
#time_A, y_A = analitical(TIME_SPAN)
fig, ax = plt.subplots(figsize=(6.5, 6.5))
fig.suptitle("Comparison")
ax.set_xlim(-2, 20)
ax.set_ylim(-2, 20)
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.plot(y_E[0], y_E[1], 'r--', label=f'Euler ', alpha=0.8)#euler
ax.plot(y_R[0], y_R[1], 'b-', label=f'Runge-Kutta ', alpha=0.8)#runge-kutty
#ax.plot(time_A, y_A, 'y-', label=f'Analitical ', alpha=0.8)#analitical
ax.legend(loc='upper right')
plt.show()

