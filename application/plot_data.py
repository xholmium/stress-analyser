import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def setup_plot(title, xlabel, ylabel, x_data, y_data):
    """Common setup for plots (title, labels, and legend)."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # plot setup
    plt.locator_params(axis='x', nbins=16)
    plt.locator_params(axis='y', nbins=20)
    ax = plt.gca()
    ax.grid(which="major")
    ax.grid(which="minor")
    ax.minorticks_on()

    ax.set_title(title, pad=22, fontsize=14, weight='bold')
    ax.set_xlabel(xlabel, loc='right')
    ax.set_ylabel(ylabel, loc='top')

    return fig, ax


def plot_strain_distance(distance, strain, time_on=True):
    """Plot strain vs. distance with a dynamically positioned annotation."""
    if distance is None or strain is None:
        print("Data is empty")
        return

    fig, ax = setup_plot("Závislost deformace na poloze", "vzdálenost [m]", "deformace [microstrain]", distance, strain)
    l, = ax.plot(distance, strain[0], '.-', picker=True)  # Enable picking

    # Create annotation
    annotation = ax.annotate("", xy=(0, 0), xytext=(10, 10),
                             textcoords="offset points", bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5),
                             arrowprops=dict(arrowstyle="->", color='black'))
    annotation.set_visible(False)  # Hide initially

    selected_index = None  # Track the currently selected index
    selected_x, selected_y = None, None  # Store last selected point

    def on_pick(event):
        """Handle mouse clicks on data points."""
        nonlocal selected_index, selected_x, selected_y
        if event.artist == l:
            index = event.ind[0]  # Get first selected point

            # If the same index is clicked again, toggle off
            if selected_index == index:
                annotation.set_visible(False)
                selected_index = None
            else:
                # Update annotation with new point data
                selected_x = distance[index]
                selected_y = strain[selected_time][index]  # Use the selected time step

                annotation.set_text(f"Index: {index}\nDistance: {selected_x:.2f} m\nStrain: {selected_y:.2f}")
                annotation.xy = (selected_x, selected_y)
                annotation.set_visible(True)
                selected_index = index  # Store selected index

            fig.canvas.draw_idle()

    def update_annotation_position(event):
        """Ensure annotation remains aligned when panning/zooming."""
        if annotation.get_visible() and selected_index is not None:
            annotation.xy = (selected_x, selected_y)  # Keep it locked to the selected point
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("pick_event", on_pick)
    fig.canvas.mpl_connect("motion_notify_event", update_annotation_position)  # Track zoom/pan

    # ** Slider to select time step **
    if time_on:
        ax_slider_time = plt.axes([0.25, 0.025, 0.45, 0.015], facecolor='lightgoldenrodyellow')
        slider_time = Slider(ax_slider_time, 'čas [s]', 0, len(strain) - 1, valinit=0, valstep=1)

        def update(val):
            """Update plot when the slider moves and reposition annotation."""
            nonlocal selected_index, selected_x, selected_y, selected_time
            selected_time = int(slider_time.val)
            l.set_ydata(strain[selected_time])  # Update plot

            if selected_index is not None:
                selected_y = strain[selected_time][selected_index]  # Get new strain value
                annotation.xy = (selected_x, selected_y)  # Update annotation position
                annotation.set_text(f"Index: {selected_index}\nDistance: {selected_x:.2f} m\nStrain: {selected_y:.2f}")
                annotation.set_visible(True)
            else:
                annotation.set_visible(False)  # Hide if no selection

            fig.canvas.draw_idle()  # Redraw the canvas
            slider_time.valtext.set_text(f"{slider_time.val / 10:.1f}")  # Update slider label

        slider_time.on_changed(update)

    selected_time = 0  # Keep track of selected time step

    # Force the canvas to update before showing
    fig.canvas.draw()
    plt.show()


def plot_strain_time(distance, time, strain):
    """Plot strain vs. time."""
    print("TODO:")
    pass

