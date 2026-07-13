# Visualise the layout of items in the van.

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from .geometry import Item, Van
from .mass_balance import balance_offset

def plot_layout(items: list[Item], van: Van, title: str = "Van Layout"):
    # Draw the outline of the van and every placed item with labels.
    fig, ax = plt.subplots(figsize=(van.length / 500, van.width / 500))

    # Van Outline
    ax.add_patch(Rectangle((0,0), van.length, van.width, fill=None, edgecolor="black", linewidth=2))

    colors = plt.cm.tab20.colors  # Use a colourmap for item colours
    for i, item in enumerate(items):
        if not item.placed:
            continue
        color = colors[i % len(colors)]
        ax.add_patch(Rectangle((item.x, item.y), item.length, item.width, facecolor=color, edgecolor="black", alpha=0.8))

        ax.text(item.x + item.length / 2, item.y + item.width / 2, item.name, ha="center", va="center", fontsize=8)

    # Plot centre of mass
    x_offset, y_offset = balance_offset(items, van)
    x_com = (van.length / 2) + (x_offset * van.length / 2)
    y_com = (van.width / 2) + (y_offset * van.width / 2)
    ax.plot(x_com, y_com, 'ro', markersize=4)
    ax.text(x_com, y_com+100, "CoM", ha="center", va="center", fontsize=8)

    ax.set_xlim(-100, van.length + 100)
    ax.set_ylim(-100, van.width + 100)
    ax.set_aspect("equal")
    ax.set_xlabel("Length (mm), front to back.")
    ax.set_ylabel("Width (mm), left to right.")
    ax.set_title(title)

    plt.show()