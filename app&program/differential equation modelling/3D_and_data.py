
import numpy as np
import matplotlib.pyplot as plt

# equation or function to plot, e.g., z = sin(sqrt(x^2 + y^2))
def func(x, y):
    return np.sin(np.sqrt(x**2 + y**2))

# create grid of x and y with ranges
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x_vals, y_vals)
z = func(x, y)

# set up the figure and 4 subplots
fig = plt.figure(figsize=(14, 10))

# subplot_1: Isometric view
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.plot_surface(x, y, z, cmap='viridis', edgecolor='none')
ax1.set_title('3D Isometric View')
ax1.view_init(30, 45)  # viewing angle

# subplot_2: Top view
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
ax2.plot_surface(x, y, z, cmap='plasma', edgecolor='none')
ax2.set_title('Top View')
ax2.view_init(90, 0)  # viewing the top

# subplot_3: Side view
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
ax3.plot_surface(x, y, z, cmap='inferno', edgecolor='none')
ax3.set_title('Side View')
ax3.view_init(0, 0)  # viewing  the side

# subplot_4: Front view
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
ax4.plot_surface(x, y, z, cmap='coolwarm', edgecolor='none')
ax4.set_title('Front View')
ax4.view_init(0, 90)  # viewing the front

plt.tight_layout()
plt.show()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def func(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x_vals, y_vals)
z = func(x, y)

fig = plt.figure(figsize=(14, 10))

ax = fig.add_subplot(111, projection='3d')
surface = ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none')
fig.colorbar(surface, ax=ax, shrink=0.5, aspect=5)
ax.set_title('Interactive 3D Plot with Clickable Points')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
def on_click(event):
    if event.inaxes == ax:
        x_click, y_click = event.xdata, event.ydata
        x_idx = (np.abs(x_vals - x_click)).argmin()
        y_idx = (np.abs(y_vals - y_click)).argmin()
        z_click = z[y_idx, x_idx]
        annotation = f"x = {x_vals[x_idx]:.2f}, y = {y_vals[y_idx]:.2f}, z = {z_click:.2f}"
        ax.texts.clear()
        ax.text2D(0.05, 0.95, annotation, transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
        plt.draw()

fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
