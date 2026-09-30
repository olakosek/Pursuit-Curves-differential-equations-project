import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import ipywidgets as widgets
from IPython.display import display

plt.ioff()
fig, ax = plt.subplots(figsize=(7, 7))
plt.ion()

#slider_v_rocket = widgets.FloatSlider(value=2.4, min=0.5, max=5.0, step=0.1, description='Velocity Rocket:')
#slider_v_plane = widgets.FloatSlider(value=1.3, min=0.5, max=5.0, step=0.1, description='Velocity Plane:')
#btn_run = widgets.Button(description='Run Simulation', button_style='success', icon='play')
#ui = widgets.VBox([widgets.HBox([slider_v_rocket, slider_v_plane]), btn_run])

ani = None
#constans
def chase_simulation(b):
    global ani
    if ani is not None:
        try:
            ani.event_source.stop()
        except:
            pass
        del ani
        ani = None
    ax.clear() 
    
    V_ROCKET = 2#slider_v_rocket.value
    V_PLANE = 3#slider_v_plane.value
    FRAMES = 300
    DT=0.1
    #set starting positions
    pos_city=np.array([12,12])
    pos_plane=np.array([12.0, 0.0])
    pos_rocket=np.array([2.0, 10.0])
    #history of movement
    history_plane = [pos_plane.copy()]
    history_rocket = [pos_rocket.copy()]
    curr_plane = pos_plane.copy()
    curr_rocket = pos_rocket.copy()
    plane_arrived = False
    rocket_hit_plane = False
    #movement
    for _ in range(FRAMES):
        if not plane_arrived and not rocket_hit_plane:
            vector_to_hole = pos_city - curr_plane
            distance_to_hole = np.linalg.norm(vector_to_hole)
            if distance_to_hole < 0.1:
                # plane arrived
                vel_plane = np.array([0.0, 0.0])
                plane_arrived = True
            else:
                direction = np.sign(pos_city[0] - curr_plane[0])#rabbit moves only on x axis
                vel_plane = np.array([direction * V_PLANE, 0.0])
        if not plane_arrived and not rocket_hit_plane:
            vector_plane_rocket = curr_plane - curr_rocket
            distance_plane_rocket = np.linalg.norm(vector_plane_rocket)
            if distance_plane_rocket < 0.2:
                vel_rocket = np.array([0.0, 0.0])
                vel_plane = np.array([0.0,0.0])
                rocket_hit_plane = True
            else:
                direction = vector_plane_rocket / distance_plane_rocket
                vel_rocket = direction * V_ROCKET
        if not plane_arrived and not rocket_hit_plane:
            curr_plane += vel_plane*DT
            curr_rocket  += vel_rocket*DT
            history_plane.append(curr_plane.copy())
            history_rocket.append(curr_rocket.copy())
    history_plane = np.array(history_plane)
    history_rocket = np.array(history_rocket)
    #chart
    ax.set_title("Simulation of a chase between a dog and a rabbit")
    ax.set_xlim(-2, 14)
    ax.set_ylim(-2, 14)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    ax.plot(0, 0, 'ko', markersize=15, markerfacecolor='black', label='Rabbit Hole')
    line_connector, = ax.plot([], [], 'k--', linewidth=1, alpha=0.4, label='Line of sight')
    rocket_trace, = ax.plot([], [], 'b-', linewidth=1.5, alpha=0.2, label='Rocket Trace')
    plane_dot, = ax.plot([], [], 'ro', markersize=8, label='Plane', zorder=3)
    rocket_dot, = ax.plot([], [], 'bo', markersize=10, label='Rocket', zorder=3)
    ax.legend(loc='upper right')
    #animation
    def animate(i):
        idx = min(i, len(history_plane) - 1)
        plane_dot.set_data([history_plane[idx, 0]], [history_plane[idx, 1]])
        rocket_dot.set_data([history_rocket[idx, 0]], [history_rocket[idx, 1]])
        line_connector.set_data([history_rocket[idx, 0], history_plane[idx, 0]], [history_rocket[idx, 1], history_plane[idx, 1]])
        rocket_trace.set_data(history_rocket[:idx+1, 0], history_rocket[:idx+1, 1])
        return plane_dot, rocket_dot, line_connector, rocket_trace
    
    ani = FuncAnimation(fig, animate, frames=len(history_plane), interval=30, blit=True, repeat=False)
    #fig.canvas.draw_idle()
    plt.show()
#btn_run.on_click(chase_simulation)

##display(ui)
#display(fig.canvas)