import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm

def visualize_GD(history, objective):
    """
    Creates interactive Plot of gradient descent for a function of one variable.

    Parameters:
    history (numpy.ndarray): Array of points visited during optimization.
    function (lambda function): Objective function to minimize.

    Returns:
    IPython.display.Animation: Animation of optimization process.
    """
    fig, ax = plt.subplots()
    x_vals = np.linspace(-10,5,81)
    y_vals = objective(x_vals)

    ax.plot(x_vals, y_vals, label='Gradient Descent for function of 1 variable')

    # Initialize an empty scatter plot
    point, = ax.plot([], [], 'ro', label='Step 0')

    text = ax.text(0.5, 0.5, '')
    
    # Add labels and title to the plot
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Gradient Descent')

    # Add legend
    ax.legend()

    # Set the limits of the x and y axes
    ax.set_xlim(-10, 5)
    ax.set_ylim(-50, 50)


    # Function to update the scatter plot
    arrows = []

    # Function to update the scatter plot
    def update(i):
        nonlocal arrows
        if(i % len(history) == 0):
            for arrow in arrows:
                arrow.remove()
            arrows = []
#         print(len(ax.patches))
#         ax.patches.pop(0)
        point.set_data(history[i], objective(history[i]))
        point.set_label('Step {}'.format(i+1))
        text.set_text(f'({history[i].round(3)}, {objective(history[i]).round(3)})')
        text.set_position((history[i], objective(history[i])))
#         ax.text(, , fontsize=10, color='black')
        ax.legend()
        if(i>0):
            arrow = ax.annotate('', xy=(history[i], objective(history[i])), xytext=(history[i-1], objective(history[i-1])),
                   arrowprops={'arrowstyle': '->', 'color': 'r', 'lw': 1}, va='center', ha='center')
            arrows.append(arrow)
        return point, text
        

    # Create the animation
    animation = FuncAnimation(fig, update, frames=len(history), interval=1000, blit=True)

#     # Show the plot
    plt.show()
    return animation




# visualization function
def visualize_GD_3D(history, objective):
    '''
    Creates an interactive 3D plot of gradient descent for a function of two variables.

    Parameters:
    history (numpy.ndarray): Array of points visited during optimization.

    Returns:
    IPython.display.Animation: Animation of optimization process.
    '''
    fig = plt.figure(figsize=(8, 8))  # Adjust the figsize as needed
    ax = fig.add_subplot(111, projection='3d', computed_zorder=False)

    x_vals = np.linspace(-5, 5, 100)
    y_vals = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = objective([X, Y])
    
    # Adjust the number of contour levels for more color variation
    contours = 50
    

    # Create a logarithmic color scale
    norm = LogNorm()
    shift_value = -np.min(Z)

    # Apply the shift to the Z values
    Z_sh = Z + shift_value

    
    surf = ax.plot_surface(X, Y, Z_sh ,cmap=plt.cm.jet, edgecolor='gray', linewidth=0.15, antialiased=False, alpha=.7,zorder = 1,\
                               rcount=contours, ccount=contours, norm=norm, label='Gradient Descent for function of 2 variable')
    surf._edgecolors2d = surf._edgecolor3d
    surf._facecolors2d = surf._facecolor3d
    point, = ax.plot([], [], [], 'mo', label='Step 0', zorder = 4)
    text = ax.text(0.5, 0.5, 0.5, '')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x, y)')
#     ax.set_zlabel(f'f(x, y) + {shift_value:.2f}')  # Adjust the Z label to show the shift
    ax.set_title('Gradient Descent')
    ax.legend()

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(np.min(Z) - shift_value - 2, np.max(Z) + shift_value)
    
    
    # Calculate tick values and labels for the z-axis
    tick_values = ax.get_zticks()
    tick_labels = [f'{value - shift_value:.2f}' for value in tick_values]
    
    # Set the new tick labels for the z-axis
    ax.set_zticks(tick_values)
    ax.set_zticklabels(tick_labels)

    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    arrows = []
    # Function to update the scatter plot
    def update(i):
        nonlocal arrows
        if(i % len(history) == 0):
            for arrow in arrows:
                arrow.remove()
            arrows = []
        x_data = history[i][0]
        y_data = history[i][1]
        z_data = objective([x_data, y_data])

#         point.set_data(x_data, y_data)
#         point.set_3d_properties(z_data)
        point.set_data_3d(x_data, y_data, z_data)
        point.set_zorder(10)
        point.set_label('Step {}'.format(i+1))
        text.set_text(f'({x_data.round(2)}, {y_data.round(2)}, {z_data.round(2)})')
        text.set_position((x_data, y_data, z_data))
        surf._edgecolors2d = surf._edgecolor3d
        surf._facecolors2d = surf._facecolor3d
        ax.legend()
        if(i>0):
            arrow = ax.quiver(x_data, y_data, z_data, x_data-history[i-1][0], y_data-history[i-1][1], z_data-objective([history[i-1][0],history[i-1][1]]) , pivot = 'tip', normalize = True, color='purple', zorder = 20)
            arrows.append(arrow)
        
        return point,text

    
    # Create the animation
    animation = FuncAnimation(fig, update, frames=len(history), interval=1000, blit= True)

#     # Show the plot
    plt.show()
    return animation

