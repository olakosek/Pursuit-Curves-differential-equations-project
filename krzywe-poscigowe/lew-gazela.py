import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
plt.close('all')
#constans
V_GAZELLE=0.9#90km/h, speed gazelle starts with
AMPLITUDE = 3
FREQUENCY = 0.5
K_GAZELLE=0.01#stamina
V_LION=0.8#80km/h, speed lion gazelle starts with
K_LION=0.02#lion gets tired quicker/loses speed faster
TIME_SPAN = (0, 25)
T_EVAL = np.linspace(TIME_SPAN[0],TIME_SPAN[1], 2000)

#set starting positions
pos_gazelle1_start=np.array([9, 0.5])
pos_gazelle2_start=np.array([11, 0.5])
pos_lion_start=np.array([10, 0])

#animal speeds
def get_speeds(t):
    v_l = np.maximum(0, V_LION - K_LION * t)
    v_g = np.maximum(0, V_GAZELLE - K_GAZELLE * t)
    return v_l, v_g

#functions defining gazzeles movements
def gazelle1_pos(t):
    dist = V_GAZELLE * t - 0.5 * K_GAZELLE * t**2 #distance during uniformly decelerated motion
    return np.array([pos_gazelle1_start[0] + AMPLITUDE * np.sin(FREQUENCY * t), pos_gazelle1_start[1] + dist ])

def gazelle2_pos(t):
    dist = V_GAZELLE * t - 0.5 * K_GAZELLE * t**2 #distance during uniformly decelerated motion
    return np.array([pos_gazelle2_start[0] - AMPLITUDE * np.sin(FREQUENCY * t), pos_gazelle2_start[1] + dist])

#lion
def lion_dynamics(t, pos):
    lion_pos = np.array([pos[0], pos[1]])
    v_lion_curr, _ = get_speeds(t) #we get both speeds (lion and gazzele), but we only need lion's
    if v_lion_curr <= 0: return [0, 0]#lion got tired and stopped
    g1 = gazelle1_pos(t)
    g2 = gazelle2_pos(t)
    distance_lion_gazelle1=np.linalg.norm(g1 - lion_pos)#calculation the distance between lion and each gazelle to determin which to pursuit
    distance_lion_gazelle2=np.linalg.norm(g2 - lion_pos)
    target = g1 if distance_lion_gazelle1 < distance_lion_gazelle2 else g2
    dist_to_target = np.linalg.norm(target - lion_pos) #denominator in our differential equation
    if dist_to_target < 0.05: #lion ate gazelle
        return [0, 0]
    unit_vector = (target - lion_pos) / dist_to_target #dx/dt=V*(x_lion-x_target)/(distance); same with y:this is our differential equation
    v_vector = unit_vector * v_lion_curr#current speed
    return [v_vector[0], v_vector[1]]#derevatives with respect to t

def catch_event(t, pos):#lion caught gazelle
    lion_pos = np.array([pos[0], pos[1]])
    dist = min(np.linalg.norm(gazelle1_pos(t) - lion_pos), 
               np.linalg.norm(gazelle2_pos(t) - lion_pos))
    return dist - 0.1
catch_event.terminal = True

def fatigue_event(t, pos):#lion stopped
    v_l, _ = get_speeds(t)
    return v_l - 0.01 
fatigue_event.terminal = True

def euler_method(dynamics,time_span, y0,dt):#y0 is our initial condition
    time_values=[time_span[0]]
    y_values=[np.array(y0)]#list to save our steps
    t=time_span[0]
    y=np.array(y0)
    while t<time_span[1]:
        dydt=np.array(dynamics(t, y))#our derivative is equal to what we calculated in lion dynamics
        y=y+dt*dydt#step
        t=t+dt
        y_values.append(y.copy())
        time_values.append(t)
        v_lion_curr, _ = get_speeds(t)
        if v_lion_curr<0.1:
            print("lion gave up")
            break
        g1_dist = np.linalg.norm(gazelle1_pos(t) - y)
        g2_dist = np.linalg.norm(gazelle2_pos(t) - y)
        if min(g1_dist,g2_dist)<0.1:
            print("lion ate gazelle")
            break
    return np.array(time_values), np.array(y_values).T


#movement
DT=0.01
time, y = euler_method(lion_dynamics,TIME_SPAN, pos_lion_start, DT)#we get steps in time and coordiates
lion_x, lion_y = y#lion coordinates
g1_traj = np.array([gazelle1_pos(t) for t in time])#trajectory of gazelles in calculated times in the euler method
g2_traj = np.array([gazelle2_pos(t) for t in time])

#chart
fig, ax = plt.subplots(figsize=(5, 5))
fig.suptitle("Simulation of a chase between a lion and two gazelles")
fig.patch.set_facecolor('darkolivegreen')
ax.set_facecolor('navajowhite')
ax.set_xlim(-2, 20)
ax.set_ylim(-2, 20)
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
line_l, = ax.plot([], [], 'orange', alpha=0.3)  #lion track
line_g1, = ax.plot([], [], 'saddlebrown', alpha=0.3) #gazelle 1 track
line_g2, = ax.plot([], [], 'brown', alpha=0.3) #gazelle 2 track
dot_l, = ax.plot([], [], 'o', color='orange', label='LION', markersize=8) #current lion position
dot_g1, = ax.plot([], [], 'o', color='saddlebrown', label='GAZELLE 1')#current gazelle 1 position
dot_g2, = ax.plot([], [], 'o', color='brown', label='GAZELLE 2')#current gazelle 2 position
ax.legend(loc='upper right')
status_text = ax.text(0.05, 0.95, '',transform=ax.transAxes,fontsize=12,fontweight='bold',verticalalignment='top',bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
final_time=time[-1]#calculating why the chase stopped; did lion get tired or did gazelles get eaten
final_lion_pos=y[:,-1]
lion_final_speed,_=get_speeds(final_time)
dist1 = np.linalg.norm(gazelle1_pos(final_time) - final_lion_pos)
dist2 = np.linalg.norm(gazelle2_pos(final_time) - final_lion_pos)
if min(dist1, dist2) < 0.15:
    outcome = "LION ATE GAZELLE"
    outcome_color = 'red'
elif lion_final_speed < 0.05:
    outcome = "LION GOT TIRED"
    outcome_color = 'blue'
else:
    outcome = "GAZELLES ESCAPED"
    outcome_color = 'black'

#animation
frame_indices = np.arange(0, len(time), 5)
def animate(frame):
    dot_l.set_data([lion_x[frame]], [lion_y[frame]])
    dot_g1.set_data([g1_traj[frame, 0]], [g1_traj[frame, 1]])
    dot_g2.set_data([g2_traj[frame, 0]], [g2_traj[frame, 1]])
    line_l.set_data(lion_x[:frame], lion_y[:frame])
    line_g1.set_data(g1_traj[:frame,0], g1_traj[:frame,1])
    line_g2.set_data(g2_traj[:frame,0], g2_traj[:frame,1])
    if frame >= len(time)-10:#last frame so we show why the animation stopped
        status_text.set_text(outcome)
        status_text.set_color(outcome_color)
    return dot_l, dot_g1, dot_g2, line_l, line_g1, line_g2, status_text
ani_lion = FuncAnimation(fig, animate, frames=frame_indices, interval=10, blit=True)

plt.show()