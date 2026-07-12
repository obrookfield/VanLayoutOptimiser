'''
v0.1
Hand-placed layout of items in a van.

There is no optimisation at this stage.

Defines a van, places items in it at predetermined locations, 
checks the layout is valid, and plots it.

Dimensions are in millimetres.
'''

from van_layout import Item, Van
from van_layout.geometry import validate_layout
from van_layout.placement import place_items
from van_layout.visualiser import plot_layout

# Dimensions - VW Transporter SWB (2014-)
van = Van(length=2572, width=1700)

# Item defined by: (name, length, width)
items = [
    Item(name="Bed", length=2000, width=1100),
    #Item(name="Twin Bed", length=1910, width=970), # More accurate bed size, standard twin.
    Item(name="Kitchen Unit", length=500, width=500),
    Item(name="Wardrobe", length=500, width=500),
    Item(name="Fire Extinguisher", length=114, width=114)
    ]

if __name__ == "__main__":
    # Place items in the van.
    placed, unplaced = place_items(items, van)
    if unplaced:
        print("Could not place:")
        for u in unplaced:
            print(f"  - {u.name} ({u.length} x {u.width})")

    # Check the layout is valid.
    problems = validate_layout(items, van)
    if problems:
        print("Layout is invalid:")
        for p in problems:
            print(f"  - {p}")
    else:
        print("Layout is valid.")

    plot_layout(items, van, title="v0.2: Naive algorithm layout")