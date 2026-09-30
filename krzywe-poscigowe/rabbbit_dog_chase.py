import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
plt.close('all')
#constans
FRAMES = 300
DT=0.5
V_RABBIT=1
V_DOG=1
#set starting positions
pos_rabbit_hole=np.array([0.0,0.0])
pos_rabbit=np.array([12.0, 0.0])
pos_dog=np.array([2.0, 10.0])
#history of movement
history_rabbit = [pos_rabbit.copy()]
history_dog = [pos_dog.copy()]
curr_rabbit = pos_rabbit.copy()
curr_dog = pos_dog.copy()
rabbit_in_hole = False
dog_ate_rabbit = False
#movement
for _ in range(FRAMES):
    if not rabbit_in_hole and not dog_ate_rabbit:
        vector_to_hole = pos_rabbit_hole - curr_rabbit
        distance_to_hole = np.linalg.norm(vector_to_hole)
        if distance_to_hole < 0.1:
            # rabbit home:)
            vel_rabbit = np.array([0.0, 0.0])
            rabbit_in_hole = True
        else:
            direction = np.sign(pos_rabbit_hole[0] - curr_rabbit[0])#rabbit moves only on x axis
            vel_rabbit = np.array([direction * V_RABBIT, 0.0])
    if not rabbit_in_hole and not dog_ate_rabbit:
        vector_dog_rabbit = curr_rabbit - curr_dog
        distance_dog_rabbit = np.linalg.norm(vector_dog_rabbit)
        if distance_dog_rabbit < 0.2:
            vel_dog = np.array([0.0, 0.0])
            vel_rabbit = np.array([0.0,0.0])
            dog_ate_rabbit = True
        else:
            direction = vector_dog_rabbit / distance_dog_rabbit
            vel_dog = direction * V_DOG
    if not rabbit_in_hole and not dog_ate_rabbit:
        curr_rabbit += vel_rabbit*DT
        curr_dog  += vel_dog*DT
        history_rabbit.append(curr_rabbit.copy())
        history_dog.append(curr_dog.copy())
history_rabbit = np.array(history_rabbit)
history_dog = np.array(history_dog)
#chart
fig, ax = plt.subplots(figsize=(8, 8))
fig.suptitle("Simulation of a chase between a dog and a rabbit")
ax.set_xlim(-2, 14)
ax.set_ylim(-2, 14)
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
hole_plot = ax.plot(pos_rabbit_hole[0], pos_rabbit_hole[1], 'ko', markersize=15, 
                    markerfacecolor='black', markeredgecolor='brown', 
                    markeredgewidth=3, label='Rabbit hole (target)', zorder=1)
line_connector, = ax.plot([], [], 'k--', linewidth=1.5, alpha=0.7, label='Line of sight')
rabbit_dot, = ax.plot([], [], 'ro', markersize=10, label='Rabbit', zorder=3)
dog_dot, = ax.plot([], [], 'bo', markersize=10, label='Dog', zorder=3)
dog_trace, = ax.plot([], [], 'b-', linewidth=1.5, alpha=0.2)

ax.legend(loc='upper right')
#animation
def animate(i):
    rx, ry = history_rabbit[i]
    dx, dy = history_dog[i]
    rabbit_dot.set_data([rx], [ry])
    dog_dot.set_data([dx], [dy])
    line_connector.set_data([dx, rx], [dy, ry])
    dog_trace.set_data(history_dog[:i+1, 0], history_dog[:i+1, 1])
    return rabbit_dot, dog_dot, line_connector, dog_trace
ani_rabbit = FuncAnimation(fig, animate, frames=len(history_rabbit), interval=100, blit=True, repeat=False)

plt.show()